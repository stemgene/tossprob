import pandas as pd

def preprocess(df):
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
    
    return df