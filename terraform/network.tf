resource "aws_vpc" "vpc_main" {
    cidr_block = ""
    enable_dns_hostnames = true
    enable_dns_support = true
    provider = aws
    tags = {
    }
}

resource "aws_subnet" "sub_pub" {
    cidr_block = ""
    vpc_id = aws_vpc.vpc_main.id
    availability_zone = ""
    tags = {
    }
    map_public_ip_on_launch = true
}

resource "aws_subnet" "sub_pri" {
    vpc_id = aws_vpc.vpc_main.id
    cidr_block = ""
    availability_zone = ""
    tags = {
    }
    map_public_ip_on_launch = false
}

resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.vpc_main.id
}

resource "aws_nat_gateway" "nat" {
    private_ip = ""
    subnet_id = aws_subnet.sub_pri.id
    vpc_id = aws_vpc.vpc_main.id
}

resource "aws_route_table" "route_table" {
    vpc_id = aws_vpc.vpc_main.id
}

resource "aws_route_table_association" "route_ass" {
    route_table_id = aws_route_table.route_table.id
    subnet_id = aws_subnet.sub_pri.id
    gateway_id = aws_nat_gateway.nat.id
}
