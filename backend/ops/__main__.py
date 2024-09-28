import pulumi
import pulumi_aws as aws
from pulumi_aws import ec2

config = pulumi.Config()

pg_username = config.require_secret("pgUsername")
pg_password = config.require_secret("pgPassword")
key_name = config.require_secret("keyName")
ami = config.require_secret("ami")
certificate = config.require_secret("certificate")



# Create a new VPC
vpc = aws.ec2.Vpc("kn-vpc",
                  cidr_block="10.0.0.0/16",
                  enable_dns_support=True,
                  enable_dns_hostnames=True)

# Create subnets
subnet_a = aws.ec2.Subnet("kn-subnet-a",
                          vpc_id=vpc.id,
                          cidr_block="10.0.1.0/24",
                          availability_zone="eu-west-3a",
                          map_public_ip_on_launch=True,

                          )

subnet_c = aws.ec2.Subnet("kn-subnet-b",
                          vpc_id=vpc.id,
                          cidr_block="10.0.2.0/24",
                          availability_zone="eu-west-3c",
                          map_public_ip_on_launch=True,

                          )

# Create an Internet Gateway
igw = aws.ec2.InternetGateway("kn-igw",
                              vpc_id=vpc.id)


# Create a route table
route_table = aws.ec2.RouteTable("kn-route-table",
                                 vpc_id=vpc.id,
                                 routes=[aws.ec2.RouteTableRouteArgs(
                                     cidr_block="0.0.0.0/0",
                                     gateway_id=igw.id
                                 )])

# Associate route table with the subnet
route_table_association_a = aws.ec2.RouteTableAssociation("kn-route-table-assc-a",
                                                          subnet_id=subnet_a.id,
                                                          route_table_id=route_table.id
                                                          )

route_table_association_c = aws.ec2.RouteTableAssociation("kn-route-table-assc-b",
                                                          subnet_id=subnet_c.id,
                                                          route_table_id=route_table.id
                                                          )

# # Create a Load Balancer security group
elb_sg = aws.ec2.SecurityGroup("kn-elb-sg",
                               vpc_id=vpc.id,
                               description="Allow HTTP and HTTPS traffic",
                               ingress=[
                                   {
                                       "protocol": "tcp",
                                       "from_port": 80,
                                       "to_port": 80,
                                       "cidr_blocks": ["0.0.0.0/0"]
                                   },
                                   {
                                       "protocol": "tcp",
                                       "from_port": 443,
                                       "to_port": 443,
                                       "cidr_blocks": ["0.0.0.0/0"]
                                   }
                               ],
                               egress=[
                                   {
                                       "protocol": "-1",
                                       "from_port": 0,
                                       "to_port": 0,
                                       "cidr_blocks": ["0.0.0.0/0"]
                                   }
                               ]
                               )

# Create a security group for the EC2 instance
ec2_sg = aws.ec2.SecurityGroup("kn-ec2-sg",
                               vpc_id=vpc.id,
                               description="Allow all traffic",
                               ingress=[{
                                   "protocol": "tcp",
                                   "from_port": 80,
                                   "to_port": 80,
                                   "security_groups": [elb_sg.id]
                               }, {
                                   "protocol": "tcp",
                                   "from_port": 22,
                                   "to_port": 22,
                                   "cidr_blocks": ["0.0.0.0/0"]
                               }],
                               egress=[{
                                   "protocol": "-1",
                                   "from_port": 0,
                                   "to_port": 0,
                                   "cidr_blocks": ["0.0.0.0/0"]
                               }]
                               )


# testing purposes
# User data to start a HTTP server in the EC2 instance
user_data = """#!/bin/bash
echo "Hello, World from Knowledgenest !" > index.html
nohup python -m SimpleHTTPServer 80 &
"""


# Create an EC2 instance
ec2_instance = aws.ec2.Instance("kn-backend-1",
                                instance_type="t2.micro",
                                # custom AMI or ubuntu
                                ami=ami,
                                subnet_id=subnet_a.id,
                                security_groups=[ec2_sg.id],
                                associate_public_ip_address=True,
                                key_name=key_name)

# export public ip address to connect through ssh
pulumi.export("ec2-public-ip", ec2_instance.public_ip)


# Create a security group for the RDS instance
rds_sg = aws.ec2.SecurityGroup("kn-rds-sg",
                               vpc_id=vpc.id,
                               description="Allow RDS access",
                               ingress=[{
                                   "from_port": 5432,
                                   "to_port": 5432,
                                   "protocol": "tcp",
                                   "security_groups": [ec2_sg.id]
                               }
                               ],
                               egress=[{
                                   "protocol": "-1",
                                   "from_port": 0,
                                   "to_port": 0,
                                   "cidr_blocks": ["0.0.0.0/0"]
                               }]
                               )

rds_subnet_group = aws.rds.SubnetGroup("rds_subnet_group",
                                       subnet_ids=[subnet_a.id, subnet_c.id],
                                       )

# Create a PostgreSQL RDS instance
rds_instance = aws.rds.Instance("kn-db-1",
                                instance_class="db.t3.micro",
                                allocated_storage=20,
                                engine="postgres",
                                engine_version="12",
                                db_name="mydatabase",
                                username=pg_username,
                                password=pg_password,
                                skip_final_snapshot=True,
                                db_subnet_group_name=rds_subnet_group.name,
                                vpc_security_group_ids=[rds_sg.id],
                                )

# # Create a Target Group
target_group = aws.lb.TargetGroup("kn-backend-target-group",
                                  port=80,
                                  protocol="HTTP",
                                  vpc_id=vpc.id,
                                  target_type="instance",
                                  health_check=aws.lb.TargetGroupHealthCheckArgs(
                                      path="/health",
                                      protocol="HTTP",
                                      interval=30
                                  ))

# # Attach the EC2 instance to the Target Group
tg_attachment = aws.lb.TargetGroupAttachment("kn-tg-attachment",
                                             target_group_arn=target_group.arn,
                                             target_id=ec2_instance.id,
                                             port=80)


# # Create a Load Balancer
load_balancer = aws.lb.LoadBalancer("kn-elb",
                                    internal=False,
                                    # Security group allowing HTTPS traffic
                                    security_groups=[elb_sg.id],
                                    subnets=[subnet_a.id, subnet_c.id],
                                    load_balancer_type="application")


# # Make the ec2 instance accesible by the ELB
# ec2_sg.ingress[0]["security_groups"] = [elb_sg.id]


# # Create a Listener for HTTPS
https_listener = aws.lb.Listener("https-listener",
                                 load_balancer_arn=load_balancer.arn,
                                 port=443,
                                 protocol="HTTPS",
                                 ssl_policy="ELBSecurityPolicy-2016-08",
                                 certificate_arn=certificate,
                                 default_actions=[aws.lb.ListenerDefaultActionArgs(
                                     type="forward",
                                     target_group_arn=target_group.arn
                                 )])

# # Output the Load Balancer DNS name
pulumi.export("load_balancer_dns", load_balancer.dns_name)
