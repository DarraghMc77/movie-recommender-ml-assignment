# pylint: disable=C0103, C0111
import codecs
from scikits.crab.models import MatrixPreferenceDataModel
import pandas

def parseMovies(movies):
    columnLabels = [y[0] for y in [x.split("|") for x in codecs.open("movielens100k/ml-100k/u.genre").readlines()]]
    columnLabels.pop()
    columnLabels += ["00s", "10s", "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90s"]
    data = []
    for x in movies:
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
            pass
    print(columnLabels)
    dataFrame = pandas.DataFrame.from_records(data, columns=columnLabels)
    return dataFrame

def parseUsers(users):
    occupationLabels = [x.strip('\n') for x in codecs.open("movielens100k/ml-100k/u.occupation", 'r', encoding = "ISO-8859-1").readlines()]
    userLabels = ["age", "male", "female"] + occupationLabels
    print(userLabels)

    data = []

    for x in users:
        occupations = [0 for x in occupationLabels]
        new_user = [int(x[1])]
        if x[2] == 'M':
            new_user += [1,0]
        else:
            new_user += [0,1]
        occupations[occupationLabels.index(x[3])] = 1
        new_user += occupations
        data.append(new_user)

    dataFrame = pandas.DataFrame.from_records(data, columns=userLabels)
    return dataFrame



if __name__ == "__main__":
    try:
        moviefile = [x.split("|") for x in codecs.open("movielens100k/ml-100k/u.item", 'r', encoding = "ISO-8859-1").readlines()]
    except IOError as e:
        print("Can't open file\n")
    
    userfile = [x.split("|") for x in codecs.open("movielens100k/ml-100k/u.user", 'r', encoding = "ISO-8859-1").readlines()]

    usersDataFrame = parseUsers(userfile)
    moviesDataFrame = parseMovies(moviefile)