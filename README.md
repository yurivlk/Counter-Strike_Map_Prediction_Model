# Counter-Strike_Match_Prediction_Model
 
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
