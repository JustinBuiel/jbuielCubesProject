Justin Buiel

Build Instructions:

make sure either automatically or manually that the requirements are installed
>pip install -r requirements.txt

you may need to include "python -m" for Linux/MacOS or "py -m" for Windows if pip isn't recognized

the last step to get the program working is to create a secrets.py file in the directory that has a variable assignment like: 
>wufoo_key = "yOuR-APi-kEy"

I originally had this as "secret.py" because pylance/autopep8 were mad about the shadowed imports thing but i just ignored it for ease of use/uniformity
___

This project accesses a wufoo form I have created that mimics the current BSU CUBES project form that we will later work on automating. This version now sends the data to a database for better storage and ease of access. 

The database consists of one (1) table that holds each entry in a separate row. Each entry gets an auto-incremented integer primary key starting at 1. The answers for what collaboration the respondent is interesting in are either 'yes' for interested or Null for not. Same goes for the timeframe. 

Form: https://justinb.wufoo.com/forms/cubes-project-proposal-submission/