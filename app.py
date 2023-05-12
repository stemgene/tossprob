import pandas as pd
import streamlit as st
import plotly_express as px

df = pd.read_csv("vehicles_us.csv")
# Preprocess

# Proprocess -- Missing values
df['model_year'] = df['model_year'].fillna(df['model_year'].mode()[0])
df['cylinders'] = df['cylinders'].fillna(df['cylinders'].median())
df['odometer'] = df['odometer'].fillna(df['odometer'].mean())
df['paint_color'] = df['paint_color'].fillna(df['paint_color'].mode()[0])
df['is_4wd'] = df['is_4wd'].fillna(0.0)
# Preprocess -- extract manufacturer
df['make'] = df['model'].apply(lambda x: x.split()[0])
# Preprocess -- data type
df['model_year'] = pd.to_datetime(df['model_year'].astype(int).astype(str), format='%Y').dt.year
df['date_posted'] = pd.to_datetime(df['date_posted'])
df['is_4wd'] = df['is_4wd'].apply(lambda x: 'yes' if x == 1.0 else 'no')
# Preprocess -- duplicates
def replace_wrong_values(df, col, replace_dict): 
    for key, value in replace_dict.items(): 
        df[col] = df[col].replace(key, value)
        
replace_dict = {"ford f150": 'ford f-150', 'ford f250': 'ford f-250', 'ford f250 super duty': 'ford f-250 super duty'}
replace_wrong_values(df, 'model',  replace_dict)
# Preprocess -- outliers
df['price'] = df.loc[((df['price'] > 1000) & (df['price'] < 300000)), 'price'] 
df['model_year'] = df.loc[(df['model_year'] > 1960), 'model_year']
df['odometer'] = df.loc[((df['odometer'] < 700000) & (df['odometer'] > 10)), 'odometer']

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