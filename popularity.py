#!/usr/bin/env python
# coding: utf-8
import math
import pandas as pd
import joblib


# In[2]:


#Read the notifications table
notifications = pd.read_csv('data/notifications.csv')
users = pd.read_csv('data/users.csv')
notifications.drop(['id', 'created_at', 'updated_at'], axis=1, inplace=True)
notifications


# In[3]:


def smooth_user_preference(x):
    '''Function to define user preference.

    Parameters
    x
    (int): The numeric input value
    
    Returns
    (float): The log base 2 of input value (x) + 1
    '''
    return math.log(1 + x, 2)


# In[4]:


def recommend(user_id):
    '''Funtion to recommend popular users

    Parameters
    user_id
    (int): The user id

    Return
    (list): A list of users similar to inputted user id 
    '''
    event_type_strength = {
        'Followed': 1.0,
        'Like': 1.0,
        'Love': 2.0,
        'Commented': 4.0,
        'Replied': 4.0
    }
    notifications['eventStrength'] = notifications['action'].apply(lambda x: event_type_strength[x])
    
    users_interactions_count = notifications.groupby(['user_id', 'post_id'])\
        .size().groupby('user_id').size()
    
    users_with_enough_interactions = users_interactions_count[users_interactions_count >= 2]\
    .reset_index()[['user_id']]
    
    interactions_from_selected_users = notifications.merge(users_with_enough_interactions,\
    how='right', left_on='user_id', right_on='user_id')
    
    interactions_full = interactions_from_selected_users.groupby(['user_id'])['eventStrength']\
    .sum().apply(smooth_user_preference).reset_index()
    
    popular_users = interactions_full.sort_values('eventStrength', ascending=False)
    
    is_Self = popular_users['user_id'] != user_id
    
    popular_users.drop(['eventStrength'], axis=1, inplace=True)
    return popular_users[is_Self]

recommend(1)


# In[5]:


filename = 'popular.sav'
joblib.dump(recommend, filename)
