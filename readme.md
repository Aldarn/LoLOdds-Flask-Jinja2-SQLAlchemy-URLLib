Introduction
============

For an overview of my solution please refer to ideas.md.


Installation
============

1. Install Python:
    * Using brew: `brew install python`
    * From the website: https://www.python.org/downloads/mac-osx/

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

8. Install bower:

        npm install -g bower

9. Install gulp:

        npm install -g gulp

10. Install all dependencies:

        pip install -r requirements.txt
        npm install
        bower install

12. Create the database:

        python create_db.py
        
12a. OPTIONAL: Use the pre-populated SQL data found in sql/hextechprojectx_PREPOPULATED.sql

This contains a fair number of games obtained from running the daemon for a couple of hours. You should be able to load 
it through your favourite MySQL tool - I used Sequel Pro to dump the data.


Running Locally
===============

Web App
-------

Open a new shell window and run the following from the project base directory:

        source env/bin/activate
        gulp

Navigate to `localhost:8000` and the application should be running.

Daemon
------

The daemon will query the LoL API and populate the database with featured games and related content. If you 
run the web app without initialising the database with any data and without running the daemon then it 
won't have any games or odds to display.

To run the daemon execute the following from the project base directory:

        source env/bin/activate
        python src/api_daemon/daemon.py


Running Tests
=============

To run both the tests run `nosetests` or the following:

        python test.py
