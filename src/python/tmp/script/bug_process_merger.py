import csv
import sys
import pandas as pd

"""
バグ情報とDIMAで取得したプロセスメトリクスをファイル名でマージするスクリプト
"""
args = sys.argv
bug_filename = args[1]
process_m_filename = args[2]
save_filename = args[3]

bug_list = []
with open(bug_filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        bug_list = row
print("bug count:  " + str(len(bug_list)))
df = pd.read_csv(process_m_filename,header=0)
df['fileName'] = df.apply(lambda x: x['fileName'].split("/")[9:], axis=1)
df['fileName'] = df.apply(lambda x: "/".join(x['fileName']), axis=1)
df['bug'] = df.apply(lambda x: 1 if(x['fileName'] in bug_list) else 0, axis=1)
found = df['bug'].sum()
print("found bug: " + str(found))
df.to_csv(save_filename)
