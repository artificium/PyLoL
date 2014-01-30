This Python library adds an extra layer on top of the traditional wrapped GET requests. It aims to provide automatic resource management. In other words, it will take care of rate-limiting your application and will attempt to optimize the number of queries to retreive data. 

I like to work with code completion when I'm writing my code, so I wrote this library to get objects from the RiotGames developer API (https://developer.riotgames.com/). The purpose of this library is simplicity for the developer, not necessarily efficiency. 

I've defined a class for each object provided by the Riot API, and I've written a client that will make the GET requests and deserialize the incoming JSON directly to these Python classes. That's it. It also automatically rate-limits your queries (if you want) and handles grouping your queries to reduce the number of queries that you're making. 

Take a look at example.py for some well-documented example usages. 

```python
from RiotAPI import pylol

# Create our client for the North American server with rate-limiting enabled and a rate limit
# of 500 queries per ten minutes
riot = pylol.RiotClient("YOUR_API_KEY_HERE", realm = 'na', limit = True, max_per_ten_min = 500)

# Let's assume we have a list of summoner IDs. Let's also assume that 
# this list is longer than 40

summoner_ids = [x for x in range(100)]

# Get a Map[Int, String] of summoner ID -> summoner name
summoner_names = riot.get_summoner_names(summoner_ids)

# Output > { 0 : "Summoner0", 1 : "Summoner1", 2 : "Summoner2", ... , 99 : "Summoner99" }
```

Riot only allows you to make a list query (a query that asks for data on multiple summoners in a single query) with up to 40 summoners. It seems our list has more than 40 summoner IDs. Problem? NOPE. PyLoL takes care of that on the request side. The library will split the list of IDs in to chunks of 40 and make as many queries as necessary*, then compile the results into a single output for you.

*Potentially with a rate limit applied. It's pretty primative, but each query will delay enough so that you don't exceed the specified max queries per ten minutes. You can turn this off if you need/want to. 
