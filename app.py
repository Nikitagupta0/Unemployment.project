from pandas.io.parsers import read_csv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
import numpy as np
import plotly.express as px


plt.style.use('seaborn')

@st.cache
def load_data():
    data= read_csv("Unemployment in India.csv",parse_dates=[' Date'],dayfirst=True)
    clean_cols = [col.strip() for col in data.columns.tolist()]
    data.columns = clean_cols
    data.columns = ["States","Date","Frequency",
                "Estimated Unemployment Rate",
                "Estimated Employed",
                "Estimated Labour Participation Rate",
                "Region"]
    return data

st.title("Unemployment in India")
st.sidebar.header("Project Options")

options = [
            "Overview",
            "Timeline analysis",
            "Unemployment Rate",
            "Estimated Employed",
            "Region wise"]

choice = st.sidebar.selectbox("select an option",options)

data = load_data()
# st.write(data.columns.tolist())
if choice == options[0]:
    st.image("unemployment.jpg")
    st.info('''One of the major social issues in India is unemployment.As the Indian labour laws are inflexible and restrictive, and its infrastructure is poor, which is actually the main reason for India’s unemployment situation, according to The Economist. 
    As of September 2018, according to the Indian Government, India had 31 million jobless people. The scenario of Assam, in the case of unemployment, is also worst. As per statistics made available by the state Skill Employment and Entrepreneurship department, the total numbers of registered employed in the state is 19,63,376; of them, 16,65,866 are educated or skilled ones and  2,97,510 unskilled ones. ''')
    st.write(data)
    
elif choice == options[1]:
    statelist = data.Region.unique().tolist()
    statelist = [str(v) for v in statelist]
    statelist.sort()
    statelist.pop()
    # st.write(statelist)
    state = st.selectbox("select a state",statelist)
    try:
        fig,ax = plt.subplots()
        data_state = data[data['Region']==state].set_index('Date')['Estimated Unemployment Rate']
        state_data = data_state.resample('M').sum()
        fig = px.line(state_data, y= "Estimated Unemployment Rate")
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Please ask the admin {e}")

elif choice == options[2]:
    fig,ax = plt.subplots()
    op = st.selectbox("select a category",["Estimated Unemployment Rate","Estimated Employed","Estimated Labour Participation Rate"])
    data.groupby(['States'])[op].sum().reset_index().sort_values(by=op).tail(10).plot(kind='bar',x='States',figsize=(15,10),ax=ax)
    st.pyplot(fig)

elif choice == options[3]:
    fig,ax = plt.subplots()
    
    plt.title("Indian Unemployment")
    fig = px.histogram(data,x="Estimated Employed")
    st.plotly_chart(fig)

elif choice == options[4]:
    fig,ax = plt.subplots()
    op = st.selectbox("select a category",["Estimated Unemployment Rate","Estimated Employed","Estimated Labour Participation Rate"])
    data.groupby(['Region'])[op].sum().reset_index().sort_values(by=op).tail(10).plot(kind='bar',x='Region',figsize=(15,10),ax=ax)
    st.pyplot(fig)