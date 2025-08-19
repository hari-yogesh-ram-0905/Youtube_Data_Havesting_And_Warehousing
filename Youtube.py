# ------------------------------------------------------------------------------------------------------------------------------

#                                                  Importing Libraries 

# ------------------------------------------------------------------------------------------------------------------------------
#                                                          

import mysql.connector   # MySQL Connector → Used to connect and interact with MySQL databases.

import os   # OS Module → Provides functions to interact with the operating system (paths, environment variables, file handling).

import googleapiclient.discovery   # Google API Client → Used to build and access Google APIs like YouTube Data API.

from googleapiclient.errors import HttpError   # HttpError → Handles API request errors/exceptions when calling Google APIs.

import json   # JSON Module → Used to parse and manipulate JSON data (common format for API responses).

import pandas as pd   # Pandas → Powerful data analysis and manipulation library, mainly for tabular (DataFrame) data.

import isodate   # ISODate → Used to parse and handle ISO 8601 date/duration formats (commonly returned in APIs like YouTube).

from datetime import time   # Datetime (time) → Provides time objects to work with hours, minutes, and seconds.

import streamlit as st   # Streamlit → Used for creating interactive web applications and dashboards in Python.

import matplotlib.pyplot as plt   # Matplotlib (Pyplot) → Used for creating static, animated, and interactive visualizations.

import seaborn as sns   # Seaborn → Built on Matplotlib, provides easier and more attractive statistical data visualizations.

import warnings   # Warnings → Used to filter, ignore, or manage warning messages during execution.

from matplotlib import font_manager   # Font Manager → Used to manage and customize fonts in Matplotlib plots.

# Change global font to one that supports Tamil
plt.rcParams['font.family'] = 'Nirmala UI'   # Sets default font to Nirmala UI (supports Tamil text in charts)



# ------------------------------------------------------------------------------------------------------------------------------

#                                                           API Connections

def Api():

    api = "AIzaSyBxcK5jsK2ntHWEviOWuQ_EIaIGDY4DZxA"   # Your API Key here
    api_service_name = "youtube"                      # Which Google API to use
    api_version = "v3"                                # Version of the API

    youtube = googleapiclient.discovery.build(

        api_service_name, api_version, developerKey=api

    )                                                 # Build a client for that API

    return youtube                                    #  Hand back the ready client


youtube = Api()                                       # Create a global client to reuse



# ------------------------------------------------------------------------------------------------------------------------------

#                                                          MySQL Connections

mydb = mysql.connector.connect(

    host='127.0.0.1',     # The database server address. 127.0.0.1 = your own machine (localhost).

    port='3306',          # MySQL’s default port. Change only if your server uses a custom port.

    user='root',          # The MySQL username with access to the database.

    password='********',  # The user’s password. (Never show the real value in presentations.)

    database='Youtube'    # The specific schema you want to use after connecting.

)

cursor = mydb.cursor()   #  Creates a cursor: a lightweight object you use to send SQL commands and fetch results


# ------------------------------------------------------------------------------------------------------------------------------

#                                                           Channel Details 

def channel_info(id):

    #  Create table if it doesn’t exist :
    # ------------------------------------

    cursor.execute("""CREATE TABLE IF NOT EXISTS channel (
                        channel_Name VARCHAR(255),
                        channel_Id VARCHAR(255) PRIMARY KEY,
                        subscribers INT,
                        views INT,
                        Total_videos INT,
                        channel_description TEXT,
                        Playlist_Id VARCHAR(255)
                    )"""
    )


#   Ensures there’s a channel table with columns for name, ID, stats, and playlist.

#   PRIMARY KEY = channel_Id → avoids duplicates.


    
    #  Request channel details from YouTube API :
    # --------------------------------------------

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=id
    )

    response = request.execute()


#   Calls YouTube API with the given channel ID.

#   snippet → name, description.

#   statistics → subscribers, views, video count.

#   contentDetails → playlist IDs.

