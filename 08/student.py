import numpy as np
import pandas as pd
from scipy import stats
import sys, csv, json, math
from datetime import datetime
from datetime import timedelta


def calc_dates(slope):
    if slope == 0:
        return float("inf"), float("inf")
    date_start = datetime.strptime('2018-09-17', "%Y-%m-%d")
    date_sixteen = (date_start + timedelta(days=math.floor((16 / slope)))).date()
    date_twenty = (date_start + timedelta(days=math.floor((20 / slope)))).date()
    return date_sixteen, date_twenty

def calc_slope(row):
    days_start = datetime.strptime('2018-09-17', "%Y-%m-%d").timetuple().tm_yday
    x = []
    for date in row.columns:
        days_actual = datetime.strptime(date, "%Y-%m-%d").timetuple().tm_yday
        difference = days_actual - days_start
        x.append(difference)
    x = np.array(x)
    y = np.array(row.values[0])
    x = x[:,np.newaxis]
    a, _, _, _ = np.linalg.lstsq(x, y, rcond=None)
    return a[0]

def merge_excercises(stats):
    pat = '(^student$|\d+$)'
    extracted = stats.columns.str.extract(pat, expand=False)
    grouped = stats.groupby(extracted, axis=1).sum()
    grouped = grouped.groupby(['student'], axis=0).sum()
    return grouped

def merge_dates(stats):
    pat = '(^\d+\-\d+\-\d+)'
    extracted = stats.columns.str.extract(pat, expand=False)
    grouped = stats.groupby(extracted, axis=1).sum()
    return grouped

def student_id(file, id):
    input_file = pd.read_csv(file)
    student_row = input_file.loc[input_file['student'].values == int(id)]
    merged_dates = merge_dates(student_row)
    merged_dates = merged_dates.sort_index(axis=1)
    merged_dates = merged_dates.cumsum(axis=1)
    merged_excercises = merge_excercises(student_row)
    process_stats(merged_excercises, merged_dates)

def student_average(file):
    input_file = pd.read_csv(file)
    average_row = input_file.mean().to_frame().T
    merged_dates = merge_dates(average_row)
    merged_dates = merged_dates.sort_index(axis=1)
    merged_dates = merged_dates.cumsum(axis=1)
    merged_excercises = merge_excercises(average_row)
    process_stats(merged_excercises, merged_dates)

def process_stats(merged_excercises, merged_dates):
    slope = float(calc_slope(merged_dates))
    mean = float(merged_excercises.mean(axis=1))
    median = float(merged_excercises.median(axis=1))
    total = float(merged_excercises.sum(axis=1))
    passed = int(merged_excercises.astype(bool).sum(axis=1))
    date_sixteen, date_twenty = calc_dates(slope)
    x ={"mean": mean,
        "median": median,
        "total": total,
        "passed": passed,
        "regression slope": slope,
        "date 16": str(date_sixteen),
        "date 20": str(date_twenty)
    }
    final = json.dumps(x, indent=4)
    print(final)

def main():
    file = sys.argv[1]
    version = sys.argv[2]

    if version == 'average':
        student_average(file)
    else:
        student_id(file, version)

if __name__ == '__main__':
    main()
