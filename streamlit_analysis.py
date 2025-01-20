import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

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

    # Convert 'Start Time' to datetime
    data["Start Time"] = pd.to_datetime(data["Start Time"], format="%H:%M:%S")

    # Extract hour and day from Start Time
    data["Hour"] = data["Start Time"].dt.hour
    data["Day"] = data["Start Time"].dt.date

    # Streamlit App
    st.title("Pomodoro Session Analysis")
    st.write("Analyze the relationship between session length, distractions, and time.")

    # 1. Scatter Plot: Minutes vs Distractions
    st.subheader("1. Relation Between Session Length (Minutes) and Distractions")
    fig, ax = plt.subplots()
    ax.scatter(data["Session Length (minutes)"], data["Distractions"], color="blue", alpha=0.7)
    ax.set_title("Minutes vs Distractions")
    ax.set_xlabel("Session Length (Minutes)")
    ax.set_ylabel("Distractions")
    st.pyplot(fig)

    # 2. Bar Chart: Distractions Over the 24 Hours
    st.subheader("2. Distractions by Hour of Day")
    distractions_by_hour = data.groupby("Hour")["Distractions"].sum()
    fig, ax = plt.subplots()
    distractions_by_hour.plot(kind="bar", color="orange", ax=ax)
    ax.set_title("Total Distractions by Hour of the Day")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Total Distractions")
    st.pyplot(fig)

    # 3. Scatter Plot: Day vs Distractions
    st.subheader("3. Distractions by Day")
    distractions_by_day = data.groupby("Day")["Distractions"].sum()
    fig, ax = plt.subplots()
    ax.scatter(distractions_by_day.index, distractions_by_day, color="green", alpha=0.7)
    ax.set_title("Distractions by Day")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Distractions")
    plt.xticks(rotation=45)
    st.pyplot(fig)

else:
    st.write("CSV file not found!")
