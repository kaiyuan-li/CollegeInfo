# College-Info
Scrapes popular sites for info about colleges

To try it out:

Download the project

Getting Python with relevant packages and setting up MongoDB:
Make sure you have Python 2.7 installed and the latest version of MongoDB with the compass GUI
Make sure Python is in your path variables, and that C:\Program Files\MongoDB\Server\3.6\bin is added as well
Create this directory to store data C:\data\db, refer to this thread: https://stackoverflow.com/questions/26585433/mongodb-failed-to-connect-to-127-0-0-127017-reason-errno10061
Install scrapy with $ pip install scrapy
Install splash with $ pip install scrapy-splash
Install dependencies as needed with pip

Setting up splash (Currently splash settings are only custom for Forbes scraper):
For splash to work, install Docker, if you do not have a compatible OS then you must install Oracle VM VirtualBox
To set up Docker with a local VM, follow the instructions on this site: https://docs.docker.com/machine/get-started/
    For windows: $ docker-machine create --driver virtualbox default
    "default" is the name of the machine
    Check that the machine was created with $ docker-machine ls, note down the VM's ip address under URL
    Ex: 192.168.99.100, from 'tcp://192.168.99.100:2376' under URL
Run Docker and enter these commands:
    $ docker pull scrapinghub/splash
    $ docker run -p 8050:8050 scrapinghub/splash
This will host splash on port 8050
Navigate to /CollegeInfo/CollegeInfo/spiders/forbes.py
If you are NOT using a VM, change 'SPLASH_URL': 'http://192.168.99.100:8050/' to 'SPLASH_URL' = 'http://localhost:8050/'
Now you can go to localhost:8050 to access splash if you want
OTHERWISE, change the IP address in 'SPLASH_URL': 'http://192.168.99.100:8050/' to your VM's IP address found earlier, do not modify 8050
Now you can go to http://YOUR_VM_IP_ADDRESS:8050 to access splash if you want

Scraping information:
Open command line and enter mongod to start the server, it should be hosted on port localhost:27017
Open another command line and cd to the project directory:
    $ scrapy crawl usnews
    $ scrapy crawl forbes
If everything runs without problem, open the compass GUI for MongoDB, connect to localhost and port 27017, and you should see the data
