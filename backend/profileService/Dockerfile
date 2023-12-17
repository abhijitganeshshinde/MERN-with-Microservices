FROM node:18
WORKDIR /beprofile
COPY  package.json .
RUN npm install
COPY . .
EXPOSE 3002
CMD [ "node","index.js" ]