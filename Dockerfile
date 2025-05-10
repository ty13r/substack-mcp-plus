FROM node:22.15.0-alpine

RUN apk add --no-cache --update --upgrade yarn

COPY ./ /opt
WORKDIR /opt

RUN yarn install --frozen-lockfile --production && \
    yarn cache clean;

CMD ["node", "src/index.js"]