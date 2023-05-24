import math
import pickle
import os

# List of all the genres found in the IMDB-database:

genre_list = ['genres', 'Documentary', 'Short', 'Animation', 'Comedy', 'Romance', 'Sport', 'News', 'Drama', 'Fantasy',
          'Horror', 'Biography', 'Music', 'War', 'Crime', 'Western', 'Family', 'Adventure', 'Action', 'History',
          'Mystery', '\\N', 'Sci-Fi', 'Musical', 'Thriller', 'Film-Noir', 'Talk-Show', 'Game-Show', 'Reality-TV', 'Adult']


def movies():
    
    # Writes the file 'top-movies.txt' which contains all the movies that are in the IMDB-database. 
    # This means that all other types of media in that database, e.g. series or short movies, are filtered out.
    
    raw_data = []
    
    # Opening the full IMDB-database:
    
    fin = open('Imdb-data.tsv', encoding="utf8")
    
    for line in fin:
        
        # Skipping the first line:
        
        if 'tconst' in line:
            continue
        
        # Appending a list with only the items that are considered 'movies':
            
        if 'movie' in line:
            
            raw_data.append(line)
                
        else:
            continue

    # Writing the raw_data into a txt-file that can be accessed by other functions:        
    
    fout = open('movies.txt', 'w', encoding = 'utf16')
            
    for line in raw_data:
        fout.write(line)
    
    fout.close()
                


def movie_ratings():
    
    # Writes a file with all the ratings that belong to movies, filtering out all the ratings from series etc.
    
    movies = open('movies.txt', 'r', encoding = 'utf16') 
    # A file containing all the ratings and number of votes for all items in the IMDB-database
    ratings = open('rating-data.tsv', encoding="utf8")
    
    test_ratings = []
    
    # Creating a list of all the ratings 
    
    for line in ratings:
        
        test_ratings.append(line)
    
    # Creating a dictionary which contains all the unique codes that IMDB links with each item in its database
    # This code looks like 'tt12345...' and can be used to find the data from each movie.
    
    movie_codes = dict()
    
    for line in movies:
        
        # Creating a dictionary with only the codes from movies:
        
        line = line.strip().split()
        movie_codes[line[0]] = 1
              
    
    fout = open('movies-with-ratings.txt', 'w', encoding = 'utf8')
    
    # A for-loop that looks at the code of the rating and compares it to the movie-codes dictionary.
    # If the code is found in the dictionary it means that the rating belongs to a movie, and its written in the file. 
    
    for r in test_ratings:
            
        r = r.strip().split()
        code = r[0]
                        
        if code in movie_codes:
            
            # This formatting is done to write the movie code in the same way as in the IMDB-database:
                
            r = '\t'.join(r) + '\n'
                    
            fout.write(r)
                    
                
    fout.close()
    
    
def movie_dict():
    
    # Creates a database with a dictionary that links the movie code with its data from the IMDB-database
    
    d = dict()
    
    movies = open('movies.txt', 'r', encoding = 'utf16') 
    
    for line in movies:
        
        # Creates a dictionary with the movie code as key and the movie data as value:
        
        line = line.strip().split()
        code = line[0]
   
        d[code] = line
        
    pickle.dump(d,open('movie_dict.pickle', 'wb'))
        
    
def top_n_rated_movies(n):
    
    # Returns the top n rated movies from IMDB with a minimum amount of votes.
    
    t = []
    ratings = open('movies-with-ratings.txt', encoding = 'utf8')
    
    # Create a list with all the movie ratings:
    
    for movie in ratings:
        
        movie = movie.strip().split()
        t.append(movie)
        
    # A short function that selects the second element from an item. 
    # This is used to sort the ratings, which items look like [movie code, rating, votes] based on the rating value. 
    
    def takeSecond(elem):
        return elem[1]
    
    # Reverse the sorted list to have it in descending order:
    
    t.sort(key=takeSecond, reverse = True)
    
    top_n_rated = []
    
    m = 0
    min_votes = 50000
    
    # Creates a list with the top n rated movies, excluding movies that have less than min_votes votes.
    
    for movie in t:
        
        votes = int(movie[2])
        
        if m == n:
            break
        
        elif votes > min_votes:
            top_n_rated.append(movie)
            m = m + 1
            
        else:
            continue
    
    return top_n_rated

    
 

