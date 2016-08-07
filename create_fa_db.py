import sqlite3

DATABASE_FILE = 'fa_stats.db'

def create_table():
	conn = sqlite3.connect(DATABASE_FILE)
	c = conn.cursor()

	c.execute('''
		CREATE TABLE matches (
			id integer,
			division text, 
			date timestamp, 
			home_team text, 
			away_team text, 
			full_time_home_team_goals integer,
			full_time_away_team_goals integer,
			half_time_home_team_goals integer,
			half_time_away_team_goals integer,
			referee text,
			home_team_shots integer,
			away_team_shots integer,
			home_team_shots_on_target integer,
			away_team_shots_on_target integer,
			home_team_hit_woodwork integer,
			away_team_hit_woodwork integer,
			home_team_corners integer,
			away_team_corners integer,
			home_team_fouls_committed integer,
			away_team_fouls_committed integer,
			home_team_offsides integer,
			away_team_offsides integer,
			home_team_yellow_cards integer,
			away_team_yellow_cards integer,
			home_team_red_cards integer,
			away_team_red_cards integer,
            home_team_possession real,
            away_team_possession real,
            home_team_touches integer,
            away_team_touches integer,
            home_team_passes integer,
            away_team_passes integer,
            home_team_tackles integer,
            away_team_tackles integer,
            home_team_clearances integer,
            away_team_clearances integer,
			PRIMARY KEY (id),
            UNIQUE (date, home_team, away_team)
		)''')
		
	c.execute('''
		CREATE TABLE odds_1X2
		(
			id integer,
			match integer,
			booker text,
			home_win real,
			draw real,
			away_win real,
			PRIMARY KEY (id),
			FOREIGN KEY (match) REFERENCES matches(id)
		)''')

	c.execute('''
		CREATE TABLE odds_over_under
		(
			id serial,
			match integer,
			booker text,
            border_value real,
			under real,
			over real,
			PRIMARY KEY (id),
			FOREIGN KEY (match) REFERENCES matches(id)
		)''')

if __name__ == "__main__":
	create_table()