#    response holds all returned data.



    # Extract useful fields :
    # ------------------------

    for i in response.get('items', []):

        data = dict(channel_Name=i['snippet']['title'],
                    channel_Id=i['id'],
                    subscribers=i['statistics']['subscriberCount'],
                    views=i['statistics']['viewCount'],
                    Total_videos=i['statistics']['videoCount'],
                    channel_description=i['snippet']['description'],
                    Playlist_Id=i['contentDetails']['relatedPlaylists']['uploads'])
        

        #  Picks out important details from the response and stores them in a dictionary data.

        #  Example:

        #  "channel_Name": "TechWithTim"

        #  "subscribers": 950000
        


        try:

            channel_Id = data['channel_Id']

            cursor.execute("SELECT * FROM channel WHERE channel_Id = %s", (channel_Id,))

            result = cursor.fetchone()


            #  Insert new channel (if not exists) :
            # --------------------------------------

            if not result:

                sql = """INSERT INTO channel (channel_Name, channel_Id, subscribers, views, Total_videos, channel_description, Playlist_Id) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                
                values = (data['channel_Name'], data['channel_Id'], data['subscribers'], data['views'], data['Total_videos'], data['channel_description'], data['Playlist_Id'])
                
                cursor.execute(sql, values)

                st.success("Channel data inserted successfully!")


            else:

                st.warning("Channel already exists in the table")

            
            #  If not present → insert new record.

            #  If present → show a warning in Streamlit UI.


        #  Handle errors :
        # -----------------

        except mysql.connector.Error as error:

            print("Failed to insert record into channel_info table {}".format(error))


        #  Catches database errors (like wrong data type, lost connection).


    #  Save changes to DB :
    # ---------------------

    mydb.commit()

    #   commit() ensures insert is permanent.


    return data        #   Returns the data dictionary for further use.

# ------------------------------------------------------------------------------------------------------------------------------

#                                                     get Video IDs

def get_Videos_Ids(channel_id):

    Video_Ids=[]

    response=youtube.channels().list(id=channel_id,
                                    part='contentDetails').execute()
    
    Playlist_Id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    next_page_token=None


    while True:

        response1=youtube.playlistItems().list(
                                        part='snippet',
                                        playlistId=Playlist_Id,
                                        maxResults=50,
                                        pageToken=next_page_token).execute()
        
        for i in range(len(response1['items'])):

            Video_Ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])

        next_page_token=response1.get('nextPageToken')


        if next_page_token is None:

            break


    mydb.commit()


    return Video_Ids 
    
# ------------------------------------------------------------------------------------------------------------------------------

#                                                      get video information

def get_video_info(Video_Ids):

    video_data=[]

    for video_id in Video_Ids:

        request=youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
        )

        response=request.execute()
        

        cursor.execute("""CREATE TABLE IF NOT EXISTS video (
                            channel_Name VARCHAR(255),
                            channel_Id VARCHAR(255),
                            video_Id VARCHAR(255) PRIMARY KEY,
                            Title VARCHAR(255),
                            Tags TEXT,
                            Thumbnail TEXT,
                            Description TEXT,
                            Published_date VARCHAR(255),
                            Duration VARCHAR(255),
                            views INT,
                            likes INT,
                            comments INT,
                            Favorite_Count INT 
                        )""")


        for item in response["items"]:

            duration_iso8601 = item['contentDetails']['duration']

            duration_seconds = isodate.parse_duration(duration_iso8601).total_seconds()

            hours = int(duration_seconds // 3600)
            minutes = int((duration_seconds % 3600) // 60)
            seconds = int(duration_seconds % 60)

            duration_time = time(hours, minutes, seconds)
            
            tags = json.dumps(item['snippet'].get('tags')) if item['snippet'].get('tags') else None

            data=dict(channel_Name=item['snippet']['channelTitle'],
                     channel_Id=item['snippet']['channelId'],
                     video_Id=item['id'],
                     Title=item['snippet']['title'],
                     Tags=tags,
                     Thumbnail=json.dumps(item['snippet']['thumbnails']),
                     Description=item['snippet'].get('description'),
                     Published_date=item['snippet']['publishedAt'].replace('T', ' ').replace('Z', ''),
                     Duration=duration_time,
                     views=item['statistics'].get('viewCount'),
                     likes=item['statistics'].get('likeCount'),
                     comments=item['statistics'].get('commentCount'),
                     Favorite_Count=item['statistics'].get('favoriteCount')
                     )
            
            video_data.append(data)

        
            #  To avoid duplicate primary key errors when the same playlist is re-fetched; 
            #  if updating is desired use ON DUPLICATE KEY UPDATE.  ( insert ignore)
            
            cursor.execute("""INSERT IGNORE INTO video 
                (channel_Name, channel_Id, video_Id, Title, Tags, Thumbnail, Description, Published_date, Duration, views, likes, comments, Favorite_Count) 
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (data['channel_Name'], data['channel_Id'], data['video_Id'], data['Title'], data['Tags'], data['Thumbnail'], data['Description'], data['Published_date'], data['Duration'], data['views'], data['likes'], data['comments'], data['Favorite_Count']))
            
            mydb.commit()


    return video_data

