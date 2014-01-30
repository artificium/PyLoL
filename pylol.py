import json
import urllib2
import time
import datetime
from utils import splitlist

class RiotObj(object):
	def load(self, json):
		self.__dict__ = json

class Summoner(RiotObj):
	def __init__(self, _id=None, name=None, profileIconId=None, revisionDate=None, summonerLevel=None, json=None):
		if json:
			self.load(json)
		else:
			self.id = _id
			self.name = name
			self.profileIconId = profileIconId
			self.revisionDate = revisionDate
			self.summonerLevel = summonerLevel

	def __str__(self):
		return "Summoner - ID: %d, Name: %s, Level: %d" % (self.id, self.name, self.summonerLevel)

class MasteryListing(RiotObj):
	def __init__(self, summonerId=None, pages=[], date=None, json=None):
		if json:
			self.load(json)
		else:
			self.summonerId = summonerId
			self.pages = pages
			self.date = date

	def load(self, json):
		super(MasteryListing, self).load(json)
		self.pages = [MasteryPage(json=m) for m in self.pages] if hasattr(self, "pages") else []

class MasteryPage(RiotObj):
	def __init__(self, current=None, _id=None, name=None, talents=[], json=None):
		if json:
			self.load(json)
		else:
			self.current = current
			self.id = _id
			self.name = name
			self.talents = talents

	def load(self, json):
		super(MasteryPage, self).load(json)
		self.talents = [Talent(json=t) for t in self.talents] if hasattr(self, "talents") else []

	def __str__(self):
		return "MasteryPage - ID: %d, Name: %s, Current: %s" % (self.id, self.name, "TRUE" if self.current else "FALSE")

class Talent(RiotObj):
	def __init__(self, _id=None, name=None, rank=None, json=None):
		if json:
			self.load(json)
		else:
			self.id = _id
			self.name = name
			self.rank = rank

	def __str__(self):
		return "Talent - ID: %d, Name: %s, Rank: %d" % (self.id, self.name, self.rank)

class RuneListing(RiotObj):
	def __init__(self, summonerId=None, pages=[], date=None, json=None):
		if json:
			self.load(json)
		else:
			self.summonerId = summonerId
			self.pages = pages
			self.date = date

	def load(self, json):
		super(RuneListing, self).load(json)
		self.pages = [RunePage(json=r) for r in self.pages] if hasattr(self, "pages") else []

class RunePage(RiotObj):
	def __init__(self, current=None, _id=None, name=None, slots=[], json=None):
		if json:
			self.load(json)
		else:
			self.current = current
			self.id = _id
			self.name = name
			self.slots = slots

	def load(self, json):
		super(RunePage, self).load(json)
		self.slots = [RuneSlot(json=r) for r in self.slots] if hasattr(self, "slots") else []

	def __str__(self):
		return "RunePage - ID: %d, Name: %s, Current: %s" % (self.id, self.name, "TRUE" if self.current else "FALSE")

class RuneSlot(RiotObj):
	def __init__(self, runeSlotId=None, rune=None, json=None):
		if json:
			self.load(json)
		else:
			self.runeSlotId = runeSlotId
			self.rune = rune

	def load(self, json):
		super(RuneSlot, self).load(json)
		self.rune = Rune(json=self.rune)

class Rune(RiotObj):
	def __init__(self, _id=None, name=None, description=None, tier=None, json=None):
		if json:
			self.load(json)
		else:
			self.id = _id
			self.name = name
			self.description = description
			self.tier = tier

	def __str__(self):
		return "Rune - ID: %d, Name: %s, Description: %s, Tier: %d" % (self.id, self.name, self.description, self.tier)

class RecentGameList(RiotObj):
	def __init__(self, summonerId=None, games=[], json=None):
		if json:
			self.load(json)
		else:
			self.summonerId = summonerId
			self.games = games

	def load(self, json):
		super(RecentGameList, self).load(json)
		self.games = [Game(json=g) for g in self.games] if hasattr(self, 'games') else []

