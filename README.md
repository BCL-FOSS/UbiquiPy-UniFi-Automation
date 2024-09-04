# UbiquiPy: Ubiquiti UniFi Python Library #
[Click here to learn more](https://www.baughcl.com/ubiquipy.html)

## Python wrapper for Ubiquiti UniFi API ##

## UniFiNetAPI.py can be utilized as a module in your scripts, will be upload to PyPi as a library soon for pip install ##

### Test Library with CLI App. This is a very rough CLI tool showcasing 5 API endpoints. ###
### For full functionality, add UniFiNetAPI.py & models->util_models-PDF.py/Utility.py to your project. ###

* git clone
* cd ubiquipy/
* apt install python3.12-venv
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install requests ipython fpdf2
* python3 app.py

#### Current Implemented Features ####

* All UDM Pro & Controller Endpoints
* All Site Endpoints (Network)
* All Callable commands (Network)

#### Current Features Under Development ####

* Implementation of all uncatagorized/experimental endpoints (Network)
* Further improvements on data parsing from returned JSON
* Upload to PyPi for pip installation

#### Upcoming Features ####
* Protect & Access API modules
* docker image 
* .EXE, .deb, .dmg executables

##### Internal Bitbucket Repo - Pull from the experiment Branch #####

* git branch -a
* git checkout experiment
* git pull origin experiment



