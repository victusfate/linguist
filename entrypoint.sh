#!/usr/bin/env sh
# this works, but no major advantage over building the image with it since it deploys ok
# pip install -v -r full_requirements.txt --no-cache
# python3 -m spacy download en_core_web_sm
# # python3 -m spacy download en_core_web_trf
# # python3 -c "import spacy; p = spacy.load('en_core_web_sm')"

consul_addr=$(echo http://$CONSUL_HOST:8500)
aws_key=$(consul kv get -http-addr=$consul_addr 'aws/auth/linguist/key')
aws_secret=$(consul kv get -http-addr=$consul_addr 'aws/auth/linguist/secret')
aws_region=$(consul kv get -http-addr=$consul_addr 'aws/region')

mkdir /root/.aws
printf "[default]\naws_access_key_id = $aws_key\naws_secret_access_key = $aws_secret\n" > /root/.aws/credentials
chmod u+rw,og-rwx /root/.aws/credentials

echo "consul_addr $consul_addr"
echo $(which python)
echo $(which pip)
echo $(which python3)
echo $(which pip3)
echo $(uname -s | tr A-Z a-z)
echo "$aws_region"

/usr/bin/python3 /var/www/linguist/bin/server.py
# python3 -m http.server