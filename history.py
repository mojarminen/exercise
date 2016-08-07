import sqlite3

DATABASE_FILE = 'fa_stats.db'

conn = sqlite3.connect(DATABASE_FILE)

def get_1X2_history(start=None, end=None):
    c = conn.cursor()
    
    if start and end:
        c.execute('select full_time_home_team_goals, full_time_away_team_goals from matches where "date" > ? and "date" < ?', (start, end))
    elif start:
        c.execute('select full_time_home_team_goals, full_time_away_team_goals from matches where "date" > ?', (start,))
    elif end:
        c.execute('select full_time_home_team_goals, full_time_away_team_goals from matches where "date" < ?', (end,))
    else:
        c.execute('select full_time_home_team_goals, full_time_away_team_goals from matches')
    
    result = c.fetchall()
    print result
    
    number_of_games = len(result)
    mark_1 = 0
    mark_X = 0
    mark_2 = 0
    for row in result:
        if row[0] > row[1]:
            mark_1 += 1
        elif row[0] < row[1]:
            mark_2 += 1
        else:
            mark_X += 1
            
    return (float(mark_1)/number_of_games, float(mark_X)/number_of_games, float(mark_2)/number_of_games)

if __name__ == "__main__":
    print get_1X2_history()
