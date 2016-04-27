# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  # config.vm.box_check_update = false
  config.vm.network "forwarded_port", guest: 5004, host: 5004
  # config.vm.network "private_network", ip: "192.168.33.10"
  # config.vm.network "public_network"

  # config.vm.synced_folder "../data", "/vagrant_data"

 
 
  config.vm.provision "shell", inline: <<-SHELL
     sudo apt-get update && sudo apt-get upgrade
     sudo apt-get install python-pip
     pip install virtualenv
   SHELL
end
