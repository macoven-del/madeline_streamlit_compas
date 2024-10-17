import sys

sys.path[-1]

import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

compas_raw_data = pd.read_csv('/Users/macoven/Desktop/Precross/COMPAS/cox-violent-parsed.csv', sep = ",")
compas_data = compas_raw_data.drop(['name', 'first', 'last', 'dob', 'decile_score.1', 'priors_count.1'], axis = 1)
compas_data = compas_data.dropna()
priors_count = np.array(compas_data['priors_count'])         
compas_data['term'] = (compas_data['end'] - compas_data['start'])
dropdown_options = np.array(compas_data['c_charge_desc'].unique())
alt.data_transformers.disable_max_rows()

brush = alt.selection_interval()
input_dropdown = alt.binding_select(options=dropdown_options, name='Charge ')
selection = alt.selection_point(fields=['c_charge_desc'], bind=input_dropdown)
points = alt.Chart(compas_data, title = 'COMPAS Violence Risk Score By Age and Race').mark_circle(size = 60).encode(
    x='race',
    y='age',
    color='v_decile_score',
    tooltip=['term', 'c_charge_desc', 'v_score_text', 'priors_count']
).add_params(
    brush,
    selection
).transform_filter(
    selection
).properties(height=200, width=400)

bars = alt.Chart(compas_data).mark_bar().encode(
    alt.X('count()'),
    alt.Y('sex'),
    alt.Color('sex')
).transform_filter(
    selection
).add_params(
    selection
)

charts = points & bars
st.altair_chart(charts, use_container_width=False)

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from st_mongo_connection import MongoDBConnection

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["connections.mongo"])

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)

uri = "mongodb+srv://mcoven:xSg8CzzAgQXjd973@census-topic-mining-clu.cd5ab.mongodb.net/?retryWrites=true&w=majority&appName=census-topic-mining-cluster"

# Create a new client and connect to the server
#client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
