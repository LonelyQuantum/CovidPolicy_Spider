# -*- coding: utf-8 -*-
'''
Usage: from postprocess import *
'''
import pandas as pd
import json
import dateparser
import re
import os

json_path = 'results/json/'
csv_path = 'results/csv/'

date_pattern = '([0-9]+[-年月日/0-9\.]*[0-9]+[日]?)'

def load_json(path):
    with open(path) as file:
        return json.load(file)

def result_format(city):
    # result_format(city) and it will change the format from .json to .csv
    res_json = load_json(json_path + city + '.json')
    cols = res_json[0].keys()
    res_csv = pd.DataFrame(columns=cols)
    for item in res_json:
        if type(item['date']) is str:
            date_cur = re.findall(date_pattern,item['date'])
            if len(date_cur) > 0:
                item['date'] = dateparser.parse(date_cur[0])
        res_csv = res_csv.append(item, ignore_index=True)
    res_csv['date'] = pd.to_datetime(res_csv['date'])
    res_csv = res_csv.sort_values(by='date')
    res_csv.to_csv(csv_path + city + '.csv',encoding='utf_8_sig',index=False)

def encodeCSV():
    csvWithIndex = ['settings/selector_settings.csv','settings/city_govs.csv']
    for csvFile in csvWithIndex:
        df = pd.read_csv(csvFile,index_col='city')
        df.to_csv(csvFile,encoding='utf_8_sig')
    csvWithoutIndex = os.listdir(csv_path)
    for csvFile in csvWithoutIndex:
        if csvFile.endswith('.csv'):
            df = pd.read_csv(csv_path + csvFile)
            df.to_csv(csv_path + csvFile,index=False,encoding='utf_8_sig')

    
def change_selector(city,columns,values):
    selector_settings = pd.read_csv('settings/selector_settings.csv',index_col='city')
    selector_settings.loc[city][columns] = values
    selector_settings.to_csv('settings/selector_settings.csv',encoding='utf_8_sig')