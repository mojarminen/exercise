import csv
import sqlite3

DATABASE_FILE = 'fa_stats.db'
DB_CONN = sqlite3.connect(DATABASE_FILE)

DATAFILES = (
        'fa_datafiles/2015_2016/E0.csv', 'fa_datafiles/2015_2016/E1.csv',
        'fa_datafiles/2014_2015/E0.csv', 'fa_datafiles/2014_2015/E1.csv',
        'fa_datafiles/2013_2014/E0.csv', 'fa_datafiles/2013_2014/E1.csv',
        'fa_datafiles/2012_2013/E0.csv', 'fa_datafiles/2012_2013/E1.csv',
        'fa_datafiles/2011_2012/E0.csv', 'fa_datafiles/2011_2012/E1.csv',
        'fa_datafiles/2010_2011/E0.csv', 'fa_datafiles/2010_2011/E1.csv',
        'fa_datafiles/2009_2010/E0.csv', 'fa_datafiles/2009_2010/E1.csv',
        'fa_datafiles/2008_2009/E0.csv', 'fa_datafiles/2008_2009/E1.csv',
        'fa_datafiles/2007_2008/E0.csv', 'fa_datafiles/2007_2008/E1.csv',
        'fa_datafiles/2006_2007/E0.csv', 'fa_datafiles/2006_2007/E1.csv',
        'fa_datafiles/2005_2006/E0.csv', 'fa_datafiles/2005_2006/E1.csv',
        'fa_datafiles/2004_2005/E0.csv', 'fa_datafiles/2004_2005/E1.csv',
        'fa_datafiles/2003_2004/E0.csv', 'fa_datafiles/2003_2004/E1.csv',
        'fa_datafiles/2002_2003/E0.csv', 'fa_datafiles/2002_2003/E1.csv',
        'fa_datafiles/2001_2002/E0.csv', 'fa_datafiles/2001_2002/E1.csv',
        'fa_datafiles/2000_2001/E0.csv', 'fa_datafiles/2000_2001/E1.csv',
    )
    
COLUMN_MAPPINGS = {
        'match_stat_columns': {
            'division': 'A', 
            'date': 'B', 
            'home_team': 'C', 
            'away_team': 'D', 
            'full_time_home_team_goals': 'E', 
            'full_time_away_team_goals': 'F', 
            'half_time_home_team_goals': 'H', 
            'half_time_away_team_goals': 'I',
            'referee': 'K',
            'home_team_shots': 'L',
            'away_team_shots': 'M',
            'home_team_shots_on_target': 'N',
            'away_team_shots_on_target': 'O',
            'home_team_hit_woodwork': None,
            'away_team_hit_woodwork': None,
            'home_team_corners': 'R',
            'away_team_corners': 'S',
            'home_team_fouls_committed': 'P',
            'away_team_fouls_committed': 'Q',
            'home_team_offsides': None,
            'away_team_offsides': None,
            'home_team_yellow_cards': 'T',
            'away_team_yellow_cards': 'U',
            'home_team_red_cards': 'V',
            'away_team_red_cards': 'W',
            'home_team_possession': None,
            'away_team_possession': None
        },
        '1X2_odds_columns': {
            'Bet365': {'home_win': 'X', 'draw': 'Y', 'away_win': 'Z'},
            'Bet&Win': {'home_win': 'AA', 'draw': 'AB', 'away_win': 'AC'},
            'Interwetten': {'home_win': 'AD', 'draw': 'AE', 'away_win': 'AF'},
            'Ladbrokes': {'home_win': 'AG', 'draw': 'AH', 'away_win': 'AI'},
            'Pinnacle Sports': {'home_win': 'AJ', 'draw': 'AK', 'away_win': 'AL'},
            'William Hill': {'home_win': 'AM', 'draw': 'AN', 'away_win': 'AO'},
            'VC Bet': {'home_win': 'AP', 'draw': 'AQ', 'away_win': 'AR'},
        }
    }


def alphabets_to_index(alphabets):
    result = None
    alphabets = alphabets.lower()
    
    if (len(alphabets) == 1):
        result = ord(alphabets) - 97
    elif (len(alphabets) == 2):
        # AA = 26, AB = 27, jne.
        result = (ord(alphabets[0]) - 96) * 26
        result += ord(alphabets[1]) - 97
    else:
        raise Exception('unhandled length of alphabets string')
        
    return result


