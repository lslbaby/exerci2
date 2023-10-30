import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('stephen_king_adaptations.db')
cursor = conn.cursor()

# Create a table named 'stephen_king_adaptations_table' with columns movieID, movieName, movieYear, and imdbRating
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
        movieID INTEGER PRIMARY KEY,
        movieName TEXT,
        movieYear INTEGER,
        imdbRating REAL
    )
''')
conn.commit()

# Read the 'stephen_king_adaptations.txt' file and copy its content into the 'stephen_king_adaptations_list' list
stephen_king_adaptations_list = []
with open('stephen_king_adaptations.txt', 'r') as file:
    for line in file:
        parts = line.strip().split('\t')
        if len(parts) == 4:
            movieName, movieYear, imdbRating = parts[0], int(parts[1]), float(parts[2])
            stephen_king_adaptations_list.append((movieName, movieYear, imdbRating))

# Insert the content into the database
cursor.executemany('''
    INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating)
    VALUES (?, ?, ?)
''', stephen_king_adaptations_list)
conn.commit()

# Provide user options
while True:
    print("Options:")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. Quit")
    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        movie_name = input("Enter the movie name to search: ")
        cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?', (movie_name,))
        movie = cursor.fetchone()
        if movie:
            print(f"Movie Name: {movie[1]}")
            print(f"Movie Year: {movie[2]}")
            print(f"IMDB Rating: {movie[3]}")
        else:
            print("The movie is not in our database")
    elif choice == '2':
        year = input("Enter the movie year to search: ")
        cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?', (year,))
        movies = cursor.fetchall()
        if movies:
            for movie in movies:
                print(f"Movie Name: {movie[1]}")
                print(f"Movie Year: {movie[2]}")
                print(f"IMDB Rating: {movie[3]}")
        else:
            print("No movies found for that year in our database")
    elif choice == '3':
        rating = float(input("Enter the movie rating: "))
        cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?', (rating,))
        movies = cursor.fetchall()
        if movies:
            for movie in movies:
                print(f"Movie Name: {movie[1]}")
                print(f"Movie Year: {movie[2]}")
                print(f"IMDB Rating: {movie[3]}")
        else:
            print("No movies found in the database with that rating or higher")
    elif choice == '4':
        break

# Close the database connection
conn.close()




