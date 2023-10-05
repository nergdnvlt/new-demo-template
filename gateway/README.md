# Gateway
This is a deployment and configuration for [@apollo/gateway](https://www.npmjs.com/package/@apollo/gateway), which has been replaced with [`router`](https://github.com/apollographql/router) for the template. However, this can still be deployed manually.

## Prerequisites
> **Note:** If you've ran `make install-deps && make setup` on the root template, these should already be configured for you.

 1. Install all dependencies: `make install-deps`
 2. Edit `.env` to with your Apollo API key and Graph Reference.


## Run Locally
```
node server.js
```

## Deploy to GCP
```
make deploy
```

## Files

 * _.env/dot_env_ - stores environmental variables that are used for deployment
 * _.gcloudignore_ - makes Google Cloud ignore certain files
 * _cloudbuild.yaml{.tmpl}_ - the configuration file for Google Cloud Build which will build and deploy Docker containers and services in GCP
 * _Dockerfile_ - the file used to build a Docker container locally or in Cloud Build
 * _Dockerfile.unmanaged_ - an unmanaged Federation gateway container
 * _Makefile_ - a collection of command shortcuts
 * _package.json_ - package requirements for a NodeJS project
 * _server-unmanaged.js_ - the Apollo Gateway using unmanaged Federation
 * _server.js_ - the Apollo Gateway code
