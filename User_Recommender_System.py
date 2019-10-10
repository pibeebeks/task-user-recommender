# -*- coding: utf-8 -*-

#Importing utilities

import pandas as pd
import numpy as np
import mysql.connector


#Getting the data from the database and showing the tables

mydb = mysql.connector.connect(host="remotemysql.com",
                              user="8SawWhnha4",
                              passwd="zFvOBIqbIz",
                              database="8SawWhnha4")

dbcursor = mydb.cursor()
dbcursor.execute("show tables")
for table in dbcursor:
  print(table)


#Extracting the table relevant for users and their bio

from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://8SawWhnha4:zFvOBIqbIz@remotemysql.com/8SawWhnha4')  
  
# Looking at the Users table

users = pd.read_sql_query("select * from users", engine)

users

# Dropping columns considered irrelevant
users = users.drop(["username","email","image","provider","provider_id","password",
                   "remember_token","created_at","updated_at"], axis=1)
# Checking the outcome
users

#Checking other tables showed that id here means user_id
#So we rename the id clumn to userid

users.rename(columns={"id":"user_id"}, inplace = True)
indices = pd.Series(users['user_id'].index)

users

# filling the missing values with empty string and dropping empty short_bio rows
users['short_bio'] = users['short_bio'].fillna('')
users.drop(users[users['short_bio']==''].index, inplace=True)

#Taking out special characters
users['short_bio'] = users['short_bio'].str.replace(r'\W', ' ')

#Checking
users

# Importing 
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

users_tfidf = TfidfVectorizer(stop_words='english')

# computing TF-IDF matrix required for calculating cosine similarity
users_transf = users_tfidf.fit_transform(users['short_bio'])

cosine_similarity = linear_kernel(users_transf, users_transf)

#Declaring a function that would use our model to fetch users similar to a given user based on user_bio

def recommend(index, cosine_sim=cosine_similarity):
    try:
        id = indices[index]
        # Get the pairwsie similarity scores of all names
        # sorting them and getting top 10
        similarity_scores = list(enumerate(cosine_sim[id]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[1:11]

        # Get the names index
        users_index = [i[0] for i in similarity_scores]

        # Return the top 10 most similar names
        return users['name'].iloc[users_index]
    except:
        return 'This user has no bio description'
    
#Testing the model
recommend(2)
recommend(7)

import pickle

# save the model to disk
filename = 'finalized_model.sav'
pickle.dump(users_tfidf, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))

# Fetching the posts table 
posts = pd.read_sql_query("select * from posts", engine)

posts.head()

#Keeping only relevant columns
posts = posts.drop(['tags','slug','created_at','updated_at','image','status_id','action','post_id'], axis=1)

# filling the missing values with empty string and dropping empty short_bio rows
posts['title'] = posts['title'].fillna('')
posts.drop(posts[posts['title']==''].index, inplace=True)

#Taking out special characters
posts['title',] = posts['title'].str.replace(r'\W', ' ')
posts['content',] = posts['content'].str.replace(r'\W', ' ')
# Remove html tags
posts['content'] = posts['content'].str.replace(r'<[^>]*>', '')

# Remove white spaces including new lines
posts['content'] = posts['content'].str.replace(r'\s', ' ')

# Remove square brackets
posts['content'] = posts['content'].str.replace(r'\[.*?\]', '')

# Remove image files
posts['content'] = posts['content'].str.replace(r'\(.*?\)', '')

# Importing 
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

posts_tfidf = TfidfVectorizer(stop_words='english')

# computing TF-IDF matrix required for calculating cosine similarity
posts_transf = posts_tfidf.fit_transform(posts['title'])

cosine_similarity = linear_kernel(posts_transf, posts_transf)

#Declaring a function that would use our model to recommend articles to a user

def recommend(index, cosine_sim=cosine_similarity):
    try:
        id = indices[index]
        # Get the pairwsie similarity scores of all names
        # sorting them and getting top 10
        similarity_scores = list(enumerate(cosine_sim[id]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[1:11]

        # Get the names index
        posts_index = [i[0] for i in similarity_scores]

        # Return the top 10 most similar names
        return posts['content'].iloc[posts_index]
    except:
        return 'This user has no article recommendation'

recommend(4)   
recommend(6) 

#Loading our model
import pickle

# save the model to disk
filename = 'final_model.sav'
pickle.dump(posts_tfidf, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))