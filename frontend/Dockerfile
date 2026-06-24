FROM node:20-alpine

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .

# Set environment variable for client-side routing
ENV PORT 3000

EXPOSE 3000

CMD ["npm", "run", "dev"]
