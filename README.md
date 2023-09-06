# sqlalchemy-challenge
Module 10 Challenge - SQL Alchemy & API creation
Contributor: Katy Yelle

### Respository Strcuture
    -Main Folder
        -README.md
        -.gitignore
    
    -Sub Folders
        -Resources
            -hawaii.sqlite
            -hawaii_measurements
            -hawaii_stations
        -SurfsUp
            -climate_analysis.ipynb
            -app.py

### Overview
-climate_analysis.ipynb </br>
This jupyter notebook file uses SQLAlchemy to explore climate data for Hawaii.  It conducts a precipitation analysis of the most recent year of daily precipitation data--including a bar chart and a summary statistics table of the data. In order to help get the x-tick formatting how I wanted it I found this resource to be helpful (https://stackoverflow.com/questions/6682784/reducing-number-of-plot-ticks/49714879#49714879). The file also explores the weather data at each of the stations, and takes a more in depth look at the temperature data at the station with the most data observations in the last year of data--including a histogram of temperature frequencies.   

-app.py </br>
This python file creates a Flask API based on the queries from the climate_analysis file.  It includes a homepage that lists all available routes, 3 static routes (one for the precipitation analysis data, one for the weather station list, and one for the temperature analysis data), and 2 dynamic routes (one that calcuates the minimum temperature, average temperature and maximum temperature based on starting date, and one that calculates the minimum temperature, average temperature and maximum temperature based on a given starting date and ending date).  For the dynamic routes, the latest date available in the data set is 2017-08-23, and the earliest date available is 2010-01-01. 
