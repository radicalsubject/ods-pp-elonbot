# ods-pp-elonbot

template for CI/CD on Github Actions and Dokku

## first step - generate ssh key on local
ssh-keygen -t rsa -C "your@email.com"

secrets.DOKKU_SSH_KEY => id_rsa

## then on the remote host with dokku:

sudo dokku ssh-keys:add dokku_key ./id_rsa.pub
sudo root ssh-keys:add dokku_key ./id_rsa.pub
sudo chmod 600 /home/dokku/.ssh/authorized_keys
sudo chmod 700 /home/dokku/.ssh/
dokku git:allow-host github.com
dokku apps:create bot

## then push from CI
when project is pushed in main, CI triggers pushing project to Dokku host 
if buildpack is not specified, then Dockerfile is used to build an image

question to solve - how to stop previous dokku app when pushing new? i suspect dokku doesnt do that automatically. i guess this is a feature managed in restarting policies. the previous container is up for ~1 minute ususally.