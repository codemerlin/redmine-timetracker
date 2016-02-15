#  Redmine Help Me Track 

*Runs on Python 2.7* 

### To execute from the source project

assumption is that the project is cloned in M:\projects\rm.helpmetrack

You would need to install https://www.microsoft.com/en-us/download/details.aspx?id=44266 on windows before running following commands

```
pip install requests

pip install pyinstaller

pip install paramiko

pip install PySide

python main.py

```

### to build, on windows 

```
cd buildscripts\windows\

.\single_build.bat

```

### to build, on ubuntu

```
.\single_build.sh

```




# Code Details
All the background work is broken into threads/timers, CoreEngine.py is the file that controls all of that.
PySideMain.py is the file that has all the ui code.
all the redmine operaions are in RedMineClient.py.
main.py is the starting point though