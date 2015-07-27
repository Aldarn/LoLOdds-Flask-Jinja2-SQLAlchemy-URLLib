Introduction
============

For an overview of my solution please refer to notes.md.


Installation
============

1. Install Python:

    * On OS X:
        Using brew: `brew install python`
        From the website: https://www.python.org/downloads/mac-osx/

    * On linux:
        sudo apt-get install mysql-server

2. Install pip to manage Python packages:

        brew install pip

3. Install MySQL. Check the MySQL website for instructions for your specific OS.
        
4. Create two empty MySQL databases (TODO: Make this happen automatically):

        hextechprojectx
        testhextechprojectx

5. Install virtualenv to deal with all of our dependencies:

        pip install virtualenv

6. Activate the virtualenv so any setup is installed in the virtual environment:
    
        virtualenv env
        source env/bin/activate

7. Install nodejs (& npm) from https://nodejs.org/.

**Note:** On linux you may need to do the following:

* Install npm:
        sudo apt-get install npm

* Fix nodejs install:
        ln -s /usr/bin/nodejs /usr/bin/node

8. Install bower:

        npm install -g bower

9. Install gulp:

        npm install -g gulp

10. Install all dependencies:

        pip install -r requirements.txt
        npm install
        bower install

**Please Note**: If you have probles with pip install, you may need to install `python-dev` and `libmysqlclient-dev` (modify the commands to use your linux flavours package manager):

        sudo apt-get install libmysqlclient-dev
        sudo apt-get install python-dev

11. Create the database:

        python create_db.py
        
12. Set your database credentials in `src/resources/client_config.py` **and** `test/python/config.py`, 
changing the variable `SQLALCHEMY_DATABASE_URI` to the following, replacing **[username]**, **[password]** 
and **[mysql host or localhost]** with your own:

        mysql://[username]:[password]@[mysql host or localhost]/hextechprojectx?charset=utf8mb4

13. Set your LoL API key in `src/resources/config.py`, changing the variable `API_KEY`.

14. **OPTIONAL**: Use the pre-populated SQL data found in sql/hextechprojectx_PREPOPULATED.sql

This contains a fair number of games obtained from running the daemon for a couple of hours. You should be able to load 
it through your favourite MySQL tool - I used Sequel Pro to dump the data.


Running Locally
===============

Web App
-------

Open a new shell window and run the following from the project base directory:

        source env/bin/activate
        gulp

Navigate to the URL shown in the terminal, which should be `http://127.0.0.1:8000`, 
and the application should be running. This URL should be interchangable with `localhost` 
and the corresponding port number.

Daemon
------

The daemon will query the LoL API and populate the database with featured games and related content. 
If you run the web app without initialising the database with any data and without running the daemon 
then it won't have any games or odds to display.

To run the daemon execute the following from the project base directory:

        source env/bin/activate
        python src/api_daemon/daemon.py


Running Tests
=============

To run the tests run `nosetests` or the following from the project base directory:

        python test.py
