# Create react + yarn image
FROM node:18.15.0-alpine as react-yarn
WORKDIR /app
COPY . .
RUN apt update && apt upgrade =y
RUN yarn install --frozen-lockfile
RUN yarn build

# Run react + yarn image
FROM node:18.15.0-alpine as react-yarn-run
WORKDIR /app
COPY --from=react-yarn /app ./
CMD ["yarn", "start", "-p", "80"]

