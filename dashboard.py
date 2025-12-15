import requests
import json
import pandas as pd
import streamlit as st

#load csv
df = pd.read_csv("data/bls_data.csv")


#title 
st.set_page_config(page_title="U.S. Labor Market Dashboard",  layout="wide")  
st.markdown("<h1 style='text-align: center;'>U.S. Labor Market Dashboard</h1>",unsafe_allow_html=True)  
st.divider()                

#total non farm series
seriesID = 'CEU0000000001'
total_nonfarm = df[df["seriesID"] == seriesID].copy()


# Visualize Total Farm

#make columns for the graph and filters
left_column, right_column = st.columns([2,5])
#add filters for year
with left_column:
    st.write("")  #adding spacer on page
    st.write("")  
    st.write("") 
    st.write("")
    st.write("")
    st.write("")  
    st.write("")  
    years = sorted(df['year'].unique())
    selected_years = st.multiselect("Year", options=years, default=years, key = "tf_years")  #creating filters for the years
    total_nonfarm = total_nonfarm[total_nonfarm["year"].isin(selected_years)]

#create chart
with right_column:
    st.header('Total Nonfarm Employees by Month, Undadjusted', anchor=None, help=None, width="stretch", text_alignment="center")
    st.line_chart(total_nonfarm, x = 'date', y = 'value', x_label = "Date", y_label = 'Value (thousands)')

st.divider()                

# Unemployment
seriesID = 'LNU04000000'
unemployment = df[df["seriesID"] == seriesID].copy()

#Visualize unemployment

#make columns for the graph and filters
left_column, right_column = st.columns([2,5])
with left_column:
    st.write("")  # vertical spacers
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    years = sorted(df["year"].unique())
    selected_years_unemp = st.multiselect("Year", options=years,default=years,key="unemp_years")  #creating filters for the years
    unemployment = unemployment[unemployment["year"].isin(selected_years_unemp)]

with right_column:
    st.header('Total National Unemployment by Month, Unadjusted', anchor=None, width="stretch",text_alignment="center")
    st.line_chart(unemployment, x='date', y='value', x_label="Date", y_label='Value (percent)')

st.divider()                


#Average Wage series
seriesID = 'CEU0500000003'
avgWage = df[df["seriesID"] == seriesID].copy()

# Visualize Average Wage

#create columns for visual and filters
left_column, right_column = st.columns([2,5])
with left_column:
    st.write("")  # vertical spacers
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    years = sorted(df["year"].unique())
    selected_years_wage = st.multiselect("Year",options=years,default=years,key="avg_wage_years")  #creating filters for the years
    avgWage = avgWage[avgWage["year"].isin(selected_years_wage)]

with right_column:
    st.header('Average Hourly Earnings of All Employees, Unadjusted',anchor=None,width="stretch",text_alignment="center")
    st.line_chart(avgWage, x='date', y='value', x_label="Date", y_label='Value ($)')

st.divider()                

# Consumer Price Index series
seriesID = 'CUUR0000SA0L1E'
CPI = df[df["seriesID"] == seriesID].copy()

# Visualize CPI

#create columns for chart and for filters
left_column, right_column = st.columns([2,5])
with left_column:
    st.write("")  # vertical spacers
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    years = sorted(df["year"].unique())
    selected_years_cpi = st.multiselect("Year",options=years,default=years,key="cpi_years") #creating filters for the years
    CPI = CPI[CPI["year"].isin(selected_years_cpi)]

with right_column:
    st.header('Consumer Price Index. All items less food and energy in U.S. city average, all urban consumers, not seasonally adjusted',anchor=None,width="stretch",text_alignment="center")
    st.line_chart(CPI, x='date', y='value', x_label="Date", y_label='Value')