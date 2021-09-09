from enum import unique
import pandas as pd
import pandera as pa
from icecream import ic
from iso4217 import Currency
import pycountry

ic(Currency.usd.country_names)
ic(Currency.usd.currency_name)

ic(Currency.gbp.country_names)
ic(Currency.gbp.currency_name)
ic(Currency.gbp.code)
ic(pycountry.countries)

 
# Loading the data:
# data = pd.read_csv('./train.csv', parse_dates=['Date'])
data = pd.read_csv('src/train.csv')

# Taking a subsample
# data_sample = data.sample(n=3, random_state = 999)
data_sample = data.sample(n=10)

 

# Defining the schema
schema = pa.DataFrameSchema({

    # "Id" : pa.Column(pa.Int, nullable=False),
    # "Date" : pa.Column(pa.DateTime),
    
    "DealName" : pa.Column(pa.String, required=True, nullable=False),
    
    "D1" : pa.Column(pa.Float64, required=True),
    "D2" : pa.Column(pa.Float64, required=False),
    "D3" : pa.Column(pa.Float64, required=False),
    "D4" : pa.Column(pa.Float64, required=False),
    "D5" : pa.Column(pa.Float64, required=False),
    
    "IsActive" : pa.Column(pa.Bool, nullable=True, required=False),
   
    "Country" : pa.Column(pa.String, checks=pa.Check.isin(
                [country.alpha_2 for country in list(pycountry.countries)]), required=False),
    "Currency" : pa.Column(pa.String, checks=pa.Check.isin(
                [currency.alpha_3 for currency in list(pycountry.currencies)]), required=False),

    "Company" : pa.Column(pa.String, required=True),

})


example = schema.example(size=3)
ic(example)



# Transformed schema
transformed_schema = schema.add_columns({
    "RowNo" : pa.Column(pa.String),
    "AsOfDate" : pa.Column(pa.DateTime),
    "ProcessIdentifier" : pa.Column(pa.String, nullable=False),
    "RowHash" : pa.Column(pa.Int)
})



# Validating the data
df_input = schema.validate(data_sample)
ic(df_input)




# Validating the transformed data
transformed_schema.validate(data)

