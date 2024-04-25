import requests
import os
import sqlite3

CLIENT_ID = 'c5f6ef96026b8ec4fcd0f16492040c97'

def get_anime_data(client_id, limit=25):
    headers = {
        'X-MAL-CLIENT-ID': client_id,
    }
    with open('next_url.txt', 'r') as f:
        next_url = f.read().strip()
    response = requests.get(next_url, headers=headers)
    data = response.json()
    with open('next_url.txt', 'w') as f:
        f.write(data['paging'].get('next', ''))
    return data['data']


def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def create_anime_table(cur, conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Anime (
            id INTEGER PRIMARY KEY,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            synopsis TEXT,
            mean REAL,
            rank INTEGER,
            popularity INTEGER,
            num_list_users INTEGER,
            num_scoring_users INTEGER,
            nsfw TEXT,
            created_at TEXT,
            updated_at TEXT,
            media_type TEXT,
            status TEXT,
            num_episodes INTEGER,
            average_episode_duration INTEGER,
            rating TEXT
        )
    ''')
    conn.commit()
    
def create_genre_table(cur, conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Genre (
            id INTEGER PRIMARY KEY,
            genre_name TEXT
        )
    ''')
    conn.commit()
    
    
def create_anime_genre_table(cur, conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS AnimeGenre (
            anime_id INTEGER,
            genre_id INTEGER,
            PRIMARY KEY (anime_id, genre_id),
            FOREIGN KEY (anime_id) REFERENCES Anime (id),
            FOREIGN KEY (genre_id) REFERENCES Genre (id)
        )
    ''')
    conn.commit()

def main():
    cur, conn = set_up_database('project_database.db')
    create_anime_table(cur, conn)
    create_genre_table(cur, conn)
    create_anime_genre_table(cur, conn)
    
    conn.close()

if __name__ == '__main__':
    main()
