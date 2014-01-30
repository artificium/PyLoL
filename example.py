from RiotAPI import pylol
import pymongo
from RiotAPI.utils import todict

# Some of these examples won't actually work as is. You need data for that. They're mostly for show.

# Create our client
riot = pylol.RiotClient("YOUR_API_KEY_HERE")

# Let's say we have a list of summoner IDs
summoner_ids = [x for x in range(100)]

# Riot only allows you to make a list query (a query that asks for data on multiple summoners in a single
# query) with up to 40 summoners. It seems our list has more than 40 summoner IDs. Problem? NOPE. 
# PyLoL takes care of that on the request side. The library will split the list of IDs in to chunks of 40
# and make as many queries as necessary*, then compile the results into a single output for you

# *Another intersting feature: the library rate-limits itself. It's pretty primative, but each query 
# will delay enough so that you don't exceed the specified max queries per ten minutes. You can turn this off if
# you need/want to. 

# Get a Map[Int, String] of summoner ID -> summoner name
summoner_names = riot.get_summoner_names(summoner_ids)

# Get a list of MasteryListing from these summoner IDs
mastery_listings = riot.get_mastery_pages(summoner_ids)


# Now, let's get a little more complicated. I'm going to assume that I want to 
# query for the mastery pages of a few summoners and store them in MongoDB (http://www.mongodb.org/).
# I'm using the pymongo driver for MongoDB. The whole purpose of this demo is to show
# that I've included a function to convert RiotObjects back into a dict for storing in MongoDB

# One client per region
clients = {
	'eune' : pylol.RiotClient("YOUR_API_KEY_HERE", realm='eune'),
	'euw' : pylol.RiotClient("YOUR_API_KEY_HERE", realm='euw'),
	'na' : pylol.RiotClient("YOUR_API_KEY_HERE", realm='na')
}

# Mongo setup
client = pymongo.mongo_client.MongoClient()
db = client.pylol

# Let's say you have a list of summoner information in the form by realm

summoners = {
	'na' : [5555, 6666, 7777],
	'euw' : [88, 99, 11],
	'eune' : [1111, 2222, 3333]
}

for realm in clients:
	print "Processing realm: %s" % realm
	riot = clients[realm]

	# Get all summoner IDs
	ids = [s for s in summoners[realm]]

	print "Summoner IDs: ", ids

	mastery_listings = riot.get_mastery_pages(ids)
	rune_listings = riot.get_rune_pages(ids)

	print mastery_listings
	print rune_listings

	print "Inserting %d mastery pages..." % len(mastery_listings)
	db.mastery_pages.insert([todict(x) for x in mastery_listings])

