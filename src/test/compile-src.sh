#Compile the python files in /src folder
cd src
python -m compileall -l .

#Compile the python files in /src/gui
python -m compileall -l ./gui