class Game(RiotObj):
	def __init__(self, championId=None, createDate=None, fellowPlayers=[], 
		gameId=None, gameMode=None, gameType=None, invalid=None, level=None, 
		mapId=None, spell1=None, spell2=None, stats=None, subType=None, teamId=None, json=None):
		if json:
			self.load(json)
		else:
			self.championId = championId
			self.createDate = createDate
			self.fellowPlayers = fellowPlayers
			self.gameId = gameId
			self.gameMode = gameMode
			self.gameType = gameType
			self.invalid = invalid
			self.level = level
			self.mapId = mapId
			self.spell1 = spell1
			self.spell2 = spell2
			self.stats = stats
			self.subType = subType

	def load(self, json):
		super(Game, self).load(json)
		self.fellowPlayers = [Player(json=p) for p in self.fellowPlayers] if hasattr(self, 'fellowPlayers') else []
		self.stats = RawStats(json=self.stats)

class Player(RiotObj):
	def __init__(self, championId=None, summonerId=None, teamId=None, json=None):
		if json:
			self.load(json)
		else:
			self.championId = championId
			self.summonerId = summonerId
			self.teamId = teamId

	def __str__(self):
		return "Player - SummonerId: %d, ChampionId: %d, TeamId: %d" % (self.summonerId, self.championId, self.teamId)