# ------------------------------------------------------------------------------------------------------------------------------

#                                                         get playlist details

def get_playlist_details(channel_id):

    all_data = []

    try:

        cursor.execute("""CREATE TABLE IF NOT EXISTS playlist(
                            Playlist_Id VARCHAR(255) PRIMARY KEY,
                            channel_Id VARCHAR(255),
                            channel_Name VARCHAR(255),
                            playlist_name VARCHAR(255)
                        )""")
        
        request = youtube.playlists().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50
        )

        response = request.execute()


        for item in response['items']:

            Playlist_Id = item['id']
            channel_Name = item['snippet']['channelTitle']
            playlist_name = item['snippet']['title']


            data = {
                "Playlist_Id": Playlist_Id,
                "channel_Id": channel_id,
                "channel_Name": channel_Name,
                "playlist_name": playlist_name
            }

            all_data.append(data)


            cursor.execute("""INSERT IGNORE INTO playlist 
                (Playlist_Id, channel_Id, channel_Name, playlist_name) 
                VALUES (%s, %s, %s, %s)""",
                           (Playlist_Id, channel_id, channel_Name, playlist_name))
            
            mydb.commit()


    except Exception as e:

        print(f"Error: {e}")


    return all_data

# ------------------------------------------------------------------------------------------------------------------------------

#                                                         Get comments details