def movie_title(code):
    
    # Returns the title(s) of the corresponding movie code(s)
    
    d = pickle.load(open('movie_dict.pickle', 'rb'))
    
    titles = []
    
    # Create a list with all the movie titles that correspond to the given movie codes:
    
    for i in code:  
    
        data = d[i]
        
        # Because the titles are comma-separated and there are also two titles in the data for each movie,
        # the individual words in the titles need to be combined.
        # This is done by taking a split from the data, which are all the words from the two titles (original and common)
        # and adding them together with spaces:
            
        double_title = data[2:-5]
            
        halve = int(len(double_title)/2)
    
        title = double_title[:halve]
    
        res = str()
            
        for i in range(halve):
            t = title[i] + ' '
            res = res + t
        
        titles.append(res)
        
    return titles


def plus(a,b):
    
    # Takes two lists and does a matrix-addition, returning the summed lists. 
    
    added_up = []
    for i in range(len(a)):
        added_up.append(a[i]+b[i])
    return added_up


def genre_to_list(genres):
    
    # Turns the items from genres into a list with either 1's or 0's, where
    # 1 denotes that the genre is present in this movie. Returns this list.
    
    t = []
    res = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for genre in genres:
        t = []
        for i in genre_list:
            if genre == i:
                t.append(1)
            else:
                t.append(0)
        res = plus(t,res)
    return res


def movie_knn_data(n, movies):
    
    # Returns movie data that can be used in the knn-algorithm. This means data that looks like 
    # [rating, 0,1,0,0,1,...]
    
    d = pickle.load(open('movie_dict.pickle', 'rb'))
    data = []
    
    # For each movie the rating and genres are obtained and combined to look like the desired data:
    
    for line in movies:
        
        rating = float(line[1])
        
        code = line[0]
        
        movie_data = d[code]
        
        # The genres are turned into a list of 1's and 0's with the genre_to_list function:

        genres = movie_data[-1]
        genres = genres.split(',')
    
        t = genre_to_list(genres)
        
        # The ratings is added to the genre-data list:
        
        t.insert(0,rating)
        
        data.append(t)
  
    return data
        

def euclidean_distance(point1, point2):
    
    # Returns the euclidean distance between two given points.
    
    sum_squared_distance = 0
    
    for i in range(len(point1)):
        sum_squared_distance += math.pow(point1[i] - point2[i], 2)
        
    return math.sqrt(sum_squared_distance)


def knn_movies(rating,genres,n,k):
    
    # Returns the k-closest neighbours for a given entry (rating and genre) using the knn-algorithm.
    
    # Turns the entry-genres into a list using the genre_to_list function:
    entry = genre_to_list(genres)
    entry.insert(0,rating)
    
    movie_data = top_n_rated_movies(n)
    data = movie_knn_data(n, movie_data)
    movie_titles = dict()
    distance_list = []
    k_neighbours_distances = []
    k_neighbours_indices = []
    
    dataset = enumerate(data)
    
    # Creating a list with distances from the entry with its respective
    # positions in the list, here denoted as 'index'
    
    for index, value in dataset:
        distance = euclidean_distance(value,entry)
        distance_list.append((distance,index))
        
    # Sort the list with distances in descending order:
        
    sorted_distances = sorted(distance_list)
    
    # Take the k closest distances create a list:
    for i in range(k):
        k_neighbours_distances.append(sorted_distances[i])
             
    # Obtain the indices of the closest neighbours and create a list with them:
        
    for distance, index in k_neighbours_distances:
        k_neighbours_indices.append(index)
        
    movies = enumerate(movie_data)
    
    top_n_rated_codes = []
    
    # Create a list with the movie codes of the k closest neighbours:
    
    for index,data in movies:
        code = data[0]
        top_n_rated_codes.append(code)
        
    # Create an enumerated list with the titles of the k closest neighbours:
    
    titles = enumerate(movie_title(top_n_rated_codes))
    
    # Create a dictionary that contains the enumerated number corresponding with the movie (key)
    # and the corresponding title (value):
    
    for index,title in titles:
        
        movie_titles[index] = title

    # Prints the titles of the k closests neighbours    

    m = 0
    
    for index in k_neighbours_indices:
        
        if m == k:
            
            return
        
        else:
            
            print(movie_titles[index])
            
            m = m + 1

# Check if the files that are needed already exist

if os.path.exists("movies.txt") == False:
    movies()

if os.path.exists("movies-with-ratings.txt") == False:
    movie_ratings()
    
if os.path.exists("movie_dict.pickle") == False:
    movie_dict()

knn_movies(7.5,['Drama','Mystery','Sci-Fi'], 10000, 4)


    
        
        
        
    
    
        
        
    




    
    


    

    
    
    
    
        

    
    



        
     