# This one is a PitA
class RawStats(RiotObj):
	def __init__(self, assists=None, barracksKilled=None, championsKilled=None, combatPlayerScore=None, consumablesPurchased=None, damageDealtPlayer=None,
		doubleKills=None, firstBlood=None, gold=None, goldEarned=None, goldSpent=None, item0=None, item1=None, item2=None, item3=None, item4=None, item5=None,
		item6=None, itemsPurchased=None, killingSprees=None, largestCriticalStrike=None, largestKillingSpree=None, largestMultiKill=None, legendaryItemsCreated=None,
		level=None, magicDamageDealtPlayer=None, magicDamageDealtToChampions=None, magicDamageTaken=None, minionsDenied=None, minionsKilled=None, 
		neutralMinionsKilled=None, neutralMinionsKilledEnemyJungle=None, neutralMinionsKilledYourJungle=None, nexusKilled=None, nodeCapture=None, nodeCaptureAssist=None,
		nodeNeutralize=None, numDeaths=None, numItemsBought=None, objectivePlayerScore=None, pentaKills=None, physicalDamageDealtPlayer=None, 
		physicalDamageDealtToChampions=None, physicalDamageTaken=None, quadraKills=None, sightWardsBought=None, spell1Cast=None, spell2Cast=None, spell3Cast=None,
		spell4Cast=None, summonSpell1Cast=None, summonSpell2Cast=None, superMonsterKilled=None, team=None, teamObjective=None, timePlayed=None, totalDamageDealt=None,
		totalDamageDealtToChampions=None, totalDamageTaken=None, totalHeal=None, totalPlayerScore=None, totalScoreRank=None, totalTimeCrowdControlDealt=None,
		totalUnitsHealed=None, tripleKills=None, trueDamageDealtPlayer=None, trueDamageDealtToChampions=None, trueDamageTaken=None, turretsKilled=None, 
		unrealKills=None, victoryPointTotal=None, visionWardsBought=None, wardKilled=None, wardPlaced=None, win=None, json=None):
		if json:
			self.load(json)
		else:
			self.assists = assists
			self.barracksKilled = barracksKilled
			self.championsKilled = championsKilled
			self.combatPlayerScore = combatPlayerScore
			self.consumablesPurchased = consumablesPurchased
			self.damageDealtPlayer = damageDealtPlayer
			self.doubleKills = doubleKills
			self.firstBlood = firstBlood
			self.gold = gold
			self.goldEarned = goldEarned
			self.goldSpent = goldSpent
			self.item0 = item0
			self.item1 = item1
			self.item2 = item2 
			self.item3 = item3
			self.item4 = item4
			self.item5 = item5
			self.item6 = item6
			self.itemsPurchased = itemsPurchased
			self.killingSprees = killingSprees
			self.largestCriticalStrike = largestCriticalStrike
			self.largestKillingSpree = largestKillingSpree
			self.largestMultiKill = largestMultiKill
			self.legendaryItemsCreated = legendaryItemsCreated
			self.level = level
			self.magicDamageDealtPlayer = magicDamageDealtPlayer
			self.magicDamageDealtToChampions = magicDamageDealtToChampions
			self.magicDamageTaken = magicDamageTaken
			self.minionsDenied = minionsDenied
			self.minionsKilled = minionsKilled
			self.neutralMinionsKilled = neutralMinionsKilled
			self.neutralMinionsKilledEnemyJungle = neutralMinionsKilledEnemyJungle
			self.neutralMinionsKilledYourJungle = neutralMinionsKilledYourJungle
			self.nexusKilled = nexusKilled
			self.nodeCapture = nodeCapture
			self.nodeCaptureAssist = nodeCaptureAssist
			self.nodeNeutralize = nodeNeutralize
			self.numDeaths = numDeaths
			self.numItemsBought = numItemsBought
			self.objectivePlayerScore = objectivePlayerScore
			self.pentaKills = pentaKills
			self.physicalDamageDealtPlayer = physicalDamageDealtPlayer
			self.physicalDamageDealtToChampions = physicalDamageDealtToChampions
			self.physicalDamageTaken = physicalDamageTaken
			self.quadraKills = quadraKills
			self.sightWardsBought = sightWardsBought
			self.spell1Cast = spell1Cast
			self.spell2Cast = spell2Cast
			self.spell3Cast = spell3Cast
			self.spell4Cast = spell4Cast
			self.summonSpell1Cast = summonSpell1Cast
			self.summonSpell2Cast = summonSpell2Cast
			self.superMonsterKilled = superMonsterKilled
			self.team = team
			self.teamObjective = teamObjective
			self.timePlayed = timePlayed
			self.totalDamageDealt = totalDamageDealt
			self.totalDamageDealtToChampions = totalDamageDealtToChampions
			self.totalDamageTaken = totalDamageTaken
			self.totalHeal = totalHeal
			self.totalPlayerScore = totalPlayerScore
			self.totalScoreRank = totalScoreRank
			self.totalTimeCrowdControlDealt = totalTimeCrowdControlDealt
			self.totalUnitsHealed = totalUnitsHealed
			self.tripleKills = tripleKills
			self.trueDamageDealtPlayer = trueDamageDealtPlayer
			self.trueDamageDealtToChampions = trueDamageDealtToChampions
			self.trueDamageTaken = trueDamageTaken
			self.turretsKilled = turretsKilled
			self.unrealKills = unrealKills
			self.victoryPointTotal = victoryPointTotal
			self.visionWardsBought = visionWardsBought
			self.wardKilled = wardKilled
			self.wardPlaced = wardPlaced
			self.win = win

class ChampionList(RiotObj):
	def __init__(self, champions=[], json=None):
		if json:
			self.load(json)
		else:
			self.champions = champions

	def load(self, json):
		super(ChampionList, self).load(json)
		self.champions = [Champion(json=c) for c in self.champions] if hasattr(self, 'champions') else []

class Champion(RiotObj):
	def __init__(self, active=None, attackRank=None, botEnabled=None, botMmEnabled=None, defenseRank=None, difficultyRank=None, freeToPlay=None,
		_id=None, magicRank=None, name=None, rankedPlayEnabled=None, json=None):
		if json:
			self.load(json)
		else:
			self.active = active
			self.attackRank = attackRank
			self.botEnabled = botEnabled
			self.botMmEnabled = botMmEnabled
			self.defenseRank = defenseRank
			self.difficultyRank = difficultyRank
			self.freeToPlay = freeToPlay
			self.id = _id
			self.magicRank = magicRank
			self.name = name
			self.rankedPlayEnabled = rankedPlayEnabled

