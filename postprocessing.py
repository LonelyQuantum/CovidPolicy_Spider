import pandas as pd
import json
import dateparser

json_path = 'results/json/'
csv_path = 'results/csv/'

def load_json(path):
    with open(path) as file:
        return json.load(file)

def result_format(city):
    res_json = load_json(json_path + city + '.json')
    cols = res_json[0].keys()
    res_csv = pd.DataFrame(columns=cols)
    for item in res_json:
        item['date'] = dateparser.parse(item['date'].strip('(),.\n\ '))
        res_csv = res_csv.append(item, ignore_index=True)
    res_csv['date'] = pd.to_datetime(res_csv['date'])
    res_csv = res_csv.sort_values(by='date')
    res_csv.to_csv(csv_path + city + '.csv',encoding='utf_8_sig')