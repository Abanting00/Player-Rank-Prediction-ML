import requests, json, csv
import numpy as np
import time

API_BASE = "https://na1.api.riotgames.com/lol/"

API_KEY_LIST = ["api_key=RGAPI-448512cc-baf3-4ac7-a502-61372f42de4c",
				"api_key=RGAPI-3b5a3728-6b95-4b8f-ad7b-5382d169420b",
				"api_key=RGAPI-e6c61b92-5faa-4950-b95a-51347690296c",
				"api_key=RGAPI-c33144c8-5f64-47f0-9d1d-43705a5e2882",
				"api_key=RGAPI-e678ed15-209c-45f9-9016-42989f241b2d",
				"api_key=RGAPI-7337a406-6590-477d-abd0-60fb9b997f12",
				"api_key=RGAPI-3ef9f829-2030-4a34-9d18-e4bfacb250ae"
]

# Request Urls from League of Legends API
GET_SUMMONER_ACCOUNT_ID = API_BASE + "summoner/v3/summoners/by-name/"
GET_SUMMONER_ID = API_BASE + "summoner/v3/summoners/by-account/"
GET_MATCHLIST = API_BASE + "match/v3/matchlists/by-account/"
GET_MATCH_INFO = API_BASE + "match/v3/matches/"
GET_LEAGUE_ID = API_BASE + "league/v3/positions/by-summoner/"
GET_LEAGUE_ACCOUNTS = API_BASE + "league/v3/leagues/"

# Seed of each division, this is one account id that belongs to their current division
BRONZE_SEED = 214247653
SILVER_SEED = 230257577
GOLD_SEED = 213728893
PLATINUM_SEED = 200900994
DIAMOND_SEED = 36799985

# Dictionary of Account ID for each Division should only have size of 1100
BRONZE_ACCOUNTS = [BRONZE_SEED]
SILVER_ACCOUNTS = [SILVER_SEED]
GOLD_ACCOUNTS = [GOLD_SEED]
PLATINUM_ACCOUNTS = [PLATINUM_SEED]
DIAMOND_ACCOUNTS = [DIAMOND_SEED]

# Unchecked division Account ID's 
ACCOUNTS = []
ACCOUNT_LIMIT = 1000

# Dictionary for each Players statistic/features
BRONZE_STATS = []
SILVER_STATS = []
GOLD_STATS = []
PLATINUM_STATS = []
DIAMOND_STATS = []

# Feature Lists
avg_stats = {
	'kills': 0,
	'deaths': 0,
	'assists': 0,
	'longestTimeSpentLiving': 0,
	'totalDamageDealtToChampions': 0,
	'visionScore': 0,
}

STATS = [
	'kills',
	'deaths',
	'assists',
	'longestTimeSpentLiving',
	'totalDamageDealtToChampions',
	'visionScore',
]

features_name = [
	'kills',
	'deaths',
	'assists',
	'longestTimeSpentLiving',
	'totalDamageDealtToChampions',
	'visionScore',
	'gold/min',
	'cs/min',
	'wins/lose',
]

LEAGUE_STATS = [
	'wins',
	'losses',
]

# Division Lists
DIVISIONS = [
	'BRONZE',
	'SILVER',
	'GOLD',
	'PLATINUM',
	'DIAMOND'
]

OUTPUTFILES = [
	'bronze.csv',
	'silver.csv',
	'gold.csv',
	'platinum.csv',
	'diamond.csv'
]

# Global to iterate to the api_keys
current_key = 0

# Requests League Accounts

def key_help(status):
	global current_key
	if status != 200:
		if status == 429:
			if current_key == len(API_KEY_LIST) - 1:
				time.sleep(2)
				current_key = 0
			else:
				current_key += 1


