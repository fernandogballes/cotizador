# docker/frontend/Dockerfile
FROM node:18

WORKDIR /app

# Copia solo los archivos de configuración de npm
COPY Sistema/frontend/package*.json ./

# Instala las dependencias de npm
RUN npm install

# Copia el resto del código del frontend
COPY Sistema/frontend/ .

# Inicia la aplicación
CMD ["sh", "-c", "npm install && npm start"]
