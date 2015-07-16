Installation
============

1. Install Python:
    * Using brew: `brew install python`
    * From the website: https://www.python.org/downloads/mac-osx/

2. Install pip to manage Python packages:

        brew install pip

3. Install MySQL:

        *** TODO ***

4. Install virtualenv to deal with all of our dependencies:

        pip install virtualenv

5. Activate the virtualenv so any setup is installed in the virtual environment:
    
        source env/bin/activate

6. Install nodejs (& npm) from https://nodejs.org/.

7. Install bower:

        npm install -g bower

8. Install gulp:

        npm install -g gulp

9. Install all dependencies:

        pip install -r requirements.txt
        npm install
        bower install

10. (Optional) Install the python project:

        python setup.py install

11. Create the database *if you didn't use setup.py*:

        python create_db.py
        
        
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

