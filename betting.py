import estimator
import sqlite3

DATABASE_FILE = 'fa_stats.db'

conn = sqlite3.connect(DATABASE_FILE)

cur = conn.cursor()

SEASON_START = '2015-08-01'
SEASON_END = '2016-06-01'
DIVISION = 'E1'

cur.execute('SELECT id, home_team, away_team, full_time_home_team_goals, full_time_away_team_goals '
            'FROM matches '
            "WHERE division = ? "
            'AND date > ? '
            'AND date < ?', (DIVISION, SEASON_START, SEASON_END))

matches = cur.fetchall()

money = 1000

for match in matches:
    matchid = match[0]
    home_team = match[1]
    away_team = match[2]
    home_team_goals = match[3]
    away_team_goals = match[4]
    
#    print match
    
    # Get probability estimations and calculate odds.
    probabilities = estimator.simple_estimation(home_team, away_team, end=SEASON_START)
    odds = (1/probabilities[0], 1/probabilities[1], 1/probabilities[2])
#    print 'probabilities:', probabilities
#    print 'odds:', odds
    
    # Get booker odds.
    cur.execute('SELECT home_win, draw, away_win '
                'FROM odds_1X2 '
                'WHERE match = ?', (matchid,))
    booker_odds = [0,0,0]
    result = cur.fetchall()
    for row in result:
        booker_odds[0] = max(row[0], booker_odds[0])
        booker_odds[1] = max(row[1], booker_odds[1])
        booker_odds[2] = max(row[2], booker_odds[2])
            
#    print booker_odds
    
    # Decide what should be played.
    
    stake_1 = 0
    stake_X = 0
    stake_2 = 0
    
    if booker_odds[0] > odds[0]:
        stake_1 = 1
        money -= 1
    if booker_odds[1] > odds[1]:
        stake_X = 1
        money -= 1
    if booker_odds[2] > odds[2]:
        stake_2 = 1
        money -= 1

    # Collect!
    if home_team_goals > away_team_goals and stake_1:
        money += booker_odds[0] * stake_1
        print "WIN", booker_odds[0] * stake_1 - stake_1 - stake_X - stake_2
    elif home_team_goals < away_team_goals and stake_2: 
        money += booker_odds[2] * stake_2
        print "WIN", booker_odds[2] * stake_2 - stake_1 - stake_X - stake_2
    elif stake_X:
        money += booker_odds[1] * stake_X
        print "WIN", booker_odds[1] * stake_X - stake_1 - stake_X - stake_2
    else:
        print "LOSS", -1 * (stake_1 + stake_X + stake_2)

print money
