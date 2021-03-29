Google Calendar Automation
==========================

A program that color-codes tasks and assignments according to their priority

Overview
--------

This program uses the Google Calendar API to read and modify events on Google Calendar. Once one creates an `event` with a special name format, this program will update its color automatically to reflect its level of priority. It is ment to facilitate time management when many assignments of different lengths and levels of completion are due for different dates.

Requirements
------------

* Python 3

Setup
-----

Install all requried dependencies using the following command:
```shell
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

First Event
-----------

Follow the steps below to create your first dynamically-color-coded event:

1. Grant this program access to your Google Calendar account by clicking the *Enable the Google Calendar API* button on [this webpage](https://developers.google.com/calendar/quickstart/js).
2. Download the `credentials.json` file from the page mentionned above and copy it under `Google Calendar Automation/`.
3. Run the python script using the following command: `python run.py`. Note that this program must run continuously in order to update your calendar events dynamically.
4. Open up [Google Calendar](https://calendar.google.com/calendar/u/0/r) and create a new event with the same Google account as used in step 1. As an example, name the event *Google Automation %25* and make sure it spans more than one day.
5. Refresh the calendar manually or wait for it to to so by itself. If everything worked correctly, the event should now be displayed in a custom color.

Usage
-----

Once the program functions correctly, it can be used to change the color of tasks according to their priority:

* This priority is calculated using the following formula: `priority = atan2(1 - event progress, 1 - duration progress) * 2 / pi`, meaning that events whose due date is closer or events that have a small progress percentage will be colored as more important.
* The colors used range from purple to blue to yellow to red, in increasing order of priority. For example, a red-colored event is your prime concern whereas a blue-colored one is not very urgent.
* All events modified by the program must match the following regular expression: `/(\d*)\%(\d+)$/`. This means that all events must end with a string like `t%d`, where `d/t` represents the current progress of the task. For example, if an event is ment to represent a math assignment where you have solved 15 out of 34 problems, its name would need to be something like the following: `Math Homework 34%15`.
* When progress is made on a task, its name must be updated to reflect the current progress. For example, if you just solved 3 more math problems, the name of the event must be updated to `Math Homework 34%18`, representing that 18 problems out of 34 have now been solved. You must constantly update the event names for the color-coding to work properly. When this assignment is completed, its name should be modified to `Math Homework 34%34`, meaning that 34 out of the 34 problems have been solved.
