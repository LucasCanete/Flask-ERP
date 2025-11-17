# ERP-NEXT Flask Extension
Flask wrapper for ERP-Next for internal use at peerMetering GmbH.

## Table of Contents
1. [About the Project](#about-the-project)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [How to use](#how-to-use)
5. [Project Status](#project-status)
6. [Q&A](#q&a)

## About the project
This flask wrapper around the ERP-Next software serves two purposes. The first one is to generate serial numbers for the products (PM01, PM02, PM03 etc.) and upload them to ERP-Next. The second purpose is to generate an eLS (as an xml file) based on the latest booked Lieferschein and send it to an email (e.g to a client),


## Features
- Generates large quantities of serial numbers (loading bar included)
- Uploads them automatically to the ERP-System
- When a Lieferschein is booked, it sends an email with the eLS (XML file) to a given email addess


## Getting Started
### Connect to the Server
```
$ssh admin@portalpy.local       password: ****
```
### Create working directory and clone repo
```
$mkdir ERP
$cd ERP
$git clone https://github.com/LucasCanete/Flask-ERP.git
```
### Create VENV and install dependencies

```
$ERP/Flask-ERP$ python -m venv venv
$ERP/Flask-ERP$ source venv/bin/activate
(venv) $ERP/Flask-ERP$ pip install -r requirements.txt
```

### Configure Address in .env
Inside .env there are three variables crucial for the correct functioning. Configure them depending if you are on the test system or production system:

```
BLABLABLA
```

### Run the code
For testing purposes only:
```
(venv) $ERP/Flask-ERP$ python run.py
```
### To make the code run in the background create a service:

```
sudo vim /etc/systemd/system/erp.service
```

### Service Example:
```
[Unit]
Description=ERP for Portalpy with Gunicorn (Test)
After=network.target

[Service]
User=admin
Group=admin
WorkingDirectory=/home/admin/ERP/Flask-ERP
Environment="PATH=/home/admin/ERP/Flask-ERP/venv/bin"
ExecStart=/home/admin/ERP/Flask-ERP/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 erp_system:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

```

### Activate and set service for automatic restart:
```
sudo systemctl daemon-reload
sudo systemctl enable erp.service
sudo systemctl start erp.service
```
### Useful commands:

See log info while code is running:
```
sudo journalctl -u erp.service -f
```
Stop the service:
```
sudo systemctl stop erp.service
```
Restart the service:
```
sudo systemctl restart erp.service
```

## How To Use
Once the rapsberry pi is on and with the erp service running go to browser and type:
```
http://portalpy.local:8000/login
```
You will will directed to the login page where you can register or login directly


## Project Status
This project is still under development. Some things that still need to be done:

- [x] Test automatic sending of reports at 18:
  Failed. Gunicorn does not run run.py therefore it never starts the scheduler. Move the scheduler to a different file.
- [] Test the pi in an environment where the wlan is not known


## Q&A
Coming soon

## License
© 2025 
