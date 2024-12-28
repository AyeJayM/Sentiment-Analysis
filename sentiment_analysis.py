'''
SentimentAnalysis.py is a script/program created to give a sentiment score on 
tweets from a json file. The files are downloaded from google cloud service(GCS)
General methodology is:
    1. get data
    2. extract column with the tweets as we only need that column to use VADER
    to get a sentiment score
    3. Combine the extracted tweet column and each tweets sentiment score into
    a dataframe
    4. export dataframe as a CSV file
    
NOTE: Script was designed to be on local and the way to get inputs need to be
modified if going to use google colab or similar product
'''
import pandas as pd
from textblob import TextBlob
import os

#Inputs
pathwayInput = "cleaned_masks.csv"

#Putting pathwayInput into quotes allows for it to read with pd.read_json
pathwayInput = "{0}".format(pathwayInput)
pathwayOutput = "{0}_processed".format(pathwayInput)


'''
- variable 'df' is used to read the json file. Currently it assumes the py file is 
in the same directory, or folder, as the json file. lines=True is put in as the 
formatting of google cloud service(GCS) puts spaces(\n).
- variable 'tweets' is used to take only the column that was named 'text' as 
column 'text' contains all the tweets. 
- sentiment array is made to hold all the sentiment scores produced by
the function 'sentiment scores'
- variable 'count' is used to keep track of where tbe script is currently at 
giving a sentiment score.
'''
df = pd.read_csv(pathwayInput)
#df.to_csv('data_csv_tweets_11_3_2022.csv')
tweets = df.pop("text")
id = df.pop("id")
#geo_location = df.pop("geo.full_name")
#geo_bbox = df.pop("geo.geo.bbox")
TEXTBLOBsentimentPolarity = []
count = 0


'''
- for loop is used to iterate through all the tweets. each iteration would get
the sentiment score and then append it to another array. that array 'sentiment'
would be later combined with tweets to create a dataframe that only contains
text and its sentiment score determined by VADER
'''
for text in tweets:    
    TBtext = TextBlob(text)
    polarity = TBtext.sentiment.polarity
    TEXTBLOBsentimentPolarity.append(polarity)
    
    '''
    if (count == [whatever number]) is used to control how much is exported.
    This is commented for now as it is used for experimentation (doing
    initial tests if the script worked)
    '''
    #if (count == 99):
    #    break
    print(count)
    count = count + 1


'''
- variable 'newFileContent' is used to put the tweets and each tweets sentiment
together
- variable 'dataFrame' is used to put newFileContent into a dataframe. We do 
this as to be able to use the pandas package feature of exporting arrays into
whatever data type we need. In this case, into CSV format.
- Currently using 'import os' to be able to make a new folder to put all 
processed files into. Put data into .csv and .xlsx for convenience in future
use. CSV is handy when putting the data into a ML model. .xlsx is handy when
uploading to github. 

NOTE: .xlsx should be only data type to be put into github
as it gives easy access for contributors to download their desired data files.
'''

newFileContent = {'text': tweets, 
                  'TEXTBLOBrawPolarity': TEXTBLOBsentimentPolarity,
                  'id': id}
                  #'geo_location': geo_location,
                  #'geo_bbox': geo_bbox}
dataFrame = pd.DataFrame(data = newFileContent)

os.makedirs("sentimentScoredFiles", exist_ok = True)
pathwayOutputCSV = "sentimentScoredFiles/{0}.csv".format(pathwayOutput)
dataFrame.to_csv(pathwayOutputCSV, index=False)

pathwayOutputEXCEL = "sentimentScoredFiles/{0}.xlsx".format(pathwayOutput)
dataFrame.to_excel(pathwayOutputEXCEL,index = False)



        
