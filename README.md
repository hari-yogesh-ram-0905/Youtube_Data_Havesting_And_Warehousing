
# YouTube Data Harvesting and Warehousing using SQL and Streamlit

---

## Table of Contents

1. [Overview](#overview)  
2. [Motivation](#motivation)  
3. [Goals](#goals)  
4. [Tech Stack](#tech-stack)  
5. [Features](#features)  
6. [Data Description](#data-description)  
7. [Installation](#installation)  
8. [Usage](#usage)  
9. [Results](#results)  
10. [Future Work](#future-work)  
11. [Contact](#contact)

---

## 1. Overview

This project is an end-to-end Streamlit application that enables users to extract, store, and visualize YouTube channel data. Using Google API, users can input YouTube Channel IDs to collect data such as channel details, video statistics, and comments, then store it in a SQL data warehouse. The app supports advanced querying and displays results using a clean Streamlit interface.

---

## 2. Motivation

Analyzing YouTube channel data is valuable for content creators, marketers, and analysts. However, manually fetching and cleaning data for multiple channels is tedious. This project simplifies that process with automation, structured storage, and instant visual feedback through a Streamlit interface.

---

## 3. Goals

- Build a simple UI to input YouTube Channel IDs  
- Use Google API to extract video/channel/comment data  
- Store cleaned and structured data in MySQL 
- Enable SQL-based querying and display results in a user-friendly format  
- Build a reusable and scalable Streamlit application

---

## 4. Tech Stack

- **Programming Language**: Python  
- **Web Framework**: Streamlit  
- **Data Collection**: Google YouTube API  
- **Database**: MySQL 
- **Data Manipulation**: pandas  
- **Backend Integration**: SQLAlchemy, mysql-connector-python  

---

## 5. Features

- Input YouTube Channel ID to retrieve data  
- Collect and warehouse data for up to 10 channels  
- Extract channel, playlist, video, and comment data  
- Store structured data into MySQL 
- Execute SQL queries on the data warehouse  
- Display query outputs as tables in Streamlit  
- Visualize metrics like views, likes, and durations  
- Interactive UI for searching, storing, and analyzing YouTube data  

---

## 6. Data Description

The data includes detailed information for each YouTube channel and associated videos:

### Example Data Structure:

- `Channel_Name`: Channel ID, Name, Subscriber Count, Views, Description, Playlist ID  
- `Video_Id_x`: Video ID, Title, Description, Tags, View Count, Like/Dislike, Comments, Duration  
- `Comments`: Comment ID, Text, Author, Published Date

### Example SQL Tables:

#### Table: `Channel`
| Column Name         | Data Type     | Description                           |
|---------------------|---------------|---------------------------------------|
| channel_id          | VARCHAR(255)  | Unique ID for the channel             |
| channel_name        | VARCHAR(255)  | Name of the channel                   |
| channel_type        | VARCHAR(255)  | Type of content                       |
| channel_views       | INT           | Total views                           |
| channel_description | TEXT          | Description of the channel            |
| channel_status      | VARCHAR(255)  | Status                                |

#### Table: `Playlist`
| Column Name  | Data Type     | Description                         |
|--------------|---------------|-------------------------------------|
| playlist_id  | VARCHAR(255)  | Playlist ID                         |
| channel_id   | VARCHAR(255)  | Foreign key to Channel              |
| playlist_name| VARCHAR(255)  | Name of the playlist                |

#### Table: `Comment`
| Column Name            | Data Type     | Description                           |
|------------------------|---------------|---------------------------------------|
| comment_id             | VARCHAR(255)  | Unique ID for the comment             |
| video_id               | VARCHAR(255)  | Foreign key to Video                  |
| comment_text           | TEXT          | Content of the comment                |
| comment_author         | VARCHAR(255)  | Author of the comment                 |
| comment_published_date | DATETIME      | When the comment was posted           |

---

## 7. Installation

1. Clone or download the project  
2. Make sure you have Python 3.x installed  
3. Install required packages:

```bash
pip install streamlit pandas sqlalchemy mysql-connector-python google-api-python-client
```

4. Set up MySQL/PostgreSQL and create a database (e.g., `youtube_data`)

5. Obtain YouTube API Key from [Google Cloud Console](https://console.cloud.google.com)

---

## 8. Usage

- Run the Streamlit app:

```bash
streamlit run Youtube_harvesting.py
```

- Use the following tabs in the app:
  - **About**: Project overview and workflow explanation  
  - **Channel Data Collection**: Input channel ID, extract and view metadata  
  - **Data Migration**: Store data into SQL database  
  - **SQL Queries**: Execute pre-defined and custom queries  
  - **Visualizations**: Visualize key metrics like views, likes, comments  
  - **Conclusion**: Project summary and insights  

### SQL Query Examples (Displayed as Tables):

1. Names of all videos and their respective channels  
2. Channels with the highest number of videos  
3. Top 10 most viewed videos and channels  
4. Video-wise comment counts  
5. Videos with the most likes and their channels  
6. Total likes/dislikes per video  
7. Total views per channel  
8. Channels that posted videos in 2022  
9. Average video duration per channel  
10. Videos with the most comments and their channels  

---

## 9. Results

- Data from up to 10 YouTube channels harvested via Google API  
- Data cleaned and stored in MySQL warehouse  
- SQL queries executed and results visualized inside the app  
- A clean, interactive tool for YouTube data analysis is available  
- Demonstrates integration between API, data engineering, and front-end display

---

## 10. Future Work

- Add support for YouTube OAuth to retrieve private channel data  
- Introduce data quality checks and outlier detection  
- Export charts as PNG or CSV  
- Enable scheduling for automatic data sync  
- Deploy app using Docker or Streamlit Cloud  
- Add multi-user login and data role permissions

---

## 11. Contact

For any questions, feedback, or collaboration opportunities, please contact:  

**Hari Yogesh Ram B**  
Email: hariyogeshram882@gmail.com
