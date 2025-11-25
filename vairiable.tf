

variable "my_ami" {
  description = "AMI ID for EC2"
  default     = "ami-02d26659fd82cf299"
}

variable "my_instance" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "my_key" {
  description = "Key pair name"
  default     = "ovi"
}


