import pandas as pd   #import the needed module
def task12():         #define the function
    df = pd.read_csv('posts.csv',usecols=['user_id','title','content'],encoding="utf-8")  #import the posts.csv file to collect title which we need
    dh = df.sort_values(by='user_id')  #sort by user_id to get the user_id in ascending order which will help us easily reference it later on
    dg = pd.read_csv('nooffollowers.csv',encoding="utf-8",usecols=['user_id', 'username'])  #we are reading our nooffollowers file which serves as a link between bio and title concatenation
    dy = dg.merge(dh, how='left', on = 'user_id') #we merge our existing csvs
    dy1 = dy[['user_id','username','title']]  #we choose the relevant fields we need
    dz = pd.read_csv('users.csv',usecols=['username','short_bio'],encoding="utf-8") #we read the file which contains short bio
    dp = dz.merge(dy1, how='left', on = 'username') #we merge by username
    dp.to_csv('output.csv', encoding='utf-8') #we define the name of the output


task12()  #we call the function

        
