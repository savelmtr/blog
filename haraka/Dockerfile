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

RUN haraka -i /home/node/haraka 

COPY config/* /home/node/haraka/config/

EXPOSE 8025

ENTRYPOINT ["/home/node/haraka/config/entrypoint.sh"]

CMD ["haraka", "-c", "/home/node/haraka"]
