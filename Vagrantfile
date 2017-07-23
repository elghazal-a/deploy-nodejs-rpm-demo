# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box_check_update = false
  config.vm.box = "centos/7"


  config.vm.define "repo" do |server|
    server.vm.hostname = "repo"
    server.vm.network "private_network", ip: "192.168.33.30"

    server.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
    end

    server.vm.synced_folder ".", "/vagrant", disabled: true
    server.vm.provision "file", source: "./repo/repo-webserver.service", destination: "/tmp/repo-webserver.service"
    server.vm.provision "shell", inline: <<-SHELL
      yum install createrepo -y
      mkdir -p /home/vagrant/repo/packages
      createrepo /home/vagrant/repo
      chown -R vagrant:vagrant /home/vagrant/repo
      mv /tmp/repo-webserver.service /etc/systemd/system/repo-webserver.service
      systemctl daemon-reload
      systemctl enable repo-webserver
      systemctl restart repo-webserver
    SHELL
  end

  config.vm.define "webserver" do |server|
    server.vm.hostname = "webserver"
    server.vm.network "private_network", ip: "192.168.33.20"

    server.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
    end

    server.vm.synced_folder ".", "/vagrant", disabled: true
    server.vm.provision "shell", inline: <<-SHELL
      yum install -y gcc-c++ make
      curl -sL https://rpm.nodesource.com/setup_6.x | sudo bash -
      yum install -y nodejs
    SHELL
    server.vm.provision "file", source: "./webserver/geniousphp.repo", destination: "/tmp/geniousphp.repo"
    server.vm.provision "shell", inline: "mv /tmp/geniousphp.repo /etc/yum.repos.d/geniousphp.repo", privileged: true
  end

  config.vm.define "builder" do |server|
    server.vm.hostname = "builder"
    server.vm.network "private_network", ip: "192.168.33.10"
    server.vm.synced_folder "./", "/vagrant" #rsync sharing (one time and ont way sync)
    server.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
    end

    server.vm.provision "shell", inline: <<-SHELL
      yum install -y rpm-build redhat-rpm-config rpmdevtools yum-utils nodejs
      curl -sL https://rpm.nodesource.com/setup_6.x | bash -
      yum install -y nodejs
      ln -s /vagrant /home/vagrant/rpmbuild -T || echo "Skipping"
      sudo -u vagrant rpmdev-setuptree
      chown -R vagrant:vagrant /home/vagrant/rpmbuild
    SHELL
    server.vm.provision "file", source: ".vagrant/machines/webserver/virtualbox/private_key", destination: "/tmp/webserver_private_key"
    server.vm.provision "file", source: ".vagrant/machines/repo/virtualbox/private_key", destination: "/tmp/repo_private_key"

  end

end


