# Importing utilities
import argparse
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


# Getting the data from the database and showing the tables
try:
    mydb = mysql.connector.connect(host="remotemysql.com",
                                user="8SawWhnha4",
                                passwd="zFvOBIqbIz",
                                database="8SawWhnha4")

except:
    print("Connection error")

dbcursor = mydb.cursor()

# Extracting the table relevant for users and their bio
engine = create_engine('mysql+mysqlconnector://8SawWhnha4:zFvOBIqbIz@remotemysql.com/8SawWhnha4')

# Looking at the Users table
users = pd.read_sql_query("select * from users", engine)

# Dropping columns considered irrelevant
users = users.drop(["username", "email", "image", "provider", "provider_id", "password",
                    "remember_token", "created_at", "updated_at"], axis=1)

# Checking other tables showed that id here means user_id
# So we rename the id column to user_id

users.rename(columns={"id": "user_id"}, inplace=True)
# Construct a reverse map of indices and user name
indices = pd.Series(users.index, index=users['user_id'])
users = users.set_index('user_id')

# filling the missing values with empty string
users['short_bio'] = users['short_bio'].fillna('')

# removing Users without a bio
users.drop(users[users['short_bio'] == ''].index, inplace=True)

# Cleaning user_bio data
users['short_bio'] = users['short_bio'].str.replace(r'\W', ' ')

# Creating user TfidVectorizer object
users_tfidf = TfidfVectorizer(stop_words='english')

# computing TF-IDF matrix required for calculating cosine similarity
users_transform = users_tfidf.fit_transform(users['short_bio'])

cosine_similarity = linear_kernel(users_transform, users_transform)


def recommend(index, cosine_sim=cosine_similarity):
    """
    Declaring a function that would use our model to fetch users similar to a given user based on user_bio
    :param index: User Id of user to recommend followers to
    :param cosine_sim: cosine similarity matrix
    :return: Pandas series of similar users based on bio
    """
    try:
        idx = indices[index]
        # Get the pairwise similarity scores of all names
        # sorting them and getting top 10
        print(f"Getting recommendations for {users['name'].iloc[idx]}")
        similarity_scores = list(enumerate(cosine_sim[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[1:11]

        # Get the names index
        lucid_index = [i[0] for i in similarity_scores]

        # Return the top 10 most similar names
        return users['name'].iloc[lucid_index]
    except KeyError:
        return 'This user shows no similarity'
    except IndexError:
        return 'This user has no bio'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id', type=int,
                        help='Enter User id of the user you wish to recommend followers to')

    args = parser.parse_args()

    recommendation_df = recommend(args.user_id)
    print(recommendation_df)


if __name__ == '__main__':
    main()
