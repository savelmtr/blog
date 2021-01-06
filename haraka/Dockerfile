# pull official base image
FROM node:alpine

# install haraka
# --no-cache: download package index on-the-fly, no need to cleanup afterwards
# --virtual: bundle packages, remove whole bundle at once, when done
RUN apk --no-cache --virtual build-dependencies add \
    python \
    make \
    g++ \
	&& npm install --quiet --no-progress -g Haraka \
	&& npm cache clean --force \
    && apk del build-dependencies

USER node

RUN mkdir /home/node/.npm-global \
	&& mkdir /home/node/haraka
ENV PATH=/home/node/.npm-global/bin:$PATH
ENV NPM_CONFIG_PREFIX=/home/node/.npm-global

RUN haraka -i /home/node/haraka

COPY smtp.ini /home/node/haraka/config/smtp.ini
COPY plugins /home/node/haraka/config/plugins
COPY host_list /home/node/haraka/config/host_list

EXPOSE 8025

CMD ["haraka", "-c", "/home/node/haraka"]