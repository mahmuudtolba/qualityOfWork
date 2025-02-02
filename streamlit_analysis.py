import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

# CSV file path
csv_file = 'pomodoro_sessions.csv'

# Check if the CSV file exists
if os.path.exists(csv_file):
    # Load the CSV data into a DataFrame
    data = pd.read_csv(csv_file)
    data.sort_values(by=['Date'] , inplace=True )

    # Convert session length to minutes and session start time to datetime
    def session_length_to_minutes(length):
        time_parts = list(map(int, length.split(":")))
        return time_parts[0] * 60 + time_parts[1] + time_parts[2] / 60

    data["Session Length (minutes)"] = data["Session Length"].apply(session_length_to_minutes)

    # Extract hour and day from Start Time
    data["Hour"] = pd.to_datetime(data["Start Time"], format="%H:%M:%S").dt.hour
    data["Day"] = pd.to_datetime(data["Date"]).dt.date
    data['minute_per_distractions'] = data["Session Length (minutes)"] / data["Distractions"]
    data['minute_per_distractions'] = np.floor(data['minute_per_distractions'].replace([np.inf, -np.inf], 0)).astype(int)
    minute_per_distractions = data['minute_per_distractions']

    # Streamlit App
    st.title("Pomodoro Session Analysis")
    st.write("Analyze the relationship between session length, distractions, and time.")

     # 1. bar Plot: Hours vs Days
    st.subheader("1. Time Of Study")
    days_to_show_1 = st.slider("Select number of days to display ", min_value=1, max_value=len(data), value=30)
    last_n_days_1 = data
    hours_per_day = (last_n_days_1.groupby("Day")["Session Length (minutes)"].sum() / 60)[-days_to_show_1:]
    hours_per_day.index = pd.to_datetime(hours_per_day.index).strftime('%d-%b')
    fig, ax = plt.subplots()
    hours_vs_days= sns.barplot(hours_per_day,  ax=ax)
    hours_vs_days.axhline( y = 10 ,  color = 'red')
    hours_vs_days.text(
            x=len(hours_per_day) // 2,  # Position text in the middle of the x-axis
            y=9.2,                       # Position text at y = 10
            s="اﺮَﺒَﺻ ﻦَﻣﻭ ﻰﻓﻭﺃ ﻦَﻣ َﺪﺠﻤﻟﺍ َﻖﻧﺎﻋﻭ ... ﻢﻫُﺮﺜﻛﺃ َّﻞﻣ ﻰﺘﺣ ﺪﺠﻤﻟﺍ اﻭﺪﺑﺎﻛ",  # Text to display
            color='red',                # Text color
            ha='center',                # Horizontal alignment
            va='bottom',                # Vertical alignment
            fontsize=12,
            fontfamily='Arial' 
        )
    ax.set_title("Hours of study per Day")
    ax.set_xlabel("Days")
    ax.set_ylabel("Total Hours")
    st.pyplot(fig)

    # 2. Scatter Plot: Minutes vs Distractions
    st.subheader("2. Relation Between Session Length (Minutes) and Distractions")
    fig, ax = plt.subplots()
    sns.countplot(x = minute_per_distractions , ax = ax )
    ax.set_title("How long you stays focused before getting distracted ?")
    ax.set_xlabel("Minutes pass before each distraction")
    #ax.set_ylabel("Distractions")
    st.pyplot(fig)

    # 3. Bar Chart: Distractions Over the 24 Hours
    st.subheader("3. Distractions over Hours per Day")
    distractions_by_hour = data.groupby("Hour")["Distractions"].mean()
    fig, ax = plt.subplots()
    distractions_vs_hours = distractions_by_hour.plot(kind="line",  ax=ax)
    distractions_vs_hours.axhline(y = 5 , color = 'red')
    ax.set_title("Mean Distractions by Hour of the Day")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Total Distractions")
    st.pyplot(fig)

    
    # 4. bar Plot: Day vs Distractions
    st.subheader("4. Distractions by Day")
    days_to_show_4 = st.slider("Select number of days to display", min_value=1, max_value=len(data), value=30)    
    distractions_by_day = data.groupby("Day")["minute_per_distractions"].mean()[-days_to_show_4:]
    distractions_by_day.index = pd.to_datetime(distractions_by_day.index).strftime('%d-%b')
    fig, ax = plt.subplots()
    sns.barplot(x = distractions_by_day.index,y =  distractions_by_day, alpha=0.7 ,ax =ax)
    ax.set_title("Minutes pass before distraction by Day ")
    ax.set_xlabel("Days")
    ax.set_ylabel("Distractions")
    st.pyplot(fig)

    

else:
    st.write("CSV file not found!")
