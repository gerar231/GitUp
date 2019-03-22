cd ./src/main/python #Move adjacent to target script for executable
python3.7 -m PyInstaller GitUp.py --onefile #Create executable
cp ./gui/git_attributes.txt ./dist #The dist folder contains the executable, but also requires this .txt for deployment
./dist/GitUp& PID=$!; sleep 5; kill $PID #Run the executable before we zip it to make sure it opens
mv dist GitUp #Rename folder to be zipped
zip -r GitUp.zip GitUp #Zip
dropbox-deployment #Deploy
