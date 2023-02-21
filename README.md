Justin Buiel

Build Instructions:

make sure either automatically or manually that the requirements are installed
>pip install -r requirements.txt

you may need to include "python -m" for Linux/MacOS or "py -m" for Windows if pip isn't recognized

the last step to get the program working is to create a secrets.py file in the directory that has a variable assignment like: 
>wufoo_key = "yOuR-APi-kEy"

I originally had this as "secret.py" because pylance/autopep8 were mad about the shadowed imports thing but i just ignored it for ease of use/uniformity


running automated testing by entering
>pytest -v

will run a suite of tests that make sure we get the proper amount of responses from the api and that a new testing database is able to be created and have data added to a table. It will also test to see if the gui displays the right data according to the current state of the test table in the testing database. 
___

This project accesses a wufoo form I have created that mimics the current BSU CUBES project form that we will later work on automating. This version now sends the data to a database for better storage and ease of access. 

The database consists of one (1) table that holds each entry in a separate row. Each entry gets an auto-incremented integer primary key starting at 1. The answers for what collaboration the respondent is interesting in are either 'yes' for interested or Null for not. Same goes for the timeframe. 

The database is now displayed to the user in a nice GUI built on Qt for python. When you run main.py and give it time to let the database get populated you will be greeted by a window with buttons displaying some information of each entry in the database. 

When you click one of the buttons a new pane in the window will open on the right and show you the full information of the entry. You can then click any of the buttons on the left side to update the right side to show that button's data.

Form: https://justinb.wufoo.com/forms/cubes-project-proposal-submission/