class League(RiotObj):
	def __init__(self, entries=[], name=None, participantId=None, queue=None, tier=None, json=None):
		if json:
			self.load(json)
		else:
			self.entries = entries
			self.name = name
			self.participantId = participantId
			self.queue = queue
			self.tier = tier

	def load(self, json):
		super(League, self).load(json)
		self.entries = [LeagueItem(json=l) for l in self.entries] if hasattr(self, 'entries') else []

class LeagueItem(RiotObj):
	def __init__(self, isFreshBlood=None, isHotStreak=None, isInactive=None, isVeteran=None, lastPlayed=None, leagueName=None, leaguePoints=None, miniSeries=None,
		playerOrTeamId=None, playerOrTeamName=None, queueType=None, rank=None, tier=None, wins=None, json=None):
		if json:
			self.load(json)
		else:
			self.isFreshBlood = isFreshBlood
			self.isHotStreak = isHotStreak
			self.isInactive = isInactive
			self.isVeteran = isVeteran
			self.lastPlayed = lastPlayed
			self.leagueName = leagueName
			self.leaguePoints = leaguePoints
			self.miniSeries = miniSeries
			self.playerOrTeamId = playerOrTeamId
			self.playerOrTeamName = playerOrTeamName
			self.queueType = queueType
			self.rank = rank
			self.tier = tier
			self.wins = wins

	def load(self, json):
		super(LeagueItem, self).load(json)
		self.miniSeries = MiniSeries(json=self.miniSeries) if hasattr(self, 'miniSeries') else None

class MiniSeries(RiotObj):
	def __init__(self, losses=None, progress=None, target=None, timeLeftToPlayMillis=None, wins=None, json=None):
		if json:
			self.load(json)
		else:
			self.losses = losses
			self.progress = progress
			self.target = target
			self.timeLeftToPlayMillis = timeLeftToPlayMillis
			self.wins = wins

class PlayerStatsSummaryList(RiotObj):
	def __init__(self, summonerId=None, playerStatSummaries=None, json=None):
		if json:
			self.load(json)
		else:
			self.summonerId = summonerId
			self.playerStatSummaries = playerStatSummaries

	def load(self, json):
		super(PlayerStatsSummaryList, self).load(json)
		self.playerStatSummaries = [PlayerStatsSummary(json=p) for p in self.playerStatSummaries] if hasattr(self, "playerStatSummaries") else []

class PlayerStatsSummary(RiotObj):
	def __init__(self, aggregatedStats=None, losses=None, modifyDate=None, playerStatSummaryType=None, wins=None, json=None):
		if json:
			self.load(json)
		else:
			self.aggregatedStats = aggregatedStats
			self.losses = losses
			self.modifyDate = modifyDate
			self.playerStatSummaryType = playerStatSummaryType
			self.wins = wins

	def load(self, json):
		super(PlayerStatsSummary, self).load(json)
		self.aggregatedStats = AggregatedStats(json=self.aggregatedStats) if hasattr(self, 'aggregatedStats') else None

class RankedStats(RiotObj):
	def __init__(self, champions=[], modifyDate=None, summonerId=None, json=None):
		if json:
			self.load(json)
		else:
			self.champions = champions
			self.modifyDate = modifyDate
			self.summonerId = summonerId

	def load(self, json):
		super(RankedStats, self).load(json)
		self.champions = [ChampionStats(json=c) for c in self.champions] if hasattr(self, 'champions') else None

class ChampionStats(RiotObj):
	def __init__(self, _id=None, name=None, stats=None, json=None):
		if json:
			self.load(json)
		else:
			self.id = _id
			self.name = name
			self.stats = stats

	def load(self, json):
		super(ChampionStats, self).load(json)
		self.stats = AggregatedStats(self.stats) if hasattr(self, 'stats') else None

