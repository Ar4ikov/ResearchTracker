# Create react + yarn image
FROM node:18.15.0-alpine
WORKDIR /app
COPY . .
RUN yarn lock && yarn install
RUN yarn build

CMD ["yarn", "start", "-p", "80"]

