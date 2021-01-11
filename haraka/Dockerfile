# pull official base image
FROM node:alpine

# install haraka
# --no-cache: download package index on-the-fly, no need to cleanup afterwards
# --virtual: bundle packages, remove whole bundle at once, when done
RUN apk --no-cache --virtual build-dependencies add python make g++ \
	&& npm install --quiet -g Haraka \
	&& npm cache clean --force \
    && apk del build-dependencies \
    && apk add openssl

USER node

RUN mkdir /home/node/.npm-global \
	&& mkdir /home/node/haraka
ENV PATH=/home/node/.npm-global/bin:$PATH
ENV NPM_CONFIG_PREFIX=/home/node/.npm-global

RUN haraka -i /home/node/haraka \
	&& touch /home/node/haraka/config/loglevel \
	&& echo 'DEBUG' > /home/node/haraka/config/loglevel \
	&& openssl req -x509 -nodes -days 2190 -newkey rsa:2048 \
        -keyout /home/node/haraka/config/tls_key.pem -out /home/node/haraka/config/tls_cert.pem \
        -subj "/C=RU/ST=Moscow/L=Moscow/O=/OU=/CN=example.com"

COPY smtp.ini /home/node/haraka/config/smtp.ini
COPY plugins /home/node/haraka/config/plugins
COPY auth_flat_file.ini /home/node/haraka/config/auth_flat_file.ini
# COPY tls_key.pem /home/node/haraka/config/tls_key.pem 
# COPY tls_cert.pem /home/node/haraka/config/tls_cert.pem
# COPY rabbitmq.ini /home/node/haraka/config/rabbitmq.ini

EXPOSE 8025

CMD ["haraka", "-c", "/home/node/haraka"]

