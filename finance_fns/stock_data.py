from collections.abc import Callable
from pandas.core import frame

import pandas as pd
import datetime
import os

import FinanceDataReader as fdr


def get_today() -> tuple[str, str, str]:
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day
    return year, month, day


def is_file_in(file_name: str) -> bool:
    year, month, day = get_today()
    csv_file_name = f"{file_name}_{year}_{month}_{day}.csv"
    return os.path.isfile(csv_file_name)


def make_stock_list(file_name: str) -> frame.DataFrame:
    year, month, day = get_today()
    csv_file_name = f"{file_name}_{year}_{month}_{day}.csv"
    if is_file_in(file_name):
        # print(f"File {csv_file_name} exists, skipping.")
        krx_df = pd.read_csv(csv_file_name)
    else:
        # print(f"File {csv_file_name} does not exist, creating it.")
        krx_df = fdr.StockListing("krx")
        # with 구문을 사용해 파일을 명시적으로 열고 닫아준다.
        with open(csv_file_name, "w", newline="", encoding="utf-8") as f:
            krx_df.to_csv(f, index=False)

    return krx_df


def get_head(items: list) -> str:
    """
    리스트의 첫 번째 요소를 반환한다.
    리스트가 비어있다면 ValueError를 발생시킨다.
    """
    if items is None or len(items) == 0:
        raise ValueError("The list is empty, cannot get head.")
    return items[0]


def double(fn: Callable) -> Callable:
    return lambda *args: fn(fn(*args))


def find_by_name(name: str) -> frame.DataFrame:
    stock_list = make_stock_list("krx_df")
    ser = stock_list["Name"] == name

    stock = stock_list[ser]
    if len(stock) == 0:
        raise ValueError("No stock found")
    return stock


def get_symbol(df: frame.DataFrame) -> str:
    get_double_head = double(get_head)
    if len(df.values) > 0:
        return get_double_head(df.values)
    else:
        raise ValueError("No stock found")


# 메인 함수
def find_code(name: str) -> str:
    df = find_by_name(name)
    return get_symbol(df)


def get_close_df(stock_code: str, start_date: str, end_date: str = None) -> frame.DataFrame:
    try:
        if end_date is None:
            df = fdr.DataReader(stock_code, start_date)
        else:
            df = fdr.DataReader(stock_code, start_date, end_date)

    except Exception as e:
        print(f"Error: {e}")

    return df[['Close']]


def add_to_df(df: frame.DataFrame) -> Callable[[str, Callable], frame.DataFrame]:
    df = df.copy()  # 원래 df에 영향을 미치지 않도록 함

    def adder(name: str, fn: Callable) -> frame.DataFrame:
        df[name] = fn(df)
        return df

    return adder


def get_filtered_df(df: frame.DataFrame) -> Callable[[Callable[[frame.DataFrame], bool]], frame.DataFrame]:
    new_df = df.copy()
    return lambda fn: new_df[fn(new_df)]


if __name__ == "__main__":
    stock_code = find_code('CJ제일제당')
    print(f"{stock_code=}")
    df = fdr.DataReader(symbol=stock_code, start='2024-10')
    print(df)
