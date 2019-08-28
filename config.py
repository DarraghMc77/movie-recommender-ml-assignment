#Sizes of dataset chunks to be trained and evaluated
#sizes = [100]
#Uncomment if PC has enough RAM
#sizes = [100,500,1000,5000,10000,50000,100000,500000]
sizes = [100]

#List of tuples(Filename, dict of attributes for that file)
#columnNameRow - the row number with column names in it
#featureColumns - (min,max) pair that represents range of feature columns
#excludeColumns - a list of any columns that should be exlcuded
#
#Any new datasets to be used can be added here
inputFiles = [
                 ("u.item",
                 { 
                     #"filePath":"The SUM dataset/without noise/",
                     "filePath":"",
                     "columnNameRow":0,
                     "targetColumn":11,
                     "featureColumns":(1,11),
                     "targetClassColumn":12,
                     "excludeColumns":[0],
                     "skipFirst":True,
                     "zipped":False}),
            ]
delimiterChar = '|'
#String of delimiters that may be used. Actual delimiter is automatically detected
possibleDelimiters = ',;|'
#Directory which contains input files, described by 'inputFiles' above
#inputDirectory = './Machine Learning Datasets/'
inputDirectory = './'

outputDirectory = './'
outputFile = "TestOutputCSV.csv"

ridgeAlpha = 0.5

debugMode = True
