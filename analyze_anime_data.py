import sqlite3
import os
import csv
import matplotlib.pyplot as plt
import numpy as np


def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def get_anime_genre_data(cur):
    cur.execute('''
        SELECT Anime.title, Genre.genre_name
        FROM Anime
        JOIN AnimeGenre ON Anime.id = AnimeGenre.anime_id
        JOIN Genre ON AnimeGenre.genre_id = Genre.id
    ''')
    return cur.fetchall()

def get_genre_counts(cur):
    cur.execute('''
        SELECT Genre.genre_name, COUNT(*)
        FROM Anime
        JOIN AnimeGenre ON Anime.id = AnimeGenre.anime_id
        JOIN Genre ON AnimeGenre.genre_id = Genre.id
        GROUP BY Genre.genre_name
        ORDER BY COUNT(*) DESC
        LIMIT 10
    ''')
    return cur.fetchall()

def write_genre_counts_to_csv(genre_counts, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Genre', 'Count'])  # headers
        writer.writerows(genre_counts)  # data

def plot_genre_counts(genre_counts):
    
    genres = []
    counts = []

    for genre_count in genre_counts:
        genre = genre_count[0]
        genres.append(genre)
    
        count = genre_count[1]
        counts.append(count)
    
    fig = plt.figure(figsize=(10,10))
    
    ax = fig.add_subplot(211)    
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(genres)))
    
    ax.bar(genres, counts, color=colors)
    ax.set_xlabel('Genre')
    ax.set_ylabel('Count')
    ax.set_title('Count of Animes by Genre')
    
    ax2 = fig.add_subplot(212) 
    ax2.pie(counts, labels = genres, colors = colors, autopct='%1.1f%%')
    ax2.set_title('Popularity of Anime Genres')
    
    plt.xticks(rotation=45)
    plt.tight_layout() 

    plt.show()
    
def main():
    cur, conn = set_up_database('project_database.db')
    
    genre_counts = get_genre_counts(cur)
    
    write_genre_counts_to_csv(genre_counts, 'genre_counts.csv')
    plot_genre_counts(genre_counts)

    conn.close()

if __name__ == '__main__':
    main()