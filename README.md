<img src="https://user-images.githubusercontent.com/6020066/192867875-0a4a593b-e655-4da5-8a77-8036b5670f32.png" width="100%" max-height="100" text-align="center">

# SE Demo Template
A template to quickly build and deploy a Federated demo environment.

Use the included setup tool (`make setup`) whenever possible as it saves
your information and can be re-run multiple times to update `.env` files
and `cloudbuild.yaml` files.

If you are new to Git, we recommend you familiarize yourself with the [Git Basics](#git-checkout-basics) before you get started.

## Prerequisites
You'll only need to do these steps on initial setup. 

### Install Dependencies
1. Install Docker for Mac
2. Install Homebrew & Python 3: https://docs.python-guide.org/starting/install3/osx/
3. Install NVM for Mac: https://tecadmin.net/install-nvm-macos-with-homebrew/ 
4. Install NodeJS v16.13.1 using NVM: `nvm install v16.13.1`
5. Use NodeJS v16.13.1: `nvm use v16.13.1`
6. Install the Apollo CLI: https://www.apollographql.com/docs/devtools/cli/
7. Install the Rover CLI: https://www.apollographql.com/docs/rover/
8. Clone repository `git clone git@github.com:apollographql/se-demo-template.git`

### Apollo Studio 
1. Log into Studio and create a Deployed Graph
2. Get an **API Key** and note your **Graph ID** and **Variant ID**

### Google Cloud
1. Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/quickstart)
2. Login to the Google Cloud Console and create a new project
   1. Go to (https://console.cloud.google.com)[https://console.cloud.google.com/]
   2. Find the __"Sales Engineering"__ folder by searching in the drop down and then click "New Project" the "Location" needs to be "Sales Engineering"
   3. Name your new project `<your-last-name>-demo`
   4. Choose `doit.apollographql.com` under "other billing accounts" as the `Billing account`
   5. In your new project click on the menu and select "Cloud Run" from the list.
   6. Click "Enable Cloud Run API"
   7. In your new project click on the menu and select "Cloud Build" from the list.
      1. Under the "Settings" area enable the "Cloud Run Admin" and "Cloud Functions Developer"  Roles (it may ask you if you want to add the role to the service account: approve that action).
3. Authenticate with Google Cloud from a terminal on your Mac using your Apollo email
   1. Run `gcloud init`
   2. *If you ever need to change your default Project ID (this might be different from the project name so always use the ID) use the command `gcloud config set project <project-ID>`)*

## Usage
### Deploy on Google Cloud
#### **Initial Deployment**
1. Run `make install-deps` to install npm packages for each subgraph and build your `.env` and `cloudbuild.yaml` files
2. Initialize your configuration state
   1. Run `make setup` and answer the inputs for your Graph ID and Variant
   
      __OR__ 

   2. Edit the .env file in _./router_, _./subgraph1_, _./subgraph2_, _./subgraph3_ with the appropriate values
3. Run `make publish` to generate a temporary supergraph schema
4. Deploy your router and subgraphs with `make deploy` (say "(Y)es" if it asks you to activate any GCP services)
5. After successfully deployed, update the routing urls for the subgraphs
   1. Re-run `make setup` and say Y to automatically fetch and set the urls

      __OR__

   2. Go to the Google Run Console to find the URLs and update the `.env` files for _./subgraph1_, _./subgraph2_, _./subgraph3_
6. Run `make publish` to finalize your supergraph schema (this will run `make publish` in each of your subgraph directories, you can also run those one by one)
7. Update Apollo Studio with the right URL for your router (you can find this in your `.config` file or on Google Cloud Run)

#### **Post Deployment - Updates**
After deploying, you only need to use these 
1. `make deploy` - Deploy new changes to your router and subgraphs
2. `make publish` - Publish your schema changes to Apollo

## Run Locally with Unmanaged Federation (Local Composition)

`make run-local-unmanaged`

## Run Locally with Managed Federation

1. Publish your schemas to Apollo, `make publish`
2. Update the routing urls for the subgraphs
    1. Edit the `ROUTING_URL` in each of the subgraph directories `.env` file:  ./subgraph1, ./subgraph2, ./subgraph3 __OR__ run `make setup` again to set them (recommended).
    2. Publish your graph with `make publish`
 1. Deploy locally: `make run-local-managed`
   
## Generate Traffic

### Cloud Scheduler Method (recommended)

 1. Enable Cloud Functions by going to that tab in the Google Cloud Console
 2. Go to Cloud Build->Settings and enable the "Cloud Functions" service account
 3. Edit the client/client.py file to put in the URL of your gateway (must be deployed, not local) __OR__ if you've ran `make setup` after deploying on GCP, this will be already be configured
 4. Run `make traffic-gen` it may ask you to enable some things like AppEngine, say (y)es (this will run `make setup-traffic-gen` and `make deploy` in the `client` directory)
 5. If you need to re-deploy your client for any reason go into the `client` directory and run `make deploy`

### CI/CD Method

 1. Update the `client/client.py` file to have the right URL for your gateway (if you change your schema you will need to update the queries in this file).
 2. Update the `.github/workflows/client_gen.yaml` file to have the correct cron string.
 3. Commit and deploy your code to your forked repo and GitHub Actions will start generating traffic for your site.

## Resources
### Git Checkout Basics

If you want to save changes that you make to your demo, it's a good idea
to use git branches.

 1. Check out the code: `git clone git@github.com:apollographql/se-demo-template.git` or `git clone https://github.com/apollographql/se-demo-template.git` (use the second one if you haven't setup a SSH key in GitHub).
 2. Make your own branch: `git checkout -b <my-branch-name>` use your name or something for `<my-branch-name>`.
 3. Push (create) your branch on GitHub: `git push origin <my-branch-name>`
 4. To add a new file to your branch: `git add <my-file-name>`
 5. If you want to save (a)ll your changes and include a (m)essage: `git commit -am "My message about what I changed"`
 6. If you want to save it remotely (on GitHub) you need to push: `git push origin <my-branch-name>`
 7. If you want to update your branch with updates made to the main branch: `git pull origin master`
 8. If you want to revert a change to a file that you haven't set saved (commited): `git checkout <the-file-name>`

### Migrating from Gateway
If you are migrating from gateway, you'll want to update up your existing `.env` and configuration:

1. Download dependencies and update environment files: `make install-deps`
2. Reconfigure your state: `make setup`
3. Redeploy: `make setup`
4. *Optional: If you would like to delete your gateway: `gcloud run services delete gateway`, and specify the region when prompted (default is `us-east-1`).*

## Files & Directories

 * _.github/_ - configuration for GitHub Actions (CI/CD)
 * _client/_ - a simple client app to send GQL queries to your demo
 * _gateway/_ - the Apollo Gateway
 * _router/_ - the Apollo router used for this demo
 * _subgraph1/_ - a subgraph for this demo
 * _subgraph2/_ - a subgraph for this demo
 * _subgraph3/_ - a subgraph for this demo
 * _.gitignore_ - files that git should not manage
 * _local-test-unmanaged.yaml_ - a config file for Docker Compose to run an unmanaged Federation demo
 * _local-test.yaml_ - a config file for Docker Compose to run a managed Federation demo
 * _Makefile_ - a collection of command shortcuts
 * _supergraph.yaml_ - the config file that Rover uses to create a supergraph offline (ie, without Studio)

## Customizing Your Demo

Change the schemas for each of the subgraphs and update the data in the `database.json` files.  In each `server.js` make sure you have the right resolvers for the queries and/or mutations on your graph. 
