# Project Destription

This project is a demo of Streamlit. I analyzed a table of used car's price and display some plots via Streamlit.

The URL is https://tossprob.onrender.com/

There is a data frame to show the details of data.

There are two check-boxes: `Show Histograms` and `Show Scatters`. If click these check-boxes, the associated plots will display on the page.

# Code explaination: `app.py`

## Data Preprocess

1. Clean data:
    * Data type
    * Missing values
    * Duplicates
    * Check outliers

2. Enrich data:
    * Break down the `model` into `make` and `model`

## Analysis by plots

### Histogram

1. Vehicle types by manufacturer

2. Histogram of `condition` vs `model_year`

3. Compare price distribution between manufacturers

### Scatters

1. Price distribution by `model_year` and `model`

# The project structure
$ tree
.
├── README.md
├── app.py
├── vehicles_us.csv
└── notebooks
    └── EDA.ipynb
└── .streamlit
    └── config.toml 