class AggregatedStats(RiotObj):
	def __init__(self, averageAssists=None, averageChampionsKilled=None, averageCombatPlayerScore=None, averageNodeCapture=None, 
		averageNodeCaptureAssist=None, averageNodeNeutralize=None, averageNodeNeutralizeAssist=None, averageNumDeaths=None, 
		averageObjectivePlayerScore=None, averageTeamObjective=None, averageTotalPlayerScore=None, botGamesPlayed=None, killingSpree=None, 
		maxAssists=None, maxChampionsKilled=None, maxCombatPlayerScore=None, maxLargestCriticalStrike=None, maxLargestKillingSpree=None, 
		maxNodeCapture=None, maxNodeCaptureAssist=None, maxNodeNeutralize=None, maxNodeNeutralizeAssist=None, maxNumDeaths=None, 
		maxObjectivePlayerScore=None, maxTeamObjective=None, maxTimePlayed=None, maxTimeSpentLiving=None, maxTotalPlayerScore=None, 
		mostChampionKillsPerSession=None, mostSpellsCast=None, normalGamesPlayed=None, rankedPremadeGamesPlayed=None, rankedSoloGamesPlayed=None,
		totalAssists=None, totalChampionKills=None, totalDamageDealt=None, totalDamageTaken=None, totalDeathsPerSession=None, totalDoubleKills=None, 
		totalFirstBlood=None, totalGoldEarned=None, totalHeal=None, totalMagicDamageDealt=None, totalMinionKills=None, totalNeutralMinionsKilled=None,
		totalNodeCapture=None, totalNodeNeutralize=None, totalPentaKills=None, totalPhysicalDamageDealt=None, totalQuadraKills=None, totalSessionsLost=None,
		totalSessionsPlayed=None,  totalSessionsWon=None, totalTripleKills=None, totalTurretsKilled=None, totalUnrealKills=None, json=None):

		if json:
			self.load(json)
		else:
			self.averageAssists = averageAssists
			self.averageChampionsKilled = averageChampionsKilled
			self.averageCombatPlayerScore = averageCombatPlayerScore
			self.averageNodeCapture = averageNodeCapture
			self.averageNodeCaptureAssist = averageNodeCaptureAssist
			self.averageNodeNeutralize = averageNodeNeutralize
			self.averageNodeNeutralizeAssist = averageNodeNeutralizeAssist
			self.averageNumDeaths = averageNumDeaths
			self.averageObjectivePlayerScore = averageObjectivePlayerScore
			self.averageTeamObjective = averageTeamObjective
			self.averageTotalPlayerScore = averageTotalPlayerScore
			self.botGamesPlayed = botGamesPlayed
			self.killingSpree = killingSpree
			self.maxAssists = maxAssists
			self.maxChampionsKilled = maxChampionsKilled
			self.maxCombatPlayerScore = maxCombatPlayerScore
			self.maxLargestCriticalStrike = maxLargestCriticalStrike
			self.maxLargestKillingSpree = maxLargestKillingSpree
			self.maxNodeCapture = maxNodeCapture
			self.maxNodeCaptureAssist = maxNodeCaptureAssist
			self.maxNodeNeutralize = maxNodeNeutralize
			self.maxNodeNeutralizeAssist = maxNodeNeutralizeAssist
			self.maxNumDeaths = maxNumDeaths
			self.maxObjectivePlayerScore = maxObjectivePlayerScore
			self.maxTeamObjective = maxTeamObjective
			self.maxTimePlayed = maxTimePlayed
			self.maxTimeSpentLiving = maxTimeSpentLiving
			self.maxTotalPlayerScore = maxTotalPlayerScore
			self.mostChampionKillsPerSession = mostChampionKillsPerSession
			self.mostSpellsCast = mostSpellsCast
			self.normalGamesPlayed = normalGamesPlayed
			self.rankedPremadeGamesPlayed = rankedPremadeGamesPlayed
			self.rankedSoloGamesPlayed = rankedSoloGamesPlayed
			self.totalAssists = totalAssists
			self.totalChampionKills = totalChampionKills
			self.totalDamageDealt = totalDamageDealt
			self.totalDamageTaken = totalDamageTaken
			self.totalDeathsPerSession = totalDeathsPerSession
			self.totalDoubleKills = totalDoubleKills
			self.totalFirstBlood = totalFirstBlood
			self.totalGoldEarned = totalGoldEarned
			self.totalHeal = totalHeal
			self.totalMagicDamageDealt = totalMagicDamageDealt
			self.totalMinionKills = totalMinionKills
			self.totalNeutralMinionsKilled = totalNeutralMinionsKilled
			self.totalNodeCapture = totalNodeCapture
			self.totalNodeNeutralize = totalNodeNeutralize
			self.totalPentaKills = totalPentaKills
			self.totalPhysicalDamageDealt = totalPhysicalDamageDealt
			self.totalQuadraKills = totalQuadraKills
			self.totalSessionsLost = totalSessionsLost
			self.totalSessionsPlayed = totalSessionsPlayed
			self.totalSessionsWon = totalSessionsWon
			self.totalTripleKills = totalTripleKills
			self.totalTurretsKilled = totalTurretsKilled
			self.totalUnrealKills = totalUnrealKills

	def load(self, json):
		super(AggregatedStats, self).load(json)

		# Patch this object because a bunch of the attributes are returned for Dominion only. I don't really like optional
		# API parameters, but alas.
		if not hasattr(self, 'averageAssists'): self.averageAssists = None
		if not hasattr(self, 'averageChampionsKilled'): self.averageChampionsKilled = None
		if not hasattr(self, 'averageCombatPlayerScore'): self.averageCombatPlayerScore = None
		if not hasattr(self, 'averageNodeCapture'): self.averageNodeCapture = None
		if not hasattr(self, 'averageNodeCaptureAssist'): self.averageNodeCaptureAssist = None
		if not hasattr(self, 'averageNodeNeutralize'): self.averageNodeNeutralize = None
		if not hasattr(self, 'averageNodeNeutralizeAssist'): self.averageNodeNeutralizeAssist = None
		if not hasattr(self, 'averageNumDeaths'): self.averageNumDeaths = None
		if not hasattr(self, 'averageObjectivePlayerScore'): self.averageObjectivePlayerScore = None
		if not hasattr(self, 'averageTeamObjective'): self.averageTeamObjective = None
		if not hasattr(self, 'averageTotalPlayerScore'): self.averageTotalPlayerScore = None
		if not hasattr(self, 'maxAssists'): self.maxAssists = None
		if not hasattr(self, 'maxCombatPlayerScore'): self.maxCombatPlayerScore = None
		if not hasattr(self, 'maxNodeCapture'): self.maxNodeCapture = None
		if not hasattr(self, 'maxNodeCaptureAssist'): self.maxNodeCaptureAssist = None
		if not hasattr(self, 'maxNodeNeutralize'): self.maxNodeNeutralize = None
		if not hasattr(self, 'maxNodeNeutralizeAssist'): self.maxNodeNeutralizeAssist = None
		if not hasattr(self, 'maxObjectivePlayerScore'): self.maxObjectivePlayerScore = None
		if not hasattr(self, 'maxTeamObjective'): self.maxTeamObjective = None
		if not hasattr(self, 'maxTotalPlayerScore'): self.maxTotalPlayerScore = None
		if not hasattr(self, 'totalNodeCapture'): self.totalNodeCapture = None
		if not hasattr(self, 'totalNodeNeutralize'): self.totalNodeNeutralize = None

		if not hasattr(self, 'maxNumDeaths'): self.maxNumDeaths = None
		if not hasattr(self, 'totalDeathsPerSession'): self.totalDeathsPerSession = None

