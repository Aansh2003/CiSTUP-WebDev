# Use a base image with Node.js
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app
COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
