
# create ssh key for aws key pair
ssh-keygen -t rsa -m 'PEM' -f aws_key
# ssh-keygen -f aws_key -m 'PEM' -e > aws_key.pem

chmod 400 ./deploy_key

# zip project - will be copied to remote machine

# start deploy with terraform
terraform init
terraform apply

