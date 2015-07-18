Installation
============

1. Install Python:
    * Using brew: `brew install python`
    * From the website: https://www.python.org/downloads/mac-osx/

2. Install pip to manage Python packages:

        brew install pip

3. Install MySQL:

        *** TODO ***
        
4. Create two empty MySQL databases (TODO: Make this happen automatically):

        hextechprojectx
        testhextechprojectx

5. Install virtualenv to deal with all of our dependencies:

        pip install virtualenv

6. Activate the virtualenv so any setup is installed in the virtual environment:
    
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

11. OPTIONAL: Install the python project:

        python setup.py install

12. Create the database *if you didn't use setup.py*:

        python create_db.py
        
13. OPTIONAL: Use the pre-populated SQL data found in sql/hextechprojectx_PREPOPULATED.sql

This contains a fair number of games obtained from running the daemon for a couple of hours. You should be able to load 
it through your favourite MySQL tool - I used Sequel Pro to dump the data.
        
14. OPTIONAL (RECOMMENDED): Start the deamon:

        python src/api_daemon/daemon.py
        
*** TOOD: Add instructions for installing supervisor + getting the daemon running ***

Running Locally
===============

Open a new shell window and run the following from the project base directory:

    gulp

Navigate to `localhost:8000` and the application should be running.

Running Tests
=============

To run both the python and JS tests run:

    ./test.py