# Get Current Accounts MatchList
def get_player_matchlist(accountid, accountDivision, divisionStats):
	r = requests.get(GET_MATCHLIST + str(accountid) + "?" + API_KEY_LIST[current_key])
	data = json.loads(r.text)

	if r.status_code != 200:
		key_help(r.status_code)
		return
	

	matches = []

	for match in data['matches']:
		if len(matches) >= 10:
			break
		if match['queue'] == 420:
			matches.append(match['gameId'])

	if len(matches) == 10:

		firstMatch = True
		gameTime = 0
		minionKilled = 0
		goldEarned = 0

		for matchid in matches:
			r = requests.get(GET_MATCH_INFO + str(matchid) + "?" + API_KEY_LIST[current_key])
			data = json.loads(r.text)

			if r.status_code != 200:
				key_help(r.status_code)
				return

			participant_id = 0
			
			for participant in data['participantIdentities']:
				curr_id = participant['player']['accountId']
				
				if curr_id == accountid:
					participant_id = participant['participantId']

				else:															# Add account to current division if its not full or in
					accountDivision.append(curr_id) 							# Sets key as account id and value to len of account

			for participant in data['participants']:
				if participant['participantId'] == participant_id:
					if firstMatch:
						for stat in STATS:
							avg_stats[stat] = participant['stats'][stat]
						firstMatch = False
					else:
						for stat in STATS:
							avg_stats[stat] += participant['stats'][stat]

					gameTime += data['gameDuration']
					goldEarned += participant['stats']['goldEarned']
					minionKilled += participant['stats']['neutralMinionsKilled']
					minionKilled += participant['stats']['totalMinionsKilled']

		fin_stats = []
		for avg_stat in avg_stats:
			fin_stats.append(avg_stats[avg_stat]/10)

		fin_stats.append((goldEarned/10)/((gameTime/60)/10))
		fin_stats.append((minionKilled)/10/((gameTime/60)/10))
		divisionStats.append(fin_stats)

		ACCOUNTS.append(accountid) 


def checkDivision(accountid, division):
	r = requests.get(GET_SUMMONER_ID + str(accountid) + "?" + API_KEY_LIST[current_key])
	data = json.loads(r.text)

	if r.status_code != 200:
		key_help(r.status_code)
		return False

	summoner_id = data['id']
	r = requests.get(GET_LEAGUE_ID + str(summoner_id) + "?" + API_KEY_LIST[current_key])
	data = json.loads(r.text)

	if r.status_code != 200:
		key_help(r.status_code)
		return False

	for league in data:
		if league['queueType'] == "RANKED_SOLO_5x5" and league['tier'] == division:
			return [league['wins'],league['losses']]									# maybe add streaks

	return False



def getPlayerStats(DIVISION, DIV_STATS, DIV_ACC, DIV_CSV):
	with open(DIV_CSV, 'w') as outfile:
		csvwriter = csv.writer(outfile)
		csvwriter.writerow(features_name)

		count = 0
		stat_count = 0
		while len(DIV_STATS) < ACCOUNT_LIMIT:
			if len(DIV_ACC) - 1 < count:
				break

			acc_id = DIV_ACC[count]

			if acc_id not in ACCOUNTS:

				# Check if account belongs in the correct division
				acc_info = checkDivision(acc_id, DIVISION)

				if acc_info != False:
					get_player_matchlist(acc_id, DIV_ACC, DIV_STATS)
					if stat_count != len(DIV_STATS):
						DIV_STATS[stat_count].append(acc_info[0]/(acc_info[0] + acc_info[1]))
						csvwriter.writerow(DIV_STATS[stat_count])
						stat_count += 1

			print(DIVISION,": ", len(DIV_STATS))
			count += 1

def main():
	# Get Stats from Bronze Players 
	getPlayerStats(DIVISIONS[0], BRONZE_STATS, BRONZE_ACCOUNTS, OUTPUTFILES[0])

	# Get Stats from Silver Players 
	getPlayerStats(DIVISIONS[1], SILVER_STATS, SILVER_ACCOUNTS, OUTPUTFILES[1])

	# # Get Stats from Gold Players
	getPlayerStats(DIVISIONS[2], GOLD_STATS, GOLD_ACCOUNTS, OUTPUTFILES[2])

	# # Get Stats from Platinum Players
	getPlayerStats(DIVISIONS[3], PLATINUM_STATS, PLATINUM_ACCOUNTS, OUTPUTFILES[3])

	# # Get Stats from Diamond Players
	getPlayerStats(DIVISIONS[4], DIAMOND_STATS, DIAMOND_ACCOUNTS, OUTPUTFILES[4])

main()