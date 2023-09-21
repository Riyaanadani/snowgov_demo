import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sample data
data = {
    'Patient_ID': list(range(1, 21)),
    'Measure_Group': ['Breast Cancer', 'Heart Disease', 'TB', 'Blood Pressure'] * 5,
    'Measure_Subgroup': ['Early Detection', 'Prevention', 'Diagnosis', 'Monitoring'] * 5,
    'Year': [2020, 2021, 2022, 2023] * 5,
    'Disease': ['Breast Cancer', 'Heart Disease', 'TB', 'Blood Pressure'] * 5,
    'Test_Undergoes': ['Mammogram', 'Cardiac Screening', 'TB Test', 'BP Monitoring'] * 5,
    'Active': [True, False, True, False] * 5,
    'Inactive': [False, True, False, True] * 5,
    'Total_Members': list(range(1, 21)),
    'Gender': ['Female', 'Male', 'Female', 'Male'] * 5,
    'City': ['City1', 'City2', 'City1', 'City2'] * 5,
}

df = pd.DataFrame(data)

def show_active_data(dataframe):
    st.subheader("Active Records")
    st.write(dataframe[dataframe['Active']])

    # Create a colorful pie chart to show Active vs. Inactive records
    active_counts = dataframe['Active'].sum()
    inactive_counts = dataframe['Inactive'].sum()
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Active', 'Inactive'],
        values=[active_counts, inactive_counts],
        hole=0.4,
        marker=dict(colors=['green', 'red']),
        textinfo='percent+label'
    )])
    fig_pie.update_layout(title_text=f"Active vs. Inactive Records")
    st.plotly_chart(fig_pie)

    # Create a bar chart to show Total Members by Gender
    gender_counts = dataframe.groupby('Gender')['Total_Members'].sum().reset_index()
    fig_bar_gender = px.bar(
        gender_counts,
        x='Gender',
        y='Total_Members',
        color='Gender',
        labels={'Total_Members': 'Total Members'},
        title=f"Total Members by Gender"
    )
    st.plotly_chart(fig_bar_gender)

def show_inactive_data(dataframe):
    st.subheader("Inactive Records")
    st.write(dataframe[dataframe['Inactive']])

# Streamlit app settings
st.set_page_config(
    page_title="Healthcare Dashboard",
    page_icon=":hospital:",
    layout="wide"
)

st.title("Healthcare Dashboard")

# Filters at the top of the screen
col1, col2, col3, col4 = st.columns(4)
selected_year = col1.selectbox("Select Year", df['Year'].unique())
selected_gender = col2.selectbox("Select Gender", ['All'] + df['Gender'].unique().tolist())
selected_measure_group = col3.selectbox("Select Measure Group", df['Measure_Group'].unique())
selected_measure_subgroup = col4.selectbox("Select Measure Subgroup", df['Measure_Subgroup'].unique())

# Filter the data based on selected filters
filtered_data = df[
    (df['Year'] == selected_year) &
    (df['Gender'] == selected_gender if selected_gender != 'All' else True) &
    (df['Measure_Group'] == selected_measure_group) &
    (df['Measure_Subgroup'] == selected_measure_subgroup)
]

# Show Active or Inactive Data using buttons
if st.button("Show Active"):
    show_active_data(filtered_data)
elif st.button("Show Inactive"):
    show_inactive_data(filtered_data)
else:
    # Display the filtered data
    st.subheader("Filtered Data")
    st.write(filtered_data)
