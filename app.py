from pandas.io.parsers import read_csv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
import numpy as np


plt.style.use('seaborn')

@st.cache
def load_data():
    data= read_csv("Unemployment in India.csv",parse_dates=[' Date'],dayfirst=True)
    clean_cols = [col.strip() for col in data.columns.tolist()]
    data.columns = clean_cols
    return data

st.title("Unemployment in India")
st.sidebar.header("Project Options")

options = [
            "Overview",
            "Timeline analysis",
            "Estimated Unemployment Rate",
            "Estimated Employed",
            "Region"]

choice = st.sidebar.selectbox("select an option",options)

data = load_data()
# st.write(data.columns.tolist())
if choice == options[0]:
    st.image("unemployment.jpg")
    st.info('''One of the major social issues in India is unemployment.As the Indian labour laws are inflexible and restrictive, and its infrastructure is poor, which is actually the main reason for India’s unemployment situation, according to The Economist. As of September 2018, according to the Indian Government, India had 31 million jobless people. The scenario of Assam, in the case of unemployment, is also worst. As per statistics made available by the state Skill Employment and Entrepreneurship department, the total numbers of registered employed in the state is 19,63,376; of them, 16,65,866 are educated or skilled ones and  2,97,510 unskilled ones. ''')
    fig,ax = plt.subplots()
    data.hist(edgecolor="black",linewidth = 1.2 , figsize=(10,10),ax=ax)
    st.pyplot(fig)
    
elif choice == options[1]:
    color=st.sidebar.color_picker("select graph color")
    state = st.sidebar.radio("select a state",data.Region.unique().tolist())
    try:
        fig,ax = plt.subplots()
        data_state = data[data['Region']==state].set_index('Date')['Estimated Unemployment Rate (%)']
        data_state.resample('M').sum().plot(kind='line',style='o--',figsize=(15,5),ax=ax,color=color)
        plt.title(f'UNEMPLOYMENT in {state}', fontsize = '11',color = 'c')
        
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Please ask the admin {e}")

elif choice == options[2]:
    fig,ax = plt.subplots()
    data.groupby(['Region'])['Estimated Unemployment Rate'].sum().reset_index().sort_values(by='Estimated Unemployment Rate').tail(10).plot(kind='bar',x='Region',figsize=(15,10),ax=ax)
    st.pyplot(fig)

elif choice == options[3]:
    fig,ax = plt.subplots()
    data.columns = ["States","Date","Frequency",
                "Estimated Unemployment Rate",
                "Estimated Employed",
                "Estimated Labour Participation Rate",
                "Region"]
    plt.title("Indian Unemployment")
    sns.histplot(x="Estimated Employed",hue="Region",data=data,ax=ax)
    st.pyplot(fig)

elif choice == options[4]:
    fig,ax = plt.subplots()
    data.hist(edgecolor="black",linewidth = 1.2 , figsize=(10,10),ax=ax)
    d = data.Region.value_counts().head(10)                 
    plt.figure(figsize=(10,10))
    x = list(d.index)
    y = list(d.values)
    x.reverse()
    y.reverse()
    plt.title("Estimated Unemployment in Regions")
    plt.ylabel("Unemployment Count")
    plt.xlabel("Regions")
    plt.bar(x,y)
    st.pyplot(fig)


elif choice == options[5]:
    fig,ax = plt.subplots()
    data.groupby(['Region'])['Estimated Unemployment Rate'].sum().reset_index().sort_values(by='Estimated Unemployment Rate').tail(10).plot(kind='bar',x='Region',figsize=(15,10))
    st.pyplot(fig)