def get_comment_info(video_ids):

    comment_data = []

    try:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comment (
                comment_Id VARCHAR(255) PRIMARY KEY,
                video_Id VARCHAR(255),
                comment_Text TEXT,
                comment_Author VARCHAR(255),
                comment_Published VARCHAR(255)
            )
        """)

        for video_id in video_ids:

            try:

                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=50
                )

                response = request.execute()


                if not response.get('items'):

                    continue


                for item in response['items']:

                    data = {
                        "comment_Id": item['snippet']['topLevelComment']['id'],
                        "video_Id": item['snippet']['topLevelComment']['snippet']['videoId'],
                        "comment_Text": item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        "comment_Author": item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        "comment_Published": item['snippet']['topLevelComment']['snippet']['publishedAt'].replace('T', ' ').replace('Z', '')
                    }

                    comment_data.append(data)

                    cursor.execute("""INSERT IGNORE INTO comment 
                        (comment_Id, video_Id, comment_Text, comment_Author, comment_Published) 
                        VALUES (%s, %s, %s, %s, %s)""",
                        (data['comment_Id'], data['video_Id'], data['comment_Text'], data['comment_Author'], data['comment_Published']))
            
            
            except Exception as ve:

                print(f"Video {video_id}: Could not fetch comments ({ve})")

        mydb.commit()


    except Exception as e:

        print("Error setting up comments table:", e)


    return comment_data

# -------------------------------------------------------------------------------------------------------------------------------

#  The error you’re seeing is not related to your API key or Google Cloud Console settings.

# It comes from the video itself — the uploader of that YouTube video has chosen to disable comments in YouTube Studio.


# That means:
# -----------

# You cannot enable comments using the API key.

# Even if your API key is fully valid and has all YouTube Data API v3 permissions, 
# the API will still block fetching comments for videos where the creator disabled them.

# Only the video owner can enable comments manually (via YouTube Studio → Settings → Community → Comments → Allow all comments).

# -------------------------------------------------------------------------------------------------------------------------------

#                                                       Collect all details

def get_channel_details(channel_id):

    channel_details = channel_info(channel_id)
    Video_Ids = get_Videos_Ids(channel_id)
    video_details = get_video_info(Video_Ids)
    playlist_details = get_playlist_details(channel_id)
    comment_details = get_comment_info(Video_Ids)
    
    channel_df = pd.DataFrame([channel_details])
    video_df = pd.DataFrame(video_details)
    playlist_df = pd.DataFrame(playlist_details)
    comment_df = pd.DataFrame(comment_details)
    
    return {
        "channel_details": channel_df,
        "video_details": video_df,
        "playlist_details": playlist_df,
        "comment_details": comment_df
    }

# ------------------------------------------------------------------------------------------------------------------------------

#                                            Fetch MySQL Tables back into DataFrame

connection =mysql.connector.connect(

    host='127.0.0.1',     # The database server address. 127.0.0.1 = your own machine (localhost).

    port='3306',          # MySQL’s default port. Change only if your server uses a custom port.

    user='root',          # The MySQL username with access to the database.

    password='********',  # The user’s password. (Never show the real value in presentations.)

    database='Youtube'    # The specific schema you want to use after connecting.

)

cursor = connection.cursor()

def get_channel_data():

    cursor.execute('SELECT * FROM channel')

    return pd.DataFrame(cursor.fetchall(), columns=[i[0] for i in cursor.description])


def get_playlist_data():

    cursor.execute('SELECT * FROM playlist')

    return pd.DataFrame(cursor.fetchall(), columns=[i[0] for i in cursor.description])


def get_video_data():

    cursor.execute('SELECT * FROM video')

    return pd.DataFrame(cursor.fetchall(), columns=[i[0] for i in cursor.description])


def get_comment_data():

    cursor.execute('SELECT * FROM comment')

    comment_data = cursor.fetchall()


    if comment_data:

        return pd.DataFrame(comment_data, columns=[i[0] for i in cursor.description])
    

    else:

        return pd.DataFrame(columns=["comment_Id", "video_Id", "comment_Text", "comment_Author", "comment_Published"])

# ------------------------------------------------------------------------------------------------------------------------------

#                                                            Streamlit UI   

def main():

    st.sidebar.title("Navigations")

    option = st.sidebar.radio("Select an option", ["Home", "Add data to MySQL", "View Tables", "Queries"])


    if option == "Home":

        st.title(":blue[YOUTUBE HARVESTING AND DATA WAREHOUSING]")
        st.write("This project extracts YouTube channel data using API and stores it in MySQL for querying.")
        st.header(":red[Technologies Used :]")
        st.markdown("- PYTHON")
        st.markdown("- MySQL")
        st.markdown("- STREAMLIT")

    elif option == "Add data to MySQL":

        st.title(':red[YouTube Channel Details]')
        channel_id = st.text_input(':blue[Enter YouTube Channel ID:]')

        if st.button('Store and collect Data'):

            details = get_channel_details(channel_id)

            st.subheader('Channel Details')
            st.dataframe(details["channel_details"])
            st.subheader('Video Details')
            st.dataframe(details["video_details"])
            st.subheader('Playlist Details')
            st.dataframe(details["playlist_details"])
            st.subheader('Comment Details')
            st.dataframe(details["comment_details"])


    elif option == 'View Tables':

        st.subheader(":blue[Select the Table to display]")

        selected_table = st.selectbox(":red[Select a table]", ["Channel", "Playlist", "Video", "Comment"])


        if selected_table == "Channel":

            st.header(":green[Channel Data :]")

            st.dataframe(get_channel_data())


        elif selected_table == "Playlist":

            st.header(":green[Playlist Data :]")

            st.dataframe(get_playlist_data())


        elif selected_table == "Video":

            st.header(":green[Video Data :]")

            st.dataframe(get_video_data())


        elif selected_table == "Comment":

            st.header(":green[Comment Data :]")

            df = get_comment_data()


            if not df.empty:

                st.dataframe(df)


            else:

                st.warning("No comments found in database.")


    elif option == "Queries":

        st.session_state.page = 'questions_page'

        questions_page()


# ------------------------------------------------------------------------------------------------------------------------------

#                                                     Questions - Only DataFrames

# ------------------------------------------------------------------------------------------------------------------------------

#                                            Questions with Visualizations + Filters

def questions_page():

    st.title("YouTube Channel Data Insights 📊")

    questions = [

        "1) Names of all the videos and their corresponding channels",
        "2) Channels with the most number of videos and how many videos they have",
        "3) Top 10 most viewed videos and their respective channels",
        "4) Number of comments for each video and their corresponding channels",
        "5) Videos published in the year 2022",
        "6) Average duration of videos for each channel",
        "7) Videos with the highest number of likes",
        "8) Total views for each channel",
        "9) Videos with views above the channel's average views",
        "10) Videos with the highest number of comments"
    ]

    selected_question = st.selectbox("Choose a question:", questions)

    videos_df = get_video_data()

    # Add filters :
    # -------------
    channel_filter = st.multiselect("Filter by Channel:", options=videos_df['channel_Name'].unique(), default=list(videos_df['channel_Name'].unique()))
    
    filtered_df = videos_df[videos_df['channel_Name'].isin(channel_filter)]


    # 1) Names of all the videos and their corresponding channels :
    # --------------------------------------------------------------

    if selected_question == questions[0]:

        st.dataframe(filtered_df[['Title', 'channel_Name']])

        plt.figure(figsize=(10, 6))

        sns.countplot(data=filtered_df, y="channel_Name", order=filtered_df['channel_Name'].value_counts().index)

        plt.title("Number of Videos per Channel")

        plt.xlabel("Count of Videos")

        st.pyplot(plt)


    # 2) Channels with most number of videos :
    # ----------------------------------------

    elif selected_question == questions[1]:

        df_count = filtered_df.groupby('channel_Name')['Title'].count().reset_index(name='video_count')

        st.dataframe(df_count)

        plt.figure(figsize=(8, 6))

        sns.barplot(data=df_count, x="video_count", y="channel_Name")

        plt.title("Channels with Most Videos")

        st.pyplot(plt)


    # 3) Top 10 most viewed videos :
    # -------------------------------

    elif selected_question == questions[2]:

        top_videos = filtered_df.sort_values(by='views', ascending=False).head(10)

        st.dataframe(top_videos[['Title', 'channel_Name', 'views']])

        plt.figure(figsize=(10, 6))

        sns.barplot(data=top_videos, x="views", y="Title", hue="channel_Name", dodge=False)

        plt.title("Top 10 Most Viewed Videos")

        st.pyplot(plt)


    # 4) Number of comments for each video :
    # ---------------------------------------

    elif selected_question == questions[3]:

        st.dataframe(filtered_df[['Title', 'channel_Name', 'comments']])

        plt.figure(figsize=(10, 6))

        sns.scatterplot(data=filtered_df, x="views", y="comments", hue="channel_Name")

        plt.title("Comments vs Views")

        st.pyplot(plt)


    # 5) Videos published in 2022 :
    # -----------------------------

    elif selected_question == questions[4]:


        df_2022 = filtered_df[filtered_df['Published_date'].str.startswith("2022")]

        st.dataframe(df_2022[['Title', 'channel_Name', 'Published_date']])


        if not df_2022.empty:

            plt.figure(figsize=(8, 6))

            df_2022['month'] = pd.to_datetime(df_2022['Published_date']).dt.month

            sns.countplot(data=df_2022, x="month", hue="channel_Name")

            plt.title("Videos Published in 2022 (by Month)")

            st.pyplot(plt)


        else:

            st.warning("No videos found for 2022 with selected channels.")


    # 6) Average duration of videos :
    # --------------------------------

    elif selected_question == questions[5]:

        filtered_df["Duration_seconds"] = pd.to_timedelta(filtered_df["Duration"]).dt.total_seconds()

        avg_duration = filtered_df.groupby("channel_Name")["Duration_seconds"].mean().reset_index()

        avg_duration["Avg_Duration"] = pd.to_timedelta(avg_duration["Duration_seconds"], unit="s").astype(str)

        st.dataframe(avg_duration[["channel_Name", "Avg_Duration"]])

        plt.figure(figsize=(8, 6))

        sns.barplot(data=avg_duration, x="Duration_seconds", y="channel_Name")

        plt.title("Average Video Duration per Channel (Seconds)")

        st.pyplot(plt)


    # 7) Videos with highest likes :
    # -------------------------------

    elif selected_question == questions[6]:

        top_likes = filtered_df.sort_values(by='likes', ascending=False).head(10)

        st.dataframe(top_likes[['Title', 'channel_Name', 'likes']])

        plt.figure(figsize=(10, 6))

        sns.barplot(data=top_likes, x="likes", y="Title", hue="channel_Name", dodge=False)

        plt.title("Top 10 Videos by Likes")

        st.pyplot(plt)


    # 8) Total views for each channel :
    # ---------------------------------

    elif selected_question == questions[7]:

        total_views = filtered_df.groupby('channel_Name')['views'].sum().reset_index()

        st.dataframe(total_views)

        plt.figure(figsize=(8, 6))

        sns.barplot(data=total_views, x="views", y="channel_Name")

        plt.title("Total Views per Channel")

        st.pyplot(plt)


    # 9) Videos with views above avg per channel :
    # ---------------------------------------------

    elif selected_question == questions[8]:


        avg_views = filtered_df.groupby('channel_Name')['views'].mean().reset_index().rename(columns={'views': 'avg_views'})

        merged_df = pd.merge(filtered_df, avg_views, on='channel_Name')

        above_avg = merged_df[merged_df['views'] > merged_df['avg_views']]

        st.dataframe(above_avg[['Title', 'channel_Name', 'views', 'avg_views']])


        if not above_avg.empty:


            plt.figure(figsize=(10, 6))

            sns.barplot(data=above_avg, x="views", y="Title", hue="channel_Name", dodge=False)

            plt.title("Videos Above Average Views")

            st.pyplot(plt)


        else:

            st.warning("No videos found above average views with selected filters.")


    # 10) Videos with highest comments :
    # -----------------------------------

    elif selected_question == questions[9]:

        top_comments = filtered_df.sort_values(by='comments', ascending=False).head(10)

        st.dataframe(top_comments[['Title', 'channel_Name', 'comments']])

        plt.figure(figsize=(10, 6))

        sns.barplot(data=top_comments, x="comments", y="Title", hue="channel_Name", dodge=False)

        plt.title("Top 10 Videos by Comments")

        st.pyplot(plt)


    if st.button('Go to Home Page'):

        st.session_state.page = 'main_page'



# ------------------------------------------------------------------------------------------------------------------------------

#                                                       Streamlit main app

if __name__ == '__main__':


    if 'page' not in st.session_state:

        st.session_state.page = 'main_page'


    if st.session_state.page == 'main_page':

        main()


    elif st.session_state.page == 'questions_page':

        questions_page()


mydb.close()


# ------------------------------------------------------------------------------------------------------------------------------