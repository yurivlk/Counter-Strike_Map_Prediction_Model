# Counter-Strike_Map_Winner_Prediction_Model

# Project objective

The main goal of this project is based on that try to create a model to predict the winner of a Counter-Strike confront.

# Methods

Web Scrapping

ETL pipeline

Filtering

Machine Learning

Visualization

# Technologies

Python

MYSQL

Pandas

Sklearn

Tableau

# Project Description
 
The size of E sports market size don't stop growing over the past years the data show it to usus. The global Esports market size was estimates at USD 2,008.4 million in 2021 and expected to reach USD 2,566.5 million in 2022. Gambling was always pratical between fans and with E sport is not different, this industry has followed tha growing market and it already took in place between fans. Having it in mind, using my new data analysis skill, I have created an automatic  ETL process to extract data from the biggest Counter-Strike statistical, matches outcomes and shaped a predicti model  using machine learning technologies.
 
# Scraping process

To have a better understanding lets use some images to help us.

Data Source: HLTV.ORG

First Step: Extract match info links from Hltv.org/results.

<>image<>

The outcome of this result is a list with all the matches links.

Second Step: Extract map info detail links from each link grabed on first step.

<>image<>

Third Step: Extract relevant info from each map played in the match.

Here in this page we can find all impact features of the matches.

<> Image <>

Fourth and Final step: Extract economy features from the economy page.

This page was reched with the same link on the step above simply adding the word economy in the URL.

Example:

 <>image<>
 
 # Data Pipeline
 
 The project has followed pipeline assumptions to get and store all this data, down bellow follow schema where we can have a better look how it works.
 
 <>Image<>
 
 Code:
 
 
 The outcome untill now is a Database shaped 1951 rows and 27 columns.
 
 # Data set
 The
 
 The main purpose of this analysis is to identify correlation between features collected and or target variable, which is winner
