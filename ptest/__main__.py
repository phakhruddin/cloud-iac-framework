"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.BucketV2('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

config = pulumi.Config()
key_name = config.require("keyName")  # EC2 KeyPair name for SSH access

# 1. VPC
vpc = aws.ec2.Vpc("bastion-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
)

# 2. Subnet
subnet = aws.ec2.Subnet("bastion-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
)

# 3. Internet Gateway
igw = aws.ec2.InternetGateway("bastion-igw", vpc_id=vpc.id)

# 4. Route Table + Association
route_table = aws.ec2.RouteTable("bastion-rt",
    vpc_id=vpc.id,
    routes=[{
        "cidr_block": "0.0.0.0/0",
        "gateway_id": igw.id,
    }]
)

route_table_association = aws.ec2.RouteTableAssociation("bastion-rt-assoc",
    subnet_id=subnet.id,
    route_table_id=route_table.id
)

# 5. Security Group (SSH access only)
secgroup = aws.ec2.SecurityGroup("bastion-sg",
    vpc_id=vpc.id,
    description="Allow SSH",
    ingress=[{
        "protocol": "tcp",
        "from_port": 22,
        "to_port": 22,
        "cidr_blocks": ["0.0.0.0/0"],
    }],
    egress=[{
        "protocol": "-1",
        "from_port": 0,
        "to_port": 0,
        "cidr_blocks": ["0.0.0.0/0"],
    }]
)

# 6. Bastion EC2 Instance
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[{"name": "name", "values": ["amzn2-ami-hvm-*-x86_64-gp2"]}]
)

bastion = aws.ec2.Instance("bastion-host",
    instance_type="t3.micro",
    vpc_security_group_ids=[secgroup.id],
    ami=ami.id,
    subnet_id=subnet.id,
    key_name=key_name,
    associate_public_ip_address=True,
    tags={"Name": "BastionHost"}
)

# 7. Outputs
pulumi.export("bastion_public_ip", bastion.public_ip)
pulumi.export("ssh_command", pulumi.Output.concat("ssh ec2-user@", bastion.public_ip))
