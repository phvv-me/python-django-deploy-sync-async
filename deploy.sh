
# create ssh key for aws key pair
ssh-keygen -t rsa -f deploy_key
chmod 400 ./deploy_key

# zip project - will be copied to remote machine

# start deploy with terraform
terraform init
terraform apply