class Team(RiotObj):
	def __init__(self, createDate=None, fullId=None, lastGameDate=None, lastJoinDate=None, lastJoinedRankedTeamQueueDate=None,
		matchHistory=None, messageOfDay=None, modifyDate=None, name=None, roster=None, secondLastJoinDate=None, status=None, tag=None,
		teamStatSummary=None, thirdLastJoinDate=None, json=None):
		if json:
			self.load(json)
		else:
			self.createDate = createDate
			self.fullId = fullId
			self.lastGameDate = lastGameDate
			self.lastJoinDate = lastJoinDate
			self.lastJoinedRankedTeamQueueDate = lastJoinedRankedTeamQueueDate
			self.matchHistory = matchHistory
			self.messageOfDay = messageOfDay
			self.modifyDate = modifyDate
			self.name = name
			self.roster = roster
			self.secondLastJoinDate = secondLastJoinDate
			self.status = status
			self.tag = tag
			self.teamStatSummary = teamStatSummary
			self.thirdLastJoinDate = thirdLastJoinDate

	def load(self, json):
		super(Team, self).load(json)
		self.matchHistory = [MatchHistorySummary(json=m) for m in self.matchHistory] if hasattr(self, 'matchHistory') else []
		self.messageOfDay = MessageOfDay(json=self.messageOfDay) if hasattr(self, 'messageOfDay') else None
		self.roster = Roster(json=self.roster) if hasattr(self, 'roster') else None
		self.teamStatSummary = TeamStatSummary(json=self.teamStatSummary) if hasattr(self, 'teamStatSummary') else None

