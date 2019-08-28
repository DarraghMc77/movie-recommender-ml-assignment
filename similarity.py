import math
from sklearn.metrics.pairwise import cosine_similarity

def userAverageRating(u):
	return sum(u)/float(len(u))

def sim(a,b):
	meanA = userAverageRating(a)
	meanB = userAverageRating(b)
	
	num = 0
	den = 0
	num = reduce(lambda i,j: i+j, [((x-meanA)*(y-meanB)) for x,y in zip(a,b)])

	dom = math.sqrt(reduce(lambda i,j: i+j, [math.pow(x - meanA, 2) for x in a]))
	dom *= math.sqrt(reduce(lambda i,j: i+j, [math.pow(x - meanB,2) for x in b]))
	return num/dom

def pred(user,nn,p):
	meanA = userAverageRating(a)
	meanB = userAverageRating(b)
	meanUser = userAverageRating(user)
	
	print "\n\nPrediction for item %d" % p
	print "Other users:"
	for x in nn:
		print "\t", x

	print "User ratings ", user
	print "User Average: ", meanUser
	num = reduce(lambda i,j: i+j, [sim(user, n) * (n[p] - userAverageRating(n)) for n in nn])
	print "Num: ", num

	den = reduce(lambda i,j: i+j, [sim(user,n) for n in nn])
	print "Den ", den

	pred = meanUser + (num/float(den))
	print "Pred: ", pred

if __name__ == "__main__":
	a = [4,5,1,4,2,2]
	b = [4,5,3,2,1,2]
	c = [3,4,0,3,1,1]
	d = [4,4,4,2,2,6]
	e = [1,2,1,2,1,1]
	
	users = [a,b,c,d,e]

	user = [4,5,2,2,2]

	mostsim = -1
	mostsimlist = []
	for u in users:
		m = sim(u,user)
		print m
		if m > mostsim:
			mostsim = sim(u,user)
			mostsimlist = u
			print "m", mostsimlist
	print mostsim
	print "Most similar list: ", mostsimlist
	print "User: ", user

	print sim(a,b)

	usersAvg = userAverageRating(user)
	#Want to predict value for item 6 for 'user'

	pred(user, users, 5) 

	itemRatings = []
	for x in range(len(a)):
		i = []
		for u in users:
			i.append(u[x])
		itemRatings.append(i)

	cosineSim = 100	
	for x in itemRatings:
		for y in itemRatings:
			s = cosine_similarity([x],[y])[0][0]
	
			print x, y, " Similarity: ", s, " in Degrees:",math.degrees(math.acos(s)) 
		print "\n"



