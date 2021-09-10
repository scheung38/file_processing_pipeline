import pytest
from pathlib import Path
from icecream import ic

from src.simple_pandera_validate import read_and_validate_csv_file

 
def test_can_process():
    out_csv = read_and_validate_csv_file('train.csv')
    ic(out_csv)
    assert 'File created in data_out/out_csv' == out_csv

def test_no_file_found():
    out_csv = read_and_validate_csv_file('XXXtrain.csv')
    ic(out_csv)
    assert "[Errno 2] No such file or directory: 'data_in/XXXtrain.csv'" == out_csv

def test_with_bad_format():
    out_csv = read_and_validate_csv_file('train_bad_format.csv')
    ic(out_csv)
    assert 'File created in data_out/out_csv' != out_csv
 