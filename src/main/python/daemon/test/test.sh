#Create gitup directory
cd /usr/share/
sudo mkdir gitup
cd gitup

#Create reporitories.csv and write initial data too it
sudo touch repositories.csv
sudo echo "local_path,last_pulled" | sudo tee repositories.csv > /dev/null
sudo echo "/tmp/testrepo,0" | sudo tee -a repositories.csv > /dev/null

#Create an empty test repo to monitor
cd /tmp
mkdir testrepo
cd testrepo
git init

#Start the daemon
#python3.7 start_daemon.py

#Stop the daemon
#python3.7 stop_daemon.py
