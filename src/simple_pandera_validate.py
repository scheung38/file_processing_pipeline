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
test_data = pd.read_csv('src/train.csv')

# print(type(test_data)) // <class 'pandas.core.frame.DataFrame'>
ic(test_data)

# Taking a subsample
# data_sample = data.sample(n=3, random_state = 999)
data_sample = test_data.sample(n=10)

Company = ['GOOG-Google', 'AAPL-Apple', 'TSLA-Tesla', 'NVDA-Nvidia', 'AMZN-Amazon', 'INTC-Intel', 'MSFT-Microsoft', 'ADI-Analog Devices', ]
Deals = ['Deals-1', 'Deals-2', 'Deals-3', 'Deals-4', 'Deals-5']
# Defining the schema
schema = pa.DataFrameSchema({

    # "Id" : pa.Column(pa.Int, nullable=False),
    # "Date" : pa.Column(pa.DateTime),
     

    "DealName" : pa.Column(pa.String, checks=pa.Check.isin(
                [deal for deal in list(Deals)]), required=True, nullable=False),
    
    "D1" : pa.Column(pa.Float64, required=True),
    "D2" : pa.Column(pa.Float64, nullable=True, required=False),
    "D3" : pa.Column(pa.Float64, nullable=True, required=False),
    "D4" : pa.Column(pa.Float64, nullable=True, required=False),
    "D5" : pa.Column(pa.Float64, nullable=True, required=False),
    
    "IsActive" : pa.Column(pa.Bool, nullable=True, required=False),

    "CountryName" : pa.Column(pa.String, checks=pa.Check.isin(
                [country.name for country in list(pycountry.countries)]), required=True),
 
    "CountryCode" : pa.Column(pa.String, checks=pa.Check.isin(
                [country.alpha_2 for country in list(pycountry.countries)]), required=True),

    "CurrencyName" : pa.Column(pa.String, checks=pa.Check.isin(
                [currency.name for currency in list(pycountry.currencies)]), required=True),

    "CurrencyCode" : pa.Column(pa.String, checks=pa.Check.isin(
                [currency.alpha_3 for currency in list(pycountry.currencies)]), required=True),

    "Company" : pa.Column(pa.String, checks=pa.Check.isin(
                [company for company in list(Company)]), required=True),

})


example_input = schema.example(size=10)
ic(example_input)



# Transformed schema
transformed_schema = schema.add_columns({
    "RowNo" : pa.Column(pa.String),
    "AsOfDate" : pa.Column(pa.DateTime),
    "ProcessIdentifier" : pa.Column(pa.String, nullable=False),
    "RowHash" : pa.Column(pa.Int,   )
})



# Validating the data
df_input = schema.validate(data_sample)
ic(df_input)

# Validating the transformed_data
df_output = transformed_schema.example(size=10)
ic(df_output)
 
