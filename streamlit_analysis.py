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

    # Convert session length to minutes and session start time to datetime
    def session_length_to_minutes(length):
        time_parts = list(map(int, length.split(":")))
        return time_parts[0] * 60 + time_parts[1] + time_parts[2] / 60

    data["Session Length (minutes)"] = data["Session Length"].apply(session_length_to_minutes)

    # Extract hour and day from Start Time
    data["Hour"] = pd.to_datetime(data["Start Time"], format="%H:%M:%S").dt.hour
    data["Day"] = pd.to_datetime(data["Date"]).dt.date

    minute_per_distractions = data["Session Length (minutes)"] / data["Distractions"]
    minute_per_distractions = np.floor(minute_per_distractions.replace([np.inf, -np.inf], 0)).astype(int)
    # Streamlit App
    st.title("Pomodoro Session Analysis")
    st.write("Analyze the relationship between session length, distractions, and time.")

     # 1. bar Plot: Hours vs Days
    st.subheader("1. Time Of Study")
    days_to_show_4 = st.slider("Select number of days to display ", min_value=1, max_value=len(data), value=30)
    last_n_days_4 = data[-days_to_show_4:]

    hours_per_day = last_n_days_4.groupby("Day")["Session Length (minutes)"].sum() / 60
    fig, ax = plt.subplots()
    hours_per_day.plot(kind="bar",  ax=ax)
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
    distractions_by_hour.plot(kind="line",  ax=ax)
    ax.set_title("Mean Distractions by Hour of the Day")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Total Distractions")
    st.pyplot(fig)

    
    # 4. bar Plot: Day vs Distractions
    st.subheader("4. Distractions by Day")
    days_to_show_3 = st.slider("Select number of days to display", min_value=1, max_value=len(data), value=30)

    sub_data = data.sort_values(by=['Date'] ).copy()
    last_n_days_3 = sub_data[-days_to_show_3:]
    
    last_n_days_3['minute_per_distractions'] = last_n_days_3["Session Length (minutes)"] / last_n_days_3["Distractions"]
    last_n_days_3['minute_per_distractions'] = np.floor(last_n_days_3['minute_per_distractions'].replace([np.inf, -np.inf], 0)).astype(int)
    distractions_by_day = last_n_days_3.groupby("Day")["minute_per_distractions"].mean()
    fig, ax = plt.subplots()
    sns.barplot(x = distractions_by_day.index,y =  distractions_by_day, alpha=0.7 ,ax =ax)
    ax.set_title("Minutes pass before each distraction by Day ")
    ax.set_xlabel("Days")
    ax.set_ylabel("Distractions")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    

else:
    st.write("CSV file not found!")
