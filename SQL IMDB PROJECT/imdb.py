import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import warnings
warnings.filterwarnings('ignore')

#get all data about movies
db="C:\\Users\\deela\\Downloads\\archive (1)\\movies.sqlite"
conn=sqlite3.connect(db)
cur=conn.cursor()



cur.execute("SELECT * FROM movies")
movies=cur.fetchall()

print("movies table\n")
movies = pd.DataFrame(movies, columns = ['id', 'original_title', 'budget', 'popularity', 'release_date', 'revenue', 'title', 'vote_average', 'vote_count', 'overview', 'tagline', 'uid', 'director_id'])
print(movies.head())
print("\n\n")


#get all data about directors
print("directors table\n")
cur.execute("select * from directors")
directors=cur.fetchall()
directors = pd.DataFrame(directors, columns = ['name', 'id', 'gender', 'uid', 'department'])
print(directors.head())


#Check how many movies are present in iMDB
cur.execute("select count(original_title) from movies;")
count=cur.fetchall()
print("\n\n\ntotal no of movies:\n",count )


#Find these 3 directors: James Cameron ; Luc Besson ; John Woo
cur.execute("select * from directors where name=='James Cameron' or name=='Luc Besson' or name=='John Woo'")
three_directors=cur.fetchall()
print("\n\ndirector info for three directors:\n",three_directors)


#all directors with name starting with Steven
cur.execute("SELECT * FROM directors WHERE name LIKE 'Steven%'")
name_like=cur.fetchall()
print("\n\nAll directors whose names start with Steven:\n",name_like)


#Count female directors
cur.execute(" SELECT COUNT(*) from directors where gender == 1")
female_directors = cur.fetchall()
print("\n\n\nThe numbe rof femail directors  are: \n \t", female_directors[0])


#the name of the 10th first women directors
cur.execute("SELECT name FROM directors WHERE gender==1 ORDER BY id")
female_dir=cur.fetchall()
print("\n\n\nThe 10th female director is :\n",female_dir[10])


#the 3 most popular movies
cur.execute("SELECT original_title FROM movies ORDER BY popularity desc")
most_popular=cur.fetchall()
print("\n\n\nthe top 3 most popular movies:\n",most_popular[:3])

#the 3 most bankable movies
cur.execute("SELECT original_title  FROM movies ORDER by budget desc ")
most_bankable = cur.fetchall()
print("\n\n\nThe three most bankable movies are: \n", most_bankable[:3])


#the most awarded average vote since the January 1st, 2000
cur.execute(" SELECT original_title FROM movies WHERE release_date > '2000-01-01' ORDER by vote_average DESC ;")
most_awarded_avg = cur.fetchall()
print("\n\n\nThe most awarded average vote since the January 1st, 2000: \n", most_awarded_avg[0])


#movie(s) were directed by Brenda Chapman
cur.execute("SELECT original_title FROM movies JOIN directors ON directors.id = movies.director_id WHERE name = 'Brenda Chapman';")
directed_by= cur.fetchall()
print("\n\n\nThe movie(s) were directed by Brenda Chapman \n", directed_by)

#director made the most movies
cur.execute("SELECT name FROM directors  JOIN movies ON directors.id = movies.director_id GROUP BY director_id ORDER BY count(name) DESC ;")
#group by should be used when we try to sort using any function
#The GROUP BY statement groups rows that have the same values into summary rows
directed_by= cur.fetchall()
print("\n\n\nThe director made the most movies \n", directed_by[0])


#Whose director is the most bankable
cur.execute("SELECT name FROM directors JOIN movies ON directors.id = movies.director_id GROUP BY name ORDER BY sum(budget) DESC limit 1;")
most_bankable_dir= cur.fetchall()
print("\n\n\nThe most bankable director is \n", most_bankable_dir)







#Data visualization/exploration



#Top 10 highest budget made movies 
cur.execute('SELECT original_title, name, release_date, budget, revenue FROM movies JOIN directors ON movies.director_id = directors.id ORDER BY budget DESC')
mostExpensive = cur.fetchall()
mostExpensive = pd.DataFrame(mostExpensive, columns = ['original_title', 'director_name', 'release_date', 'budget', 'revenue'])
print("\n\n\nTop 10 highest budget made movies\n\n",mostExpensive.head(10))

