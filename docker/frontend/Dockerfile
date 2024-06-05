# docker/frontend/Dockerfile
FROM node:14

WORKDIR /app

COPY Sistema/frontend/package.json package.json
RUN npm install

COPY Sistema/frontend/ .

CMD ["npm", "start"]
