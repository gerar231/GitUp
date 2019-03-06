#!/bin/bash
# Called to indicate a failed install to the user and
# quit the script.
function install_failed {
    echo 'Install failed'
    exit 1
}
# Called to download GitUp.
function download {
    # TODO implement this
}
# Check for an existing data directory and create one if one
# doesn't exist.
if [[ -e '/usr/share/gitup' ]]; then
    echo 'Directory /usr/share/gitup already exists please delete
          before proceeding'
    install_failed
else
    sudo mkdir /usr/share/gitup
fi
# Set up the repositories.csv file to be initially empty
sudo echo 'local_path,dirty' >> /usr/share/gitup/repositories.csv
# Download GitUp
download
# Register start_daemon to run at system start
crontab -l > tmpcron
cat cron  >> tmpcron
crontab tmpcron
rm tmpcron