class MatchHistorySummary(RiotObj):
	def __init__(self, assists=None, deaths=None, gameId=None, gameMode=None, invalid=None, kills=None, mapId=None, opposingTeamKills=None,
		opposingTeamName=None, win=None, json=None):
		if json:
			self.load(json)
		else:
			self.assists = assists
			self.deaths = deaths
			self.gameId = gameId
			self.gameMode = gameMode
			self.invalid = invalid
			self.kills = kills
			self.mapId = mapId
			self.opposingTeamKills = opposingTeamKills
			self.opposingTeamName = opposingTeamName
			self.win = win

class MessageOfDay(RiotObj):
	def __init__(self, createDate=None, message=None, version=None, json=None):
		if json:
			self.load(json)
		else:
			self.createDate = createDate
			self.message = message
			self.version = version

class Roster(RiotObj):
	def __init__(self, memberList=None, ownerId=None, json=None):
		if json:
			self.load(json)
		else:
			self.memberList = memberList
			self.ownerId = ownerId

	def load(self, json):
		super(Roster, self).load(json)
		self.memberList = [TeamMemberInfo(json=t) for t in self.memberList] if hasattr(self, 'memberList') else []

class TeamStatSummary(RiotObj):
	def __init__(self, fullId=None, teamStatDetails=None, json=None):
		if json:
			self.load(json)
		else:
			self.fullId = fullId
			self.teamStatDetails = teamStatDetails

	def load(self, json):
		super(TeamStatSummary, self).load(json)
		self.teamStatDetails = [TeamStatDetail(json=t) for t in self.teamStatDetails] if hasattr(self, 'teamStatDetails') else []

class TeamMemberInfo(RiotObj):
	def __init__(self, inviteDate=None, joinDate=None, playerId=None, status=None, json=None):
		if json:
			self.load(json)
		else:
			self.inviteDate = inviteDate
			self.joinDate = joinDate
			self.playerId = playerId
			self.status = status

class TeamStatDetail(RiotObj):
	def __init__(self, averageGamesPlayed=None, fullId=None, losses=None, teamStatType=None, wins=None, json=None):
		if json:
			self.load(json)
		else:
			self.averageGamesPlayed = averageGamesPlayed
			self.fullId = fullId
			self.losses = losses
			self.teamStatType = teamStatType
			self.wins = wins

