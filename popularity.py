import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
import rec

def get_data():
    #Read the notifications table
    notifications = pd.read_csv('https://raw.githubusercontent.com/pibeebeks/task-user-recommender/master/data/notifications.csv')
    notifications.drop(['id', 'created_at', 'updated_at'], axis=1, inplace=True)
    return notifications

def save_model(recommender):
    filename = 'popular.sav'
    joblib.dump(recommender, filename)

def main():
    notifications = get_data()
    train_data, test_data = train_test_split(notifications, test_size=0.40, random_state=0)
    
    recommender = rec.popularity_recommender_py()
    recommender.create(train_data, 'user_id')
    recommender.create(test_data, 'user_id')

    save_model(recommender)

if __name__ == '__main__':
    main()
