#!/usr/bin/env bash

if [[ "$#" -ne 2 ]]; then
    echo "Usage: $0 user group"
    exit 1
fi

USER=$1
GROUP=$2
CLUSTERENDPOINT=https://api.kubepub.hotelscan.net
CLUSTERNAME=kubepub.hotelscan.net
CACERT=certs/ca.crt
CAKEY=certs/ca.key
CLIENTCERTKEY=clients/$USER/$USER.key
CLIENTCERTCSR=clients/$USER/$USER.csr
CLIENTCERTCRT=clients/$USER/$USER.crt

mkdir -p clients/$USER

openssl genrsa -out $CLIENTCERTKEY 4096
openssl req -new -key $CLIENTCERTKEY -out $CLIENTCERTCSR \
      -subj "/O=$GROUP/CN=$USER"
openssl x509 -req -days 365 -sha256 -in $CLIENTCERTCSR -CA $CACERT -CAkey $CAKEY -set_serial 2 -out $CLIENTCERTCRT

cat <<-EOF > clients/$USER/kubeconfig
apiVersion: v1
kind: Config
preferences:
  colors: true
current-context: $CLUSTERNAME
clusters:
- name: $CLUSTERNAME
  cluster:
    server: $CLUSTERENDPOINT
    certificate-authority-data: $(cat $CACERT | base64 --wrap=0)
contexts:
- context:
    cluster: $CLUSTERNAME
    user: $USER
  name: $CLUSTERNAME
users:
- name: $USER
  user:
    client-certificate-data: $(cat $CLIENTCERTCRT | base64 --wrap=0)
    client-key-data: $(cat $CLIENTCERTKEY | base64 --wrap=0)
EOF

