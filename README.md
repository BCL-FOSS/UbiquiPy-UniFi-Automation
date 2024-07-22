# UbiquiPy: UniFi Automation Framework & CLI Management Tool #

## Allows for simple administration on the command line. The net_admin option holds all UniFi Network features, the other options are under development.

### Environment Initialization ###

* git clone https://github.com/BCL-FOSS/UbiquiPy-UniFi-Automation.git
* cd ubiquipy/
* apt install python3.10-venv (if on Ubuntu)
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install requests ipython fpdf2
* python3 app.py


### Pull from the experiment Branch ###

* git branch -a
* git checkout experiment
* git pull origin experiment

#### Current Implemented Features ####

* All UDM Pro & Controller Endpoints
* All Site Endpoints (Network)
* All Callable commands (Network)

#### Currentl Features Under Development ####

* Implementation of all uncatagorized/experimental endpoints (Network)
* Further improvements on data parsing from returned JSON

#### Upcoming Features ####
* Protect & Access modules
* docker image 
* .EXE, .deb, .dmg executables



