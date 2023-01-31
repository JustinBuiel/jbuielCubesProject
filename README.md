Justin Buiel

Build Instructions:

make sure either automatically or manually that the requirements are installed
>pip install -r requirements.txt

you may need to include "python -m" for Linux/MacOS or "py -m" for Windows if pip isn't recognized

the last step to get the program working is to create a secret.py file in the directory that has a variable assignment like: 
>wufoo_key = "your api key here"

and replace the url with your own form
___

This project accesses a wufoo form I have created that mimics the current BSU CUBES project form that we will later work on automating.

Form: https://justinb.wufoo.com/forms/cubes-project-proposal-submission/

At the last second (as I was updating this readme) I realized that using a different form as you said you were going to do might not work well with my neatly formatted file so I added a quick and dirty implementation that should be universal.

Also while trying to figure out the secrets thing I exposed my api key inside one of the action runs to try and debug to see why it wasn't working (i still don't know why it didn't work as I had it set up) I reset my key after this.