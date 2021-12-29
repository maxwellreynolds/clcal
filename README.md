# terminalcal
Show your google calendar events in the command line (including Zoom links from the event description)

Optional arguments  
-d: maximum number of days ahead to check (0 checks until end of today, 1 until end of tomorrow, etc.)  
-e: maximum events to show (default 10)


![sample](img/sample.png)


On Mac: (Cmd + DoubleClick) to open Zoom link from terminal



## Installation

1. 
```
git clone https://github.com/maxwellreynolds/terminalcal/
```

2.
```
pip install -r requirements.txt
```

3. Follow oauth client id credentials steps 1-3 for "Web App" here. https://developers.google.com/workspace/guides/create-credentials?authuser=3#web-application.

In the Google Cloud Platform "Create OAuth Client ID" step, select Desktop App 

Create name for project (any name should work)

Select "Download JSON", and download credentials as "credentials.json" in the same directory as this repository.

4. 
```
python clcal.py
```
(will be an authorization step the first time running)
Note: if you only want to give the app read priveleges (i.e. cannot create events, just shows them; change the line in clcal.py from 
```
SCOPES = ['https://www.googleapis.com/auth/calendar']
```
to 
```
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
```


5. for easy access make an alias

On Mac:

- nano ~/.bash_profile (or vi ~/.bash_profile)
- In the bash profile add the line:

alias gcal = python <path/to/clcal.py>  
(restart terminal for alias to take effect)



Now simply type "gcal" into terminal to list your next events

