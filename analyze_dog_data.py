import sqlite3
import os
import csv
import matplotlib.pyplot as plt


def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def parse_weight(weight_str):
    weight_parts = weight_str.split(' - ')
    weights = []
    
    for part in weight_parts:
        weights.append(float(part))
    
    if len(weights) == 2:
        return sum(weights) / 2
    
    return None
    
def get_breed_weights(cur):
    cur.execute("SELECT name, weight_imperial FROM Breed")
    return cur.fetchall()

def calculate_average_weights(breed_weights):
    breed_weight_average = []
    for breed, weight_str in breed_weights:
        average_weight = parse_weight(weight_str)
        if average_weight is not None:
            breed_weight_average.append((breed, average_weight))
    return breed_weight_average

def write_weights_to_csv(breed_weights, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Breed', 'Average Weight (Imperial)'])  # headers
        writer.writerows(breed_weights)  # data

def plot_breed_weights(breed_weights):
    breeds = []
    weights = []
    for bw in breed_weights:
        breeds.append(bw[0])
        weights.append(bw[1])

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(211)
    ax.bar(breeds, weights, color = "green")
    ax.set_xlabel('Breed')
    ax.set_ylabel('Average Weight (lbs)')
    ax.set_title('Average Weights of Dog Breeds')

    plt.xticks(rotation=90)
    plt.tight_layout() 
    
    plt.show()

def main():
    cur, conn = set_up_database('project_database.db')

    breed_weights = get_breed_weights(cur)
    average_breed_weights = calculate_average_weights(breed_weights)
    
    write_weights_to_csv(average_breed_weights, 'breed_weights.csv')
    
    plot_breed_weights(average_breed_weights)

    conn.close()

if __name__ == '__main__':
    main()