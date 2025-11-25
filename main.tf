provider "aws" {
  region = "ap-south-1"
}

resource "aws_security_group" "jarvis_sg" {
  name        = "jarvis-sg"
  description = "Security group for Jarvis"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Jarvis App Port"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "myserver" {
  ami                    = var.my_ami
  instance_type          = var.my_instance
  key_name               = var.my_key

  # IMPORTANT: SG reference
  vpc_security_group_ids = [aws_security_group.jarvis_sg.id]

  tags = {
     Name = "Jarvis-Server"
  }
}
