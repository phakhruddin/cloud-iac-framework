#!/usr/bin/env python3

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_ram as ram,
    Stack, CfnOutput, Duration, Tags, RemovalPolicy
)
from constructs import Construct

class SplunkIndexerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Parameters
        vpc_cidr = "10.0.0.0/16"
        cross_account_ids = ["112233445566", "223344556677"]  # Replace with actual account IDs
        splunk_ami_id = "ami-0c55b159cbfafe1f0"  # Replace with your Splunk AMI ID
        instance_type = "m5.2xlarge"
        min_capacity = 2
        max_capacity = 10
        desired_capacity = 2
        
        # Create a VPC with public and private subnets
        vpc = ec2.Vpc(
            self, "SplunkVPC",
            cidr=vpc_cidr,
            max_azs=3,
            nat_gateways=3,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask=24
                )
            ]
        )
        
        # Create security groups
        indexer_sg = ec2.SecurityGroup(
            self, "IndexerSecurityGroup",
            vpc=vpc,
            description="Security group for Splunk Indexers",
            allow_all_outbound=True
        )
        
        nlb_sg = ec2.SecurityGroup(
            self, "NLBSecurityGroup",
            vpc=vpc,
            description="Security group for NLB",
            allow_all_outbound=True
        )
        
        # Allow inbound traffic from NLB to Indexers
        indexer_sg.add_ingress_rule(
            peer=nlb_sg,
            connection=ec2.Port.tcp(8089),  # Splunk management port
            description="Allow management port from NLB"
        )
        
        indexer_sg.add_ingress_rule(
            peer=nlb_sg,
            connection=ec2.Port.tcp(9997),  # Splunk forwarding port
            description="Allow forwarding port from NLB"
        )
        
        # NLB security group rules - allow connections from cross-account VPCs
        for account_id in cross_account_ids:
            nlb_sg.add_ingress_rule(
                peer=ec2.Peer.ipv4(vpc_cidr),  # Replace with specific CIDRs if needed
                connection=ec2.Port.tcp(8089),
                description=f"Allow management port from account {account_id}"
            )
            
            nlb_sg.add_ingress_rule(
                peer=ec2.Peer.ipv4(vpc_cidr),  # Replace with specific CIDRs if needed
                connection=ec2.Port.tcp(9997),
                description=f"Allow forwarding port from account {account_id}"
            )
        
        # Create IAM role for EC2 instances
        indexer_role = iam.Role(
            self, "IndexerRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        
        # Add managed policies to the role
        indexer_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )
        
        # User data script for Splunk configuration
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "yum update -y",
            "mkdir -p /opt/splunk/etc/apps/base/local",
            "cat > /opt/splunk/etc/apps/base/local/inputs.conf << 'EOL'",
            "[splunktcp://9997]",
            "connection_host = dns",
            "EOL",
            "chown -R splunk:splunk /opt/splunk",
            "/opt/splunk/bin/splunk start --accept-license --answer-yes --no-prompt"
        )
        
        # Create Auto Scaling Group for Splunk Indexers
        asg = autoscaling.AutoScalingGroup(
            self, "IndexerASG",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
            instance_type=ec2.InstanceType(instance_type),
            machine_image=ec2.MachineImage.generic_linux({
                self.region: splunk_ami_id
            }),
            security_group=indexer_sg,
            role=indexer_role,
            user_data=user_data,
            min_capacity=min_capacity,
            max_capacity=max_capacity,
            desired_capacity=desired_capacity,
            health_check=autoscaling.HealthCheck.elb(
                grace=Duration.minutes(5)
            )
        )
        
        # Create Network Load Balancer
        nlb = elbv2.NetworkLoadBalancer(
            self, "IndexerNLB",
            vpc=vpc,
            internet_facing=True,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        )
        
        # Create target groups
        management_tg = elbv2.NetworkTargetGroup(
            self, "ManagementTargetGroup",
            vpc=vpc,
            port=8089,
            protocol=elbv2.Protocol.TCP,
            target_type=elbv2.TargetType.INSTANCE,
            health_check=elbv2.HealthCheck(
                protocol=elbv2.Protocol.TCP,
                port="8089",
                healthy_threshold_count=2,
                unhealthy_threshold_count=2,
                timeout=Duration.seconds(10),
                interval=Duration.seconds(30)
            )
        )
        
        forwarding_tg = elbv2.NetworkTargetGroup(
            self, "ForwardingTargetGroup",
            vpc=vpc,
            port=9997,
            protocol=elbv2.Protocol.TCP,
            target_type=elbv2.TargetType.INSTANCE,
            health_check=elbv2.HealthCheck(
                protocol=elbv2.Protocol.TCP,
                port="9997",
                healthy_threshold_count=2,
                unhealthy_threshold_count=2,
                timeout=Duration.seconds(10),
                interval=Duration.seconds(30)
            )
        )
        
        # Add Auto Scaling Group to target groups
        management_tg.add_target(asg)
        forwarding_tg.add_target(asg)
        
        # Create listeners
        nlb.add_listener(
            "ManagementListener",
            port=8089,
            default_target_groups=[management_tg]
        )
        
        nlb.add_listener(
            "ForwardingListener",
            port=9997,
            default_target_groups=[forwarding_tg]
        )
        
        # Set up Resource Access Manager (RAM) for cross-account access
        for account_id in cross_account_ids:
            ram.CfnResourceShare(
                self, f"NLBShare-{account_id}",
                name=f"SplunkNLBShare-{account_id}",
                allow_external_principals=True,
                principals=[f"arn:aws:organizations::{account_id}:organization/o-xxxxxxxxxx"],  # Replace with actual org ID
                resource_arns=[nlb.load_balancer_arn]
            )
        
        # Outputs
        CfnOutput(
            self, "LoadBalancerDNS",
            value=nlb.load_balancer_dns_name,
            description="DNS name of the Network Load Balancer"
        )
        
        CfnOutput(
            self, "ManagementPort",
            value="8089",
            description="Splunk management port"
        )
        
        CfnOutput(
            self, "ForwardingPort",
            value="9997",
            description="Splunk forwarding port"
        )

# Entry point for CDK app
app = core.App()
SplunkIndexerStack(app, "SplunkIndexerStack")
app.synth()
