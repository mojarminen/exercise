import history

def simple_estimation(home, away, end=None):
    home_team = history.get_home_game_percentages_of_team(home, end)
    away_team = history.get_away_game_percentages_of_team(away, end)
    
    return ((home_team[0]+away_team[0])/2, 
            (home_team[1]+away_team[1])/2,
            (home_team[2]+away_team[2])/2)


if __name__ == "__main__":
    home_team = history.get_home_game_percentages_of_team("Bournemouth", end="2015-07-01")
    print home_team

    away_team = history.get_away_game_percentages_of_team("Aston Villa", end="2015-07-01")
    print away_team
    
    print ((home_team[0]+away_team[0])/2, 
           (home_team[1]+away_team[1])/2,
           (home_team[2]+away_team[2])/2)
