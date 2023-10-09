# Create react + yarn image
FROM node:18.15.0-alpine as react-yarn
WORKDIR /app
COPY . .
RUN yarn install --frozen-lockfile
RUN yarn build

CMD ["yarn", "start", "-p", "80"]

