"""
A file to set up the streamlit dashboard needed for 11/14 stats lab.
"""

import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sqlite3

# Connect to SQLite
conn = sqlite3.connect("db/responses.db")
c = conn.cursor()


# functions to interact with db
def insert_response(height, money, color):
    with conn:
        c.execute("INSERT INTO responses (height, money, color) VALUES (?, ?, ?)",
                  (height, money, color))


def fetch_responses():
    c.execute("SELECT * FROM responses")
    data = c.fetchall()
    return pd.DataFrame(data, columns=["id", "height", "money", "color"])


# Text on dashboard
st.title("11/14 Stats Lab")
st.write("Please answer the following questions.")

height_q = st.number_input("What is your height in inches?", min_value=50,
                           max_value=84)
money_q = st.number_input("You are partnered with an anonymous person who you\
                           cannot see or speak to. You are given $10 and are\
                           told that you can send any amount of that money\
                           to your partner. The money you send them will be\
                           tripled in value. After they receive the money\
                           they have the option of sending some back to you\
                           (however they can also send back nothing).\
                           Your partner knows how much money you were given\
                           to start with. How much do you send them?",
                           min_value=0.0, max_value=10.0, step=1., format="%.2f")
color_q = st.radio("What's your favorite color?", ["red", "green", "blue"])

# dictionary to associate data
data = {
    "height": height_q,
    "money": money_q,
    "color": color_q
}

# Submit Button
if st.button("Submit"):
    insert_response(**data)
    st.success("Thank you for your response!")

    # Fetch Data if submitted
    df = fetch_responses()

    # Export data to CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download responses as CSV",
        data=csv,
        file_name="responses.csv",
        mime="text/csv"
    )

    st.header("Everyone else's responses...")

    # Height histogram
    st.subheader("Histogram of Height (Continuous) in Synchrony '24")
    fig, ax = plt.subplots()
    ax.hist(df["height"], bins=10, edgecolor='black')
    ax.set_xlabel("Height")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Money histogram
    st.subheader("Histogram of Money Response (Continuous) in Synchrony '24")
    fig, ax = plt.subplots()
    ax.hist(df["money"], bins=10, edgecolor='black')
    ax.set_xlabel("Amount Given")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Color bar-plot
    st.subheader("Barplot of favorite colors (Categorical) in Synchrony '24")
    fig, ax = plt.subplots()
    ax.bar(df["color"].value_counts().index,
           df["color"].value_counts().values,
           color=["green", "blue", "red"])
    ax.set_xlabel("Color")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Color pie-chart
    st.subheader("Pie-Chart of favorite colors (Categorical) in Synchrony '24")
    fig, ax = plt.subplots()
    ax.pie(df["color"].value_counts().values, labels=df["color"].value_counts().index)
    st.pyplot(fig)

    # height vs money scatter plot
    st.subheader("Scatter Plot of height vs money given Synchrony '24")
    fig, ax = plt.subplots()
    ax.scatter(df["height"], df["money"])
    ax.set_xlabel("Height")
    ax.set_ylabel("Money")
    st.pyplot(fig)

    # color vs money boxplot
    st.subheader("Boxplot of favorite colors vs money in Synchrony '24")
    fig, ax = plt.subplots()
    ax = sns.boxplot(x="color", y="money", data=df)
    ax.set_xlabel("Color")
    ax.set_ylabel("Amount Given")
    st.pyplot(fig)


conn.close()
