#!/bin/sh

#touch /home/node/haraka/config/loglevel
#echo 'DEBUG' > /home/node/haraka/config/loglevel
openssl req -x509 -nodes -days 2190 -newkey rsa:2048 \
    -keyout /home/node/haraka/config/tls_key.pem -out /home/node/haraka/config/tls_cert.pem \
    -subj "/C=$TLS_KEY_C/ST=$TLS_KEY_ST/L=$TLS_KEY_L/O=$TLS_KEY_O/OU=$TLS_KEY_OU/CN=$TLS_KEY_CN"
touch /home/node/haraka/config/auth_flat_file.ini
echo -e "[core]\nmethods=CRAM-MD5\n\n[users]\n$MAIL_USER=$MAIL_PASSWORD" \
    	> /home/node/haraka/config/auth_flat_file.ini
touch /home/node/haraka/config/relay_acl_allow
echo $NETWORK > /home/node/haraka/config/relay_acl_allow

exec "$@"