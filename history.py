import sqlite3

DATABASE_FILE = 'fa_stats.db'

conn = sqlite3.connect(DATABASE_FILE)

def get_common_1X2_history(start="1900-01-01", end="2100-01-01"):
    c = conn.cursor()
    
    c.execute('select full_time_home_team_goals, full_time_away_team_goals from matches where "date" >= ? and "date" <= ?', (start, end))
    
    result = c.fetchall()
    
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


def get_premier_league_1X2_history(start="1900-01-01", end="2100-01-01"):
    c = conn.cursor()

    c.execute('select full_time_home_team_goals, full_time_away_team_goals '
              'from matches '
              'where "date" >= ? and "date" <= ? '
              "and division = 'E0'", (start, end))
    
    result = c.fetchall()
    
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


def get_championship_1X2_history(start="1900-01-01", end="2100-01-01"):
    c = conn.cursor()

    c.execute('select full_time_home_team_goals, full_time_away_team_goals '
              'from matches '
              'where "date" >= ? and "date" <= ? '
              "and division = 'E1'", (start, end))
    
    result = c.fetchall()
    
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


def get_home_game_percentages_of_team(team, start=None, end=None):
    c = conn.cursor()
    
    if start is None:
        start = "1900-01-01"
    if end is None:
        end = "2100-01-01"
    
    c.execute('select full_time_home_team_goals, full_time_away_team_goals '
              'from matches '
              'where home_team like ? '
              'and "date" >= ? '
              'and "date" <= ? ', (team, start, end))

    result = c.fetchall()
    
    number_of_games = len(result)
    number_of_wins = 0
    number_of_draws = 0
    number_of_losses = 0
    for row in result:
        if row[0] > row[1]:
            number_of_wins += 1
        elif row[0] < row[1]:
            number_of_losses += 1
        else:
            number_of_draws += 1
            
    return (float(number_of_wins)/number_of_games, float(number_of_draws)/number_of_games, float(number_of_losses)/number_of_games)

if __name__ == "__main__":
    print 'get_common_1X2_history:', get_common_1X2_history()
    print 'get_premier_league_1X2_history:', get_premier_league_1X2_history()
    print 'get_championship_1X2_history:', get_championship_1X2_history()

    print 'get_home_win_percentage_of_team("Man United"):', get_home_game_percentages_of_team("Man United", end="2015-07-01")
    print 'get_home_win_percentage_of_team("Aston Villa"):', get_home_game_percentages_of_team("Aston Villa", end="2015-07-01")
    print 'get_home_win_percentage_of_team("Hull"):', get_home_game_percentages_of_team("Hull", end="2015-07-01")
    print 'get_home_win_percentage_of_team("Chelsea"):', get_home_game_percentages_of_team("Chelsea", end="2015-07-01")
    print 'get_home_win_percentage_of_team("Liverpool"):', get_home_game_percentages_of_team("Liverpool", end="2015-07-01")
    print 'get_home_win_percentage_of_team("Burnley"):', get_home_game_percentages_of_team("Burnley", end="2015-07-01")
