import pandas as pd
import streamlit as st
import plotly_express as px
from data_preprocess import preprocess

df = pd.read_csv("vehicles_us.csv")
# Preprocess
df = preprocess(df)

# Streamlit part
# Data table
st.header('Data viewer')
st.dataframe(df)

# checkbox
hist_plot = st.checkbox('Show Histograms')
scatter_plot = st.checkbox("Show Scatters")
# Histograms
if hist_plot:
    st.header("Vehicle types by manufacturer")
    fig = px.histogram(df, x='make', color='type')
    st.write(fig)

    st.header("Histogram of `condition` vs `model_year`")
    fig = px.histogram(df, x='model_year', color='condition')
    st.write(fig)

    st.header("Compare price distribution between manufacturers")
    manufact_list = sorted(df['make'].unique())
    manufacturer_1 = st.selectbox(
        label='Select manufacturer 1',
        options=manufact_list,
        index=manufact_list.index("chevrolet")
    )
    manufacturer_2 = st.selectbox(
        label='Select manufacturer 2',
        options=manufact_list,
        index=manufact_list.index("hyundai")
    )

    mask_filter = (df['make'] == manufacturer_1) | (df['make'] == manufacturer_2)
    df_filtered = df[mask_filter]

    normalize = st.checkbox("Normalize histogram", value=True)
    if normalize:
        histnorm = 'percent'
    else:
        histnorm = None

    fig = px.histogram(df_filtered, x='price', nbins=30, color='make', histnorm=histnorm, barmode='overlay')
    st.write(fig)

# Scatter
if scatter_plot:
    st.header("Price distribution by `model_year` and `model`")
    model_list = sorted(df['model'].unique())
    model_selectbox = st.selectbox(
        label='Select model',
        options=model_list,
        index=model_list.index(model_list[0])
    )

    fig = px.scatter(df[df['model'] == model_selectbox], x='model_year', y='price')
    st.write(fig)