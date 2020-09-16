import pandas as pd
import streamlit as st
import math
import pydeck as pdk


#reading in query table to get 5 line sample data
queries = pd.read_csv('/Users/chrisbaugh/Downloads/rubipy - Query Table (2).csv')

sidebar_selector = st.sidebar.selectbox('Page View', ['Query Repo','Scheduler', 'Map', 'Well Map'])


#group values by category, then sort so category with largest number of queries is first
query_titles = queries.groupby('category')[['query_uuid']].count()
query_titles.sort_values(by='query_uuid',inplace=True, ascending=False)

st.set_option('deprecation.showfileUploaderEncoding', False)
submit = False

if sidebar_selector == 'Query Repo':
    st.title('Query Repository')
    for index, values in query_titles.iterrows():
        st.header(index)
        temp_df = queries[queries['category'] == index]
        for index, row in temp_df.iterrows():
            st.markdown('**' + row['query_name'] +'**' + ' - ' +  row['query_uuid'])
            #st.write(row['query_name'], '-', row['query_uuid'])
            #sql_button = st.checkbox('SQL', key=row['query_name'])
            #if sql_button:
             #   st.write(row['SQL'])
            sample_data = st.checkbox('Sample Data', key=row['query_uuid'])
            if sample_data:
                st.write(row['json_data'])

if sidebar_selector == 'Scheduler':
    st.title('Scheduler')
    query_uuid = st.text_input('Query UUID')
    sheet_link = st.text_input('Google Sheet Link')
    tab_name = st.text_input('Tab Name')
    job_frequency = st.radio('Job Frequency', ['Daily', 'Weekly'])
    if job_frequency == 'Weekly':
        day_frequency = st.radio('Select Day', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    submit = st.button('Submit')
    if submit:
        st.title('Your job is now scheduled, please reload page to schedule more jobs')
        #kick off cloud function cloud_function(query_uuid, sheet_link, tab_name, job_frequency, day_frequency)



if sidebar_selector == 'Map':
    st.title('Map Upload')
    map_data = st.file_uploader('File Upload',multiple_files=False)
    if map_data == None:
        pass
    else:
        map_data = pd.read_csv(map_data)
        map_data = map_data.dropna()
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=30.263397,
                longitude=-97.744575,
                zoom=5,
                pitch=30,
            ),
            layers=[
                pdk.Layer(
                    'HexagonLayer',
                    data=map_data,
                    get_position='[lon, lat]',
                    radius=20000,
                    elevation_scale=20,
                    elevation_range=[0, 10000],
                    pickable=True,
                    extruded=True,
                )
            ]
        ))

if sidebar_selector == 'Well Map':
    st.title('Well Map')
