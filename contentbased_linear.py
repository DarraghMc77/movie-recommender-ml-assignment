# pylint: disable=C0103, C0111
import codecs
#from scikits.crab.models import MatrixPreferenceDataModel
import pandas
from collections import defaultdict
import random

def parseMovies(movies):
    columnLabels = [y[0] for y in [x.split("|") for x in codecs.open("movielens100k/ml-100k/u.genre").readlines()]]
    columnLabels.pop()
    columnLabels += ["00s", "10s", "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90s"]
    data = []
    for c,x in enumerate(movies):
        decades = [0 for x in range(10)]
        del(x[0:2], x[1:3])
        x[19] = x[19].strip('\n')
        year = x.pop(0)
        try:
            decade = int((int(year[-4:])%1900)/10)%10
            decades[decade] = 1
            x += decades
            x = [int(y) for y in x]
            data.append(x)
        except ValueError:
            print("ValueError movies")
            data.append(x)
    #print(columnLabels)
    dataFrame = pandas.DataFrame.from_records(data, columns=columnLabels)
    return dataFrame

def parseUsers(users):
    occupationLabels = [x.strip('\n') for x in codecs.open("movielens100k/ml-100k/u.occupation", 'r', encoding = "ISO-8859-1").readlines()]

    #agelabels = ["10s", "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90s"]

    userLabels = ["age", "male", "female"] + occupationLabels
    #userLabels = agelabels + ["male", "female"] + occupationLabels

    data = []
    for x in users:
        #ages = [0 for x in agelabels] 
        occupations = [0 for x in occupationLabels]
        new_user = [int(x[1])]
        #ages[int(x[1][0])-1] = 1
        #new_user = ages
       
        if x[2] == 'M':
            new_user += [1,0]
            #new_user += [1]
        else:
            new_user += [0,1]
            #new_user += [0]
        occupations[occupationLabels.index(x[3])] = 1
        new_user += occupations
        data.append(new_user)

    dataFrame = pandas.DataFrame.from_records(data, columns=userLabels)
    return dataFrame

def printUserStats(usersDataFrame, genreaverages, ratings):
    mt=0
    mr=0
    mg=[0]*19
    fg=[0]*19
    ft=0
    fr=0
    for x in ratings:
        userd = usersDataFrame.ix[x[0]-1].tolist()
        if userd[1] == 1:
            mt += 1
            mr += x[2]
            mg = [a+b for (a,b) in zip(mg, genreaverages[x[0]])]
        elif userd[2] == 1:
            ft += 1
            fr += x[2]
            fg = [a+b for (a,b) in zip(fg, genreaverages[x[0]])]
    print("User stats\nNumber males:" + str(mt) + "\nNumber females:" + str(ft) + "\nAverage Male rating:" + str(float(mr)/mt) + "\nAverage Female rating:" + str(float(fr)/ft))
    print("Male genre averages: ")
    print([x/mt for x in mg])
    print("Female genre averages: ")
    print([x/ft for x in fg])


def init():
    try:
        moviefile = [x.split("|") for x in codecs.open("movielens100k/ml-100k/u.item", 'r', encoding = "ISO-8859-1").readlines()]
    except IOError as e:
        print("Can't open file\n")
    
    userfile = [x.split("|") for x in codecs.open("movielens100k/ml-100k/u.user", 'r', encoding = "ISO-8859-1").readlines()]

    ratings = [[int(y) for y in z] for z in [x.strip().split("\t") for x in open("movielens100k/ml-100k/u.data").readlines()]]
    moviedict = defaultdict(list)
    userdict = defaultdict(list)

    for x in moviefile:
        movieid = int(x[0])
        moviedict[movieid].append(x)
    for x in userfile:
        userid = int(x[0])
        userdict[userid].append(x)

    moviedict = defaultdict(list)
    userdict = defaultdict(list)

    usersDataFrame = parseUsers(userfile)
    moviesDataFrame = parseMovies(moviefile)

    for x in ratings:
        movieid = int(x[1])
        moviedict[movieid].append(x)
    #    print(moviesDataFrame.ix[movieid])
    for x in ratings:
        userid = int(x[0])
        userdict[userid].append(x)

    avgmovieratings = defaultdict(int)
    # a dict {movieid: [items]} (i.e. userid, movieid, rating, timestamp)
    for x in moviedict.keys():
        r = [y[2] for y in moviedict[x]]
        avgmovieratings[x] = float(sum(r))/len(r)

    avguserratings = defaultdict(int)
    # a dict {user: [items]} (i.e. userid, movieid, rating, timestamp)
    for x in userdict.keys():
        r = [y[2] for y in userdict[x]]
        avguserratings[x] = float(sum(r))/len(r)

# Gets the average rating for every genre for each user, and saves it in dict avegusergenreratings[user id]
    avgusergenreratings = defaultdict(list)
    for x in userdict.keys():
        usersgenreratings = [0] * 19
        numusergenreratings = [0] * 19 

        # for each movie rated by userdict[x]
        for y in userdict[x]:
            moviegenre = [int(a) for a in moviesDataFrame.ix[y[1]-1].tolist()[0:19]] #get genres of rated movie
            numusergenreratings = [a+b for (a,b) in zip(moviegenre, numusergenreratings)]
            moviegenre = [z*y[2] for z in moviegenre] 
            usersgenreratings = [a+b for (a,b) in zip(moviegenre, usersgenreratings)]
        usersavgratings = [float(a)/b if b != 0 else 0 for (a,b) in zip(usersgenreratings, numusergenreratings)]
        avgusergenreratings[x] = usersavgratings

    userlabels = list(usersDataFrame.columns.values)
    movielabels = list(moviesDataFrame.columns.values)

    datalabels = userlabels + movielabels + ["avguserrating","avgmovierating","avggenrerating","rating"]
    #printUserStats(usersDataFrame, avgusergenreratings, ratings)

    random.seed()
    data = []
    for rating in ratings:
        # For the current rating of movie A by user X, get the genre of movie A -> moviegenre e.g. if movie is action and comedy [1,0,0,0,0,1,0,0,0,0] 
        #                                              get user X's average rating for every genre
        #                                              get the dot product of the above, and divide by number of genres of movie A
        # This will give a combined average score out of 5, by the user, for the combination of genres of movie A
        # e.g. if User A rated comedies, actions and dramas (4,5,2) on average, then an action comedy has a combined rating of (4+5)/2
        #      and an action/drama has a combined rating of (5+2)/2 
        # Added as feature 'avggenrating'
        moviegenre = [int(a) for a in moviesDataFrame.ix[rating[1]-1].tolist()[0:19]] #get genres of rated movie
        genres_dot_avguserrating = [x*y for (x,y) in zip(moviegenre, avgusergenreratings[rating[0]])]
        combinedgenrescore = sum(genres_dot_avguserrating)/moviegenre.count(1)

        data.append(usersDataFrame.ix[rating[0]-1].tolist() + moviesDataFrame.ix[rating[1]-1].tolist() + [float(avguserratings[rating[0]])/5] + [float(avgmovieratings[rating[1]])/5] + [combinedgenrescore/5] + [float(rating[2]/5)])

    dataFrame = pandas.DataFrame.from_records(data[0:100000], columns = datalabels)

    return dataFrame

if __name__ == "__main__":
    init()