class RiotClient(object):
	def __init__(self, api_key, realm = 'na', limit=True, max_per_ten_min=500, include_timestamp=True, summonerAPIVersion = "1.3", 
		championAPIVersion = "1.1", gameAPIVersion = "1.3", leagueAPIVersion = "2.3", statsAPIVersion = "1.2", teamAPIVersion = "2.2"):
		self.api_key = api_key
		self.realm = realm.lower()
		self._limit = limit 
		self._max_per_ten_min = max_per_ten_min
		self.include_timestamp = include_timestamp
		self.summonerAPIVersion = summonerAPIVersion
		self.championAPIVersion = championAPIVersion
		self.gameAPIVersion = gameAPIVersion
		self.leagueAPIVersion = leagueAPIVersion
		self.statsAPIVersion = statsAPIVersion
		self.teamAPIVersion = teamAPIVersion

		self._lastCallTime = time.time()
		self._numQueries = 0

	def makeapicallonlist(self, url, lst, version):
		output = {}

		for group in splitlist(lst, 40):
			resp = self.makeapicall(url.replace('{}', ','.join([str(x) for x in group])), version)

			output = dict(output.items() + resp.items())

		return output

	def sleep(self):
		target_delay_time = int(10 * 60 / self._max_per_ten_min)
		remaining_delay_time = target_delay_time - int(time.time() - self._lastCallTime)
		time.sleep(remaining_delay_time)
		self._lastCallTime = time.time()

	def makeapicall(self, remainder, version):
		self.sleep()
		self._numQueries += 1

		url = "http://prod.api.pvp.net/api/lol/" + urllib2.quote(self.realm) + "/v" + urllib2.quote(version + remainder) + '?api_key=' + urllib2.quote(self.api_key)
		print "Calling: %s" % url
		return json.loads(urllib2.urlopen(url).read())

	def get_num_queries(self):
		return self._numQueries

	def list_result(self, json, clazz=None):
		date = datetime.datetime.utcnow()

		output = []
		for raw in json.values():
			if self.include_timestamp:
				raw['date'] = date

			mplist = clazz(json=raw)

			output.append(mplist)

		return output

	def get_mastery_pages(self, id_list):
		resp = self.makeapicallonlist("/summoner/{}/masteries", id_list, self.summonerAPIVersion)

		return self.list_result(resp, MasteryListing)

	def get_rune_pages(self, id_list):
		resp = self.makeapicallonlist("/summoner/{}/runes", id_list, self.summonerAPIVersion)

		return self.list_result(resp, RuneListing)

	def get_summoners_by_ids(self, id_list):
		resp = self.makeapicallonlist("/summoner/{}", id_list, self.summonerAPIVersion)

		return self.list_result(resp, Summoner)

	def get_summoner_names(self, id_list):
		resp = self.makeapicallonlist("/summoner/{}/name", id_list, self.summonerAPIVersion)

		output = {}
		for summoner_id, summoner_name in resp.iteritems():
			output[int(summoner_id)] = summoner_name

		return output

	def get_summoners_by_name(self, names):
		resp = self.makeapicallonlist("/summoner/by-name/{}", names, self.summonerAPIVersion)

		return self.list_result(resp, Summoner)

	def get_champions(self):
		resp = self.makeapicall("/champion", self.championAPIVersion)

		return ChampionList(json=resp)

	def get_recent_games(self, summonerId):
		resp = self.makeapicall("/game/by-summoner/%d/recent" % summonerId, self.gameAPIVersion)

		return RecentGameList(json=resp)

	def get_league(self, summonerId):
		resp = self.makeapicall("/league/by-summoner/%d" % summonerId, self.leagueAPIVersion)

		return [League(json=l) for l in resp]

	def get_stats_summary(self, summonerId):
		resp = self.makeapicall("/stats/by-summoner/%d/summary" % summonerId, self.statsAPIVersion)

		return PlayerStatsSummaryList(json=resp) 

	def get_ranked_stats(self, summonerId):
		resp = self.makeapicall("/stats/by-summoner/%d/ranked" % summonerId, self.statsAPIVersion)

		return RankedStats(json=resp)

	def get_team(self, summonerId):
		resp = self.makeapicall('/team/by-summoner/%d' % summonerId, self.teamAPIVersion)

		return [Team(json=t) for t in resp]

# TODO:

#	Forbidden realms
