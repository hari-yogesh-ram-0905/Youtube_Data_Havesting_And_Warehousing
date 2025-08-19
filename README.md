# YouTube Data Harvesting & Warehousing (By Using Python, MySQL & Streamlit)

------------------------------------------------------------------------

## 🧠 Table of Contents

-   [📌 Overview](#-overview)
-   [🎯 Motivation](#-motivation)
-   [🚀 Goals](#-goals)
-   [🛠 Tech Stack](#-tech-stack)
-   [✨ Features](#-features)
-   [📊 Data Description](#-data-description)
-   [⚙️ Installation](#️-installation)
-   [💡 Usage](#-usage)
-   [📈 Results](#-results)
-   [🔮 Future Work](#-future-work)
-   [📬 Contact](#-contact)

------------------------------------------------------------------------

## 📌 Overview

This project focuses on **extracting, storing, and analyzing YouTube
data** using the **YouTube Data API v3**.\
The data (Channels, Playlists, Videos, Comments) is stored in a **MySQL
database** and analyzed through an **interactive Streamlit dashboard**
for insights.

------------------------------------------------------------------------

## 🎯 Motivation

YouTube generates a massive volume of unstructured data every second.\
Manually collecting and analyzing this data is time-consuming and
inefficient.\
This project automates the process to:

-   Collect structured YouTube data.\
-   Store it centrally in a MySQL database.\
-   Provide easy querying and visualization through a dashboard.\
-   Help content creators, marketers, and analysts make informed
    decisions.

------------------------------------------------------------------------

## 🚀 Goals

-   Automate YouTube data collection via API.\
-   Store channel, video, playlist, and comment data in MySQL.\
-   Build an interactive Streamlit dashboard for queries & insights.\
-   Answer analytical questions with visualizations.\
-   Provide business and marketing insights from YouTube data.

------------------------------------------------------------------------

## 🛠 Tech Stack

  -----------------------------------------------------------------------
  Component                               Description
  --------------------------------------- -------------------------------
  **Python**                              Data extraction, processing,
                                          and integration

  **YouTube Data API v3**                 Fetch channel, video, playlist,
                                          and comment data

  **MySQL**                               Structured data storage

  **Streamlit**                           Interactive dashboard &
                                          visualization

  **Pandas**                              Data manipulation & analysis

  **Matplotlib & Seaborn**                Data visualization & charts
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## ✨ Features

-   📊 **Data Extraction** --- Channel, Video, Playlist, Comment
    details.\
-   💾 **MySQL Storage** --- Centralized structured storage of YouTube
    data.\
-   📈 **Interactive Dashboard** --- Built using Streamlit with
    navigation tabs.\
-   🎨 **Visualizations**:
    -   Bar Charts (Top Videos by Views/Likes/Comments)\
    -   Countplots (No. of Videos, Published per Month)\
    -   Scatterplots (Views vs Comments)\
    -   Line Charts (Monthly Trends)\
-   🧩 **Query Section** --- 10 analytical questions with charts.\
-   🗂 **Data Retrieval** --- View stored channel, video, playlist, and
    comment tables.

------------------------------------------------------------------------

## 📊 Data Description

  -----------------------------------------------------------------------
  Table Name                               Columns
  ---------------------------------------- ------------------------------
  **Channel**                              Channel ID, Name, Subscribers,
                                           Views, Description, Playlist
                                           ID

  **Video**                                Video ID, Title, Tags,
                                           Duration, Views, Likes,
                                           Comments

  **Playlist**                             Playlist ID, Channel ID, Title

  **Comment**                              Comment ID, Video ID, Author,
                                           Text, Published Date
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## ⚙️ Installation

1.  Clone the repository and install requirements.

    ``` bash
    pip install -r requirements.txt
    ```

2.  Generate **YouTube API Key** from Google Developer Console.

3.  Set up **MySQL Database**:

    ``` sql
    CREATE DATABASE youtube;
    ```

4.  Update **DB credentials** in the Python script.

5.  Run the Streamlit App:

    ``` bash
    streamlit run app.py
    ```

------------------------------------------------------------------------

## 💡 Usage

-   Enter **Channel ID** in the Streamlit app to fetch and store data.\
-   Explore tables: Channel, Playlist, Video, Comment.\
-   Run predefined **queries** to answer business questions.\
-   Visualize results using charts & plots.

**Sample Analytical Questions Answered:**\
1. What are the video names with corresponding channels?\
2. Which channel has the most videos?\
3. What are the top 10 most viewed videos?\
4. How many comments per video?\
5. Which videos were published in 2022?\
6. What is the average video duration per channel?\
7. Which videos have the highest likes?\
8. What are the total views per channel?\
9. Which videos are above average views?\
10. Which videos have the highest comments?

------------------------------------------------------------------------

## 📈 Results

-   Automated extraction of YouTube data.\
-   Stored data in **MySQL database** for structured access.\
-   Built a **Streamlit dashboard** for querying & visualization.\
-   Provided insights on channel growth, engagement, and content
    performance.\
-   Scalable solution for content creators & businesses.

------------------------------------------------------------------------

## 🔮 Future Work

-   📝 Add **sentiment analysis** for comments.\
-   ☁️ Deploy dashboard to cloud (AWS/Heroku).\
-   🔄 Enable real-time data streaming.\
-   📊 Migrate to **NoSQL (MongoDB)** for large-scale data.

------------------------------------------------------------------------

## 📬 Contact

Developed by **HARI YOGESH RAM B**

📧 Email: hariyogeshram882@gmail.com

------------------------------------------------------------------------
