import tweepy
import sys
import sqlite3
from sqlite3 import Error
import time



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


# http://www.sqlitetutorial.net/sqlite-python/insert/

def create_connection(db_file):
    """Create a database connection to the SQLite database
    param db_file: database file for database
    return: connection object or None"""

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def write_articles_by_screen_name(conn, t_screen_name):
    try:
        t_sql = '''INSERT INTO main_articles(article_id, author, title , source_url) VALUES(?, ?, ? ,?)'''

        cur = conn.cursor()
        cur.execute(t_sql, t_screen_name)
    except Error as e:
        print(e)
    return cur.lastrowid

def link_comments_to_articles(conn):
    cursor = conn.execute("UPDATE main_comments SET article_id=(SELECT article_id FROM main_articles WHERE author = main_comments.screen_name);")
    conn.commit()


def build_articles_by_screen_name(conn):
    cursor = conn.execute("select distinct user_screen_name, user_name from main_tweets")
    i = 1
    for row in cursor:
        user_url = 'https://twitter.com/'+row[0]
        article_payload = (i, row[0], row[0], user_url)
        recId = write_articles_by_screen_name(conn, article_payload)
        i +=1
    conn.commit()
    return True


def write_comments_by_screen_name(conn, t_tweet):
    #print(t_tweet)
    t_sql = '''INSERT INTO main_comments(screen_name, comment_raw) VALUES(?, ?)'''
    try:
        cur = conn.cursor()
        cur.execute(t_sql, t_tweet)
    except Error as e:
        print(e)
    return cur.lastrowid


def build_comments_by_screen_name(conn):
    cursor = conn.execute("select distinct id_str, tweet_id, tweet_text, user_screen_name, topic "
                          "from main_tweets order by user_screen_name")
    master_comments = {}
    current_screen_name = 'NULL'
    work_string = ''
    i = 0
    for row in cursor:
        i += 1
        if current_screen_name == row[3]:
            work_string = work_string + ' |||||t' + row[2].replace('\n', '').replace('\r', '')
        else:
            master_comments[current_screen_name] = work_string
            work_string = ''
            work_string = row[2].replace('\n', '').replace('\r', '') + '\t'
            current_screen_name = row[3]
    return master_comments

def clean_comments(conn):
    cursor = conn.execute("update main_comments set comment_clean = replace(replace(comment_raw,'#',''),'@','')")
    conn.commit()

def db_create_tweet(conn, t_tweet):
    print(t_tweet)
    t_sql = '''INSERT INTO main_tweets(id_str, tweet_text, user_screen_name, created_at, topic) VALUES(?, ?, ? ,?, ?)'''
    cur = conn.cursor()
    cur.execute(t_sql, t_tweet)
    return cur.lastrowid

def hashtag_list():
    hashtags = {'#democrat': 100, "#danger": 100, '#republican': 100, '#breaking': 100, '#china': 100, '#russia': 100,
    '#healthinsurance': 100, '#fraud': 100, '#surveillance': 100, '#measles': 100, '#felony': 100,
    '#drug': 100, '#mueller': 100, '#arrest': 100, '#criminal': 100, '#police': 100,
    '@CNN': 100, '#Foxnews': 100, '#shooting': 1000, '@realdonaldtrump': 1500, '#terrorism': 1500,
    '#fishing': 1500, '#python': 1500, '#UIUC': 1500, "#buildawall": 1000, "@OCSheriff": 750,
    "#illegal": 100, '#hate': 1000, '@elonmusk': 100, '#mexico': 100, '#buildthewall': 100,
    '#teens': 100, '#coursera': 100, '@speakerpelosi': 100, '#victim': 100, '#FBI': 100,
    '#disneyland': 100, '#stocks': 100, '#CIA': 100, '#FBI': 100, '#CBP': 100,
    '#MAGA': 100, '#OCREgister': 100, '#school': 100, '#california': 100, '#mexico': 100,
    '#healthcare': 100, '#april': 100, '#endgame': 100, '#student': 100, '#theif': 100,
    '#SB54': 100, "#losangeles": 100, "#world": 100, "#UN": 100, "#newyork": 100,
    '#hacker': 100, '#may': 100, '#zombie': 100, '#today': 100, '#GOT': 100,
    '@wapo': 100, "#nytimes": 100, '#HBPD': 100, "#google": 100, "#rally": 100,
    '#opioids': 100, '#HIV': 100, '#religion': 100, '#trending': 100, '@WSJ': 100, '@cnnpolitics': 100,
    '#fakenews': 100, '#media': 100}
    clear_hashtags_from_db(conn)
    for hashtag, last_id in hashtags.items():
        hashtag_string = (hashtag, last_id)
        write_hashtag_to_db(conn, hashtag_string)

    return hashtags

def clear_hashtags_from_db(conn):
    print('Deleting existing hashtags and resetting')
    cur = conn.execute('Delete from main_hashtags')

def write_hashtag_to_db(conn, topic):
    cur = conn.execute
    print('writing hashtag to database', topic)
    t_sql = '''INSERT INTO main_hashtags(hashtag_string, hashtag_lastvalue) VALUES(?, ?)'''
    try:
        cur = conn.cursor()
        cur.execute(t_sql, topic)
    except Error as e:
        print(e)
    print('success')
    conn.commit()
    return cur.lastrowid




def main(topics, conn):

    f_tweet = {}
    replies = []
    count = 1
    for topic, start in topics.items():
        print(topic)
        print("running for topic: ", topic, " starting at tweet:")
        with conn:
            non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
            for full_tweets in tweepy.Cursor(api.search, q=topic + " -filter:retweets", count=500, lang="en", since="2019-04-01").items(500):
                art_payload = full_tweets.id_str+";"+full_tweets.user.screen_name+";" + \
                              full_tweets.text.translate(non_bmp_map).replace('\n', ' ').replace('\r', '').replace(';', ':')
                comment = ""
                ft_sql_pay_load = (full_tweets.id_str, full_tweets.text.translate(non_bmp_map),
                                   full_tweets.user.screen_name, full_tweets.created_at, topic);
                ft_id = db_create_tweet(conn, ft_sql_pay_load)
                count +=1

                f_tweet.update({full_tweets.id_str: art_payload})
        print("starting wait")
        sleep_time = 10
        for i in range(6):
            print('sleeping for ',sleep_time,' seconds, step:', 6-i)
            time.sleep(sleep_time)

    #build_articles_by_screen_name(conn)
    #master_comments = build_comments_by_screen_name(conn)
    #for key, value in master_comments.items():
    #    ft_sql_pay_load = (key, value);
    #    ft_id = write_comments_by_screen_name(conn, ft_sql_pay_load)
    #    print(ft_id)



#setup the base database connection
db_name = '..\db.sqlite3'
conn = create_connection(db_name)
#get our list of hashtags (TODO: move this to db later)

topics_new =hashtag_list()

#run our main twitter extract, TODO: split this up into smaller functions
#main(topics_new, conn)

build_articles_by_screen_name(conn)
master_comments = build_comments_by_screen_name(conn)

for key, value in master_comments.items():
    ft_sql_pay_load = (key, value);
    ft_id = write_comments_by_screen_name(conn, ft_sql_pay_load)

link_comments_to_articles(conn)

#Because the comments come in with # and @, lets remove those so they do not interfer with rank function
clean_comments(conn)
#make sure everything gets pushed to the DB
conn.commit()
conn.close()

