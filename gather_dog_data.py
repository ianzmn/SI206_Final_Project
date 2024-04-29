import requests
import os
import sqlite3

API_KEY = 'live_FYSwu4Ka6cm7aUfNMYxAt9aOZPkrdVaSlyVV57RlG1f7uE6b1owJw1W2cwdc5z2V'

import requests
import os
import sqlite3

def get_dog_data(api_key, limit=25):
    page = 0
    try:
        with open('current_page.txt', 'r') as f:
            page = int(f.read().strip())
    except FileNotFoundError:
        page = 0

    headers = {
        'x-api-key': api_key,
    }
    url = f'https://api.thedogapi.com/v1/breeds?limit={limit}&page={page}'
    response = requests.get(url, headers=headers)
    data = response.json()

    next_page = page + 1
    with open('current_page.txt', 'w') as f:
        f.write(str(next_page))

    return data

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def create_breed_table(cur, conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Breed (
            id TEXT PRIMARY KEY,
            name TEXT,
            weight_imperial TEXT,
            weight_metric TEXT,
            temperament TEXT,
            origin TEXT,
            life_span TEXT,
            wikipedia_url TEXT,
            image_url TEXT
        )
    ''')
    conn.commit()

def insert_breed_data_to_db(conn, cur, breed_data):
    for breed in breed_data:
        id = breed['id']
        name = breed['name']
        weight_imperial = breed['weight']['imperial']
        weight_metric = breed['weight']['metric']
        temperament = breed.get('temperament', None)
        origin = breed.get('origin', None)
        life_span = breed.get('life_span', None)
        wikipedia_url = breed.get('wikipedia_url', None)
        image_url = breed['image']['url'] if 'image' in breed else None

        cur.execute('''
            INSERT OR IGNORE INTO Breed (
                id, name, weight_imperial, weight_metric, temperament, origin, life_span, wikipedia_url, image_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, name, weight_imperial, weight_metric, temperament, origin, life_span, wikipedia_url, image_url))
    conn.commit()

def main():
    cur, conn = set_up_database('project_database.db')
    create_breed_table(cur, conn)
    insert_breed_data_to_db(conn, cur, get_dog_data(API_KEY, 25))

    conn.close()

if __name__ == '__main__':
    main()