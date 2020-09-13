terraform {
  required_providers {
    aws = {
      # uses the latest provider from hashicorp registry
      source = "hashicorp/aws"
    }
  }
}


provider "aws" {
  # uses the default credentials
  profile = "default"
  region  = "us-west-2" # Oregon
  version = "~> 3.6.0"
}


# free tier postgres sql RDS db
resource "aws_db_instance" "db_instance" {
  allocated_storage     = 20
  max_allocated_storage = 21
  storage_type          = "gp2"
  engine                = "postgres"
  instance_class        = "db.t2.micro"
  identifier            = "mydatabase"
  name                  = "mydatabase"
  username              = "db_username"
  password              = "db_pa$$word"
  final_snapshot_identifier = "mydestroyeddatabase"

  # appends all env vars to .env file
  provisioner "local-exec" {
    command = "echo '\n' >> .env && printenv | grep 'DB_*' >> .env"

    environment = {
      DB_HOST     = self.address
      DB_NAME     = self.name
      DB_PORT     = self.port
      DB_USER     = self.username
      DB_PASSWORD = self.password
    }
  }
}


resource "aws_key_pair" "aws_key" {
  key_name   = "aws_key"
  public_key = file("~/.ssh/aws_key.pub")
}

data "aws_ami" "ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn-ami-hvm-2018*"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "django-sync" {
  depends_on = [aws_db_instance.db_instance]

  ami           = data.aws_ami.ami.id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.aws_key.id

  tags = {
    Name = "django-sync"
  }

//  user_data_base64 = base64encode(
//  <<EOF
//  #!/bin/sh
//
//  set -e
//  pip install -r requirements.txt
//  uwsgi --master --enable-threads --http-socket :8000 --module my_django_project.my_django_project.wsgi
//
//  EOF
//  )

//  connection {
//    type        = "ssh"
//    user        = "ubuntu"
//    host        = self.public_ip
//    private_key = file("~/.ssh/aws_key")
//  }
//
//  # copy zipped project code to remote machine
//  provisioner "file" {
//    source      = ".env"
//    destination = "/tmp/.env"
//  }
}

output "ip" {
  value = aws_instance.django-sync.public_ip
}