#Top 10 popularity on movies
cur.execute('SELECT original_title, name, release_date, popularity, revenue FROM movies JOIN directors ON movies.director_id = directors.id ORDER BY popularity DESC')
mostPopular = cur.fetchall()
mostPopular = pd.DataFrame(mostPopular, columns = ['original_title', 'director_name', 'release_date', 'popularity', 'revenue'])
print("\n\n\nTop 10 popularity on movies\n\n",mostPopular.head(10))



#the top 10 Revenue  movies  
cur.execute('SELECT original_title, name, release_date, revenue FROM movies JOIN directors ON movies.director_id = directors.id ORDER BY revenue DESC')
mostProfit = cur.fetchall()
mostProfit = pd.DataFrame(mostProfit, columns = ['original_title', 'director_name', 'release_date', 'revenue'])
print("\n\n\nthe top 10 Revenue  movies \n\n",mostProfit.head(10))



#most profitable movies by james cameron 
cur.execute('SELECT original_title, release_date, budget, revenue, popularity, vote_average FROM directors JOIN movies ON directors.id = movies.director_id WHERE name = "James Cameron" ORDER BY revenue DESC')
moviesByJamesCameron = cur.fetchall()
moviesByJamesCameron = pd.DataFrame(moviesByJamesCameron, columns = ['original_title', 'release_date', 'budget', 'revenue', 'popularity', 'vote_average'])
print("\n\n\nmost profitable movies by james cameron are\n\n",moviesByJamesCameron)


#List out Particular movie for Voting average and votecount
cur.execute('SELECT original_title, name, release_date, vote_average, vote_count FROM movies JOIN directors ON movies.director_id = directors.id ORDER BY vote_average DESC')
bestVote = cur.fetchall()
bestVote = pd.DataFrame(bestVote, columns = ['original_title', 'director_name', 'release_date',  'vote_average', 'vote_count'])
print("\n\n\nmovie for Voting average and votecount\n\n",bestVote.head(10))



# plot a heatmap of correlation
#corr() is used to create the correlation matrix.
#You'll have to make sure that all the elements in the matrix are of numeric type. 
#If they are not of the numeric type you'll have to add or concat them explicitly.

sns.set(rc = {'figure.figsize': (8, 8)})
sns.heatmap(movies[['budget', 'popularity', 'revenue', 'vote_average', 'director_id']].corr(), 
            annot = True, fmt = '.2f', linewidth = 1)
plt.show()
#The Heat Map Graph Shows The Effect Between One Variable To The Other Variables. 
#In The Graph, It Is Clear That budget Has The Greatest Impact on revenue with 0.73. 
#Meanwhile, popularity Is Quite Impact On revenue, And director_id Which Means director_name Also Has A Correlation With revenue, Even Though It Is Small. 
#However, vote_average Has A Very Small Correlation With revenue.



#the  director names with number of movies and revenue
cur.execute('SELECT name, COUNT(original_title), SUM(revenue)FROM directors JOIN movies ON directors.id = movies.director_id GROUP BY name ORDER BY SUM(revenue) DESC')
mostProfitableDirector = cur.fetchall()
mostProfitableDirector = pd.DataFrame(mostProfitableDirector, columns = ['director_name', 'movies', 'revenue'])
print("\n\n\nthe director names with number of movies and revenue\n\n",mostProfitableDirector.head(10))


#By doing Director analysis We know Steven Spielberg is the highest revenue, so list the Steven Spielberg movies info
cur.execute('SELECT original_title, release_date, budget, revenue, popularity, vote_average FROM directors JOIN movies ON directors.id = movies.director_id WHERE name = "Steven Spielberg" ORDER BY release_date DESC')
moviesByStevenSpielberg = cur.fetchall()
moviesByStevenSpielberg = pd.DataFrame(moviesByStevenSpielberg, columns = ['original_title', 'release_date', 'budget', 'revenue', 'popularity', 'vote_average'])
print("\n\n\nthe Steven Spielberg movies info\n\n",moviesByStevenSpielberg)



