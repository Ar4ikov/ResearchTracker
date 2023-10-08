# Create react + yarn image
FROM node:18.15.0-alpine3.12 as react-yarn
WORKDIR /app
COPY ./frontend_next/package.json ./frontend_next/yarn.lock ./
RUN apt update && apt upgrade =y
RUN yarn install --frozen-lockfile
COPY ./frontend_next ./
RUN yarn build

# Run react + yarn image
FROM node:18.15.0-alpine3.12 as react-yarn-run
WORKDIR /app
COPY --from=react-yarn /app ./
CMD ["yarn", "start"]

