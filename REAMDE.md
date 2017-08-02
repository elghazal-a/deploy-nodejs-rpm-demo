# deploy-nodejs-rpm-demo

There is a lot of ways to deploy your node.js app. The easiest one is to use a process manager like PM2. The hottest technology we could see now is Docker, but it has a big overhead and deploying only one service using Docker could be an overkill. This demo is not meant to compare the different deployment solutions but instead, presents  a clean and standard way (RPM) to package and deploy apps written in any language. Nodejs is chosen because it's my favorite web development platform and because of the luck of articles that show ho to deploy Node.js app via RPM.
RPM is a standariazed packaging solution for Centos. This demo will show how you can easily 
  - package your node.js app as an RPM
  - publish your package to your private RPM repo
  - Deploy your application to servers 

## Requirements
This demo runs on VMs using Vagrant and VirtualBox. In order to try this demo, you need to install both of them

## Run
This demo will setup 3 virtual machines

  - repo
    - RPM repository is installed
    - The repository is served using the SimpleHTTPServer static web server. For production use, you can use more powerful webserver
  - webserver
    - Node.js installed to run node.js app
    - Configured to install our nodejs app from our proper RPM repo
  - builder
    - Where we will build our code source, publish it to RPM repository and finally deploy it to the webserver
    - Ideally, you could use a CI/CD system like Jenkins to orchestrate those jobs
    - It has access ssh to the other 2 VMs

Boot and provision the environment
```sh
vagrant up
```

Update `node-app.spec` to set for example the version number

ssh to the builder machine and run `deploy.sh`. This will build, publish packages and deploy the new version to the webserver
```sh
vagrant ssh builder
sh rpmbuild/deploy.sh
```

The good when using RPM is that you have the possibility to rollback to previous versions. Imagine this new version contains bugs, no worries, let's rollback
```sh
vagrant ssh webserver
sudo yum --disablerepo=\* --enablerepo=geniousphp downgrade node-app -y
```

