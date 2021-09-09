import pytest

from simple_pandera_validate import read_and_validate_csv_file

def test():
    assert read_and_validate_csv_file('train.csv').exists()