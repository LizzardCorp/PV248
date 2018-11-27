import numpy as np
import pandas as pd
from scipy import stats
import sys, csv, json


def process_stats(stats):
    final = {}
    for column in stats:
        if column == 'student':
            continue
        mean = stats[column].mean(axis=0)
        median = stats[column].median(axis=0)
        first, last = np.percentile(stats[column], [25,75])
        passed = (stats[column] != 0).sum(axis=0)
        x ={"mean": float(mean),
            "median": float(median),
            "first": float(first),
            "last": float(last),
            "passed": int(passed)
        }
        y = json.dumps(x)
        final[column] = x
    final = json.dumps(final, indent=4)
    print(final)


def merge_excercises(stats):
    pat = '(\d+$)'
    extracted = stats.columns.str.extract(pat, expand=False)
    grouped = stats.groupby(extracted, axis=1).sum()
    return grouped

def merge_dates(stats):
    pat = '(^\d+\-\d+\-\d+)'
    extracted = stats.columns.str.extract(pat, expand=False)
    grouped = stats.groupby(extracted, axis=1).sum()
    return grouped

def stat_excercises(file):
    input_file = pd.read_csv(file)
    merged = merge_excercises(input_file)
    process_stats(merged)

def stat_dates(file):
    input_file = pd.read_csv(file)
    merged = merge_dates(input_file)
    process_stats(merged)

def stat_deadlines(file):
    input_file = pd.read_csv(file)
    process_stats(input_file)

def main():
    file = sys.argv[1]
    version = sys.argv[2]

    if version == 'excercises':
        stat_excercises(file)
    elif version == 'dates':
        stat_dates(file)
    else:
        stat_deadlines(file)

if __name__ == '__main__':
    main()
