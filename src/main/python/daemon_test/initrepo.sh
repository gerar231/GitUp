#Create gitup directory
cd /tmp
if [[ -e gitup ]]; then
    rm -rf gitup
fi
mkdir gitup
cd gitup

#Create reporitories.csv and write initial data too it
echo "local_path" >> repositories.csv
echo "/tmp/testrepo" >> repositories.csv

#Create an empty test repo to monitor
cd /tmp
if [[ -e testrepo ]]; then
    rm -rf testrepo
fi
mkdir testrepo
cd testrepo
git init