def insert_match_details_to_db(datarow, columns):
    global DB_CONN
    cur = DB_CONN.cursor()
    
    # Parse date to be inserted.
    db_data = {}
    for column in columns:
        if columns[column] is not None:
            db_data[column] = datarow[alphabets_to_index(columns[column])]
            
            if type(db_data[column]) is str:
                db_data[column] = unicode(db_data[column])
            
            if column == "date":
                t = db_data[column].split("/")
                if int(t[2]) < 90:
                    db_data[column] = "20" + t[2] + "-" + t[1] + "-" + t[0]
                else:
                    db_data[column] = "19" + t[2] + "-" + t[1] + "-" + t[0]
        else:
            db_data[column] = None
    
    # Insert to db.
    cur.execute(
        "INSERT INTO matches ("
        "  division, date, home_team, away_team, full_time_home_team_goals, full_time_away_team_goals, half_time_home_team_goals, half_time_away_team_goals, referee, home_team_shots, "
        "  away_team_shots, home_team_shots_on_target, away_team_shots_on_target, home_team_hit_woodwork, away_team_hit_woodwork, home_team_corners, away_team_corners, home_team_fouls_committed, "
        "  away_team_fouls_committed, home_team_offsides, away_team_offsides, home_team_yellow_cards, away_team_yellow_cards, home_team_red_cards, away_team_red_cards, home_team_possession, "
        "  away_team_possession"
        ") VALUES ("
        "  :division, :date, :home_team, :away_team, :full_time_home_team_goals, :full_time_away_team_goals, :half_time_home_team_goals, :half_time_away_team_goals, :referee, :home_team_shots, "
        "  :away_team_shots, :home_team_shots_on_target, :away_team_shots_on_target, :home_team_hit_woodwork, :away_team_hit_woodwork, :home_team_corners, :away_team_corners, :home_team_fouls_committed, "
        "  :away_team_fouls_committed, :home_team_offsides, :away_team_offsides, :home_team_yellow_cards, :away_team_yellow_cards, :home_team_red_cards, :away_team_red_cards, :home_team_possession, "
        "  :away_team_possession"
        ")", 
        db_data
    )
    
    # Check and return the id for the inserted match.
    
    if not cur.lastrowid:
        raise Exception("cur.lastrowid = " + str(cur.lastrowid))
    
    return cur.lastrowid


def insert_1X2_odds_to_db(matchid, datarow, bookers):
    global DB_CONN
    cur = DB_CONN.cursor()

    for booker in bookers:
        home_win = datarow[alphabets_to_index(bookers[booker]['home_win'])]
        draw = datarow[alphabets_to_index(bookers[booker]['draw'])]
        away_win = datarow[alphabets_to_index(bookers[booker]['away_win'])]
        
        if home_win and draw and away_win:
            cur.execute(
                "INSERT INTO odds_1X2 (match, booker, home_win, draw, away_win) "
                "VALUES (:match, :booker, :home_win, :draw, :away_win)", 
                {"match": matchid, "booker": booker, "home_win": home_win, "draw": draw, "away_win": away_win}
            )
    


def populate():
    global DB_CONN

    for filename in DATAFILES:
        print 'importing', filename, "..."
        with open(filename, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for idx, row in enumerate(csvreader):
                # skip the heading row
                if idx == 0:
                    continue
                
                # insert match details to database
                matchid = insert_match_details_to_db(row, COLUMN_MAPPINGS['match_stat_columns'])
                
                # insert 1X2 match odds to database
                insert_1X2_odds_to_db(matchid, row, COLUMN_MAPPINGS['1X2_odds_columns'])

    DB_CONN.commit()
    


if __name__ == '__main__':
    assert alphabets_to_index('A') == 0
    assert alphabets_to_index('a') == 0
    assert alphabets_to_index('AA') == 26
    assert alphabets_to_index('aa') == 26
    assert alphabets_to_index('B') == 1
    assert alphabets_to_index('b') == 1
    assert alphabets_to_index('AB') == 27
    assert alphabets_to_index('ab') == 27
    assert alphabets_to_index('ba') == 52
    
    populate()
