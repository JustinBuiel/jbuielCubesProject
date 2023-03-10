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

The database consists of three (3) tables, one table that holds each entry in a separate row. Each entry gets an auto-incremented integer primary key starting at 1. The answers for what collaboration the respondent is interesting in are either 'yes' for interested or Null for not. Same goes for the timeframe. One table that holds user information with an auto-incremented integer id. And one final table that just holds a reference to the project/entry id and the user id of the user who has claimed that project. Since only one user should claim a project the primary key for this table is both of the ids together.

Once the user runs the program they are asked if they want to update the data or show the visualization. If the database isn't created yet and the user asks for visualization the program will print out an error message and exit. Asking to update the data will also automatically show the data. 

The database is now displayed to the user in a nice GUI built on Qt for python. When you choose to show the data (or update the data) you will be greeted by a window with buttons displaying some information of each entry in the database. 

When you click one of the buttons a new pane in the window will open on the right and show you the full information of the entry. You can then click any of the buttons on the left side to update the right side to show that button's data.

Under the entry information is a new button where the user can claim the project. They are then greeted by a new window where they are prompted to enter their email. If they are an existing user in the database, their information will be automatically populated in the next screen where they are asked to enter more information about them before they can claim the project.

Once the user claims the project the newer window will close and they can click on the project they just claimed to see new information about how they have claimed it and no one else can claim it. 

Form: https://justinb.wufoo.com/forms/cubes-project-proposal-submission/