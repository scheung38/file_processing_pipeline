from enum import unique
import pandas as pd
import pandera as pa
from icecream import ic
from iso4217 import Currency
import pycountry
from pathlib import Path

# ic(Currency.usd.country_names)
# ic(Currency.usd.currency_name)

# ic(Currency.gbp.country_names)
# ic(Currency.gbp.currency_name)
# ic(Currency.gbp.code)
# ic(pycountry.countries)

 
def read_and_validate_file(file):

    try:

        if Path(file).suffix == ".csv": 

            test_data = pd.read_csv('data_in/'+file)
            ic('Found csv file!')

        elif Path(file).suffix == ".xlsx":

            test_data = pd.read_excel('data_in/'+file, skiprows=1)
            ic('Found Excel file!')

        else:
            ic('Cannot determine file extension, please check')

        ic(test_data)

        data_sample = test_data.sample(n=4)

        Company = ['GOOG-Google', 'AAPL-Apple', 'TSLA-Tesla', 'NVDA-Nvidia', 'AMZN-Amazon', 'INTC-Intel', 'MSFT-Microsoft', 'ADI-Analog Devices', ]
        Deals = ['Deals-1', 'Deals-2', 'Deals-3', 'Deals-4', 'Deals-5']

        # Defining the schema
        schema = pa.DataFrameSchema({
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
        # transformed_schema = schema.add_columns({
        #     "RowNo" : pa.Column(pa.String),
        #     "AsOfDate" : pa.Column(pa.DateTime),
        #     "ProcessIdentifier" : pa.Column(pa.String, nullable=False),
        #     "RowHash" : pa.Column(pa.Int,   )
        # })
        # But this only appends to end of existing schema

        new_schema = pa.DataFrameSchema({
        "RowNo" : pa.Column(pa.INT8, allow_duplicates=False),
        **schema.columns,
        "AsOfDate" : pa.Column(pa.DateTime),
        "ProcessIdentifier" : pa.Column(pa.INT32, allow_duplicates=False, nullable=False),
        "RowHash" : pa.Column(pa.INT64, allow_duplicates=False)
        })

        # Validating the data
        df_input = schema.validate(data_sample)
        ic(df_input)

        # Validating the transformed_data
        df_output = new_schema.example(size=10) # transformed_schema
        ic(df_output)
        
        df_output.to_csv('data_out/out.csv', sep=',', index=False)
        df_output.to_parquet('data_out/df_output.parquet.gzip', compression='gzip', use_deprecated_int96_timestamps=True)

        return 'File created in data_out/out.csv'

    except Exception as e:
        with open('error_log/error.txt', 'a') as f:
            ic(e)
            f.write(str(e)+'\n')
            return str(e)

if __name__ == '__main__':
    read_and_validate_file('train.csv')
    read_and_validate_file('train.xlsx')

