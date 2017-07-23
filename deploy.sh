#!/bin/bash

rpmdev-setuptree
cp ~/rpmbuild/node-app.spec ~/rpmbuild/SPECS/
npm install --prefix=/vagrant /vagrant --production
tar --exclude=RPMS \
	--exclude=SOURCES \
	--exclude=SPECS \
	--exclude=SRPMS \
	--exclude=BUILD \
	--exclude=BUILDROOT \
	-czvf ~/rpmbuild/SOURCES/node-app.tar.gz --directory="/home/vagrant/rpmbuild" .
rpmbuild -bb ~/rpmbuild/SPECS/node-app.spec

scp -o StrictHostKeyChecking=no -i /tmp/repo_private_key ~/rpmbuild/RPMS/x86_64/node-app-* vagrant@192.168.33.30:/home/vagrant/repo/packages
ssh -o StrictHostKeyChecking=no -i /tmp/repo_private_key vagrant@192.168.33.30 << _EOC
	createrepo --update /home/vagrant/repo
_EOC

ssh -o StrictHostKeyChecking=no -i /tmp/webserver_private_key vagrant@192.168.33.20 << _EOC
	sudo yum clean all
	rpm -q  node-app || sudo yum --disablerepo=\* --enablerepo=geniousphp install node-app -y
	rpm -q  node-app && sudo yum --disablerepo=\* --enablerepo=geniousphp update node-app -y

_EOC
