import pytest
from pathlib import Path
from icecream import ic

from src.main import read_and_validate_file

 
def test_can_process():
    out_csv = read_and_validate_file('train.csv')
    ic(out_csv)
    assert 'File created in data_out/out.csv' == out_csv

def test_no_csv_file_found():
    out_csv = read_and_validate_file('XXXtrain.csv')
    ic(out_csv)
    assert "[Errno 2] No such file or directory: 'data_in/XXXtrain.csv'" == out_csv

def test_can_process_excel():
    out_csv = read_and_validate_file('train.xlsx')
    ic(out_csv)
    assert 'File created in data_out/out.csv' == out_csv    