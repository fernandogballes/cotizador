FROM node:14

WORKDIR /app

COPY frontend/package.json frontend/package.json
RUN npm install

COPY frontend/ frontend/

CMD ["npm", "start"]
