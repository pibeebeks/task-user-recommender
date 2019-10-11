import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
import rec

def get_data():
    '''
    Function to get data from file.
    
    Returns
    (Lists): Notifications table
    '''
    #Read the notifications table
    try:
        notifications = pd.read_csv('https://raw.githubusercontent.com/pibeebeks/task-user-recommender/master/data/notifications.csv')
        notifications.drop(['id', 'created_at', 'updated_at'], axis=1, inplace=True)
        return notifications
    except:
        print("unable to read file")

def save_model(recommender):
    '''
    Function to save recommended output to a file 
    
    Parameters
    recommender
    (file):a file of the reccommender model

    Returns
    (): The list of file names in which the data is stored
    '''
    filename = 'popular.sav'
    joblib.dump(recommender, filename)

def main():
    '''
    Function to classify and define train data and test data

    '''
    try:
        notifications = get_data()
        train_data, test_data = train_test_split(notifications, test_size=0.40, random_state=0)
        
        recommender = rec.popularity_recommender_py()
        recommender.create(train_data, 'user_id')
        recommender.create(test_data, 'user_id')

        save_model(recommender)
    
    except:
        print("Error saving model")


if __name__ == '__main__':
    main()
