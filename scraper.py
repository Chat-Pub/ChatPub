"""
The integrated process to crawl the entire data from 
https://www.youthcenter.go.kr/main.do
https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do
https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do

The specific process will be determined later.

Process & Description : 
1. Get whole data of young_policies by options. options will be determined by user. 
(e.g. Region, Category, Core keywords)

2. Data structure of crawled data will be defaultdict.

3. We will give YP number to each data.
main data structure will be [YP, title, R-number, contents]

"""


import argparse
import datetime
import logging.handlers
import sys
import numpy as np
import os
import pandas as pd
import pickle
import requests
import ssl
import ipdb
import time
import warnings
import math
import re
import json

from bs4 import BeautifulSoup
from collections import Counter, defaultdict
from fake_headers import Headers
from urllib3.exceptions import MaxRetryError
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm, trange
from pprint import pprint

parser = argparse.ArgumentParser()

def get_id():
    ids = set()
    err_count=0
    url = 'https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?'
    url += 'pageIndex=1'
    url += '&srchRegion=003001&srchRegion=003002001&srchRegion=003002008&srchSortOrder=1&pageUnit=12'
    while True:
        try:
            headers = Headers(headers=True).generate()
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            try:
                total_num=int(float(soup.find(class_='result-num').find('span').text))
            except:
                print("result-num error : cannot find result-num")
                break
            pages = math.ceil(total_num/12)
            for page_idx in range(2,2+pages):
                headers = Headers(headers=True).generate()
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                for index, contents in enumerate(soup.find_all(class_='tit-wrap')):
                    try:
                        ids.add((contents.text.replace('\n','').strip(),contents.a.get('id')[8:]))
                    except:
                        continue
                url = 'https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?'
                url += 'pageIndex='
                url += f'{page_idx}'
                url += '&srchRegion=003001&srchRegion=003002001&srchRegion=003002008&srchSortOrder=1&pageUnit=12'
            break
        except:
            err_count += 1
            if err_count > 10:  
                print("error")
                break
            time.sleep(1)
            continue

    ret_list=[]
    ids=list(ids)
    for index, contents in enumerate(ids):
        contents=list(contents)
        url = "https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do?pageIndex=1&bizId="
        url += contents[1]
        contents.append(index)
        contents.append(url)
        ret_list.append(contents)
    return ret_list

def doc_parser(contents):
    headers = Headers(headers=True).generate()
    url = contents[3]
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    main_div = soup.find('div', id='wrap')
    
    if main_div is None:
        return None
    
    Tag_list = main_div.find("div", class_='policy-detail')
    return_dict = defaultdict()

    '''
    The codes below are process of extracting data field
    data will be stored in return_dict
    '''

    #main title
    main_title = Tag_list.find("h2").text
    
    #short description
    short_description = Tag_list.find(class_="doc_desc").text

    #SUMMARY dictionary
    summary_dict = defaultdict()
    
    summary_contents = Tag_list.find_all(class_="table_wrap")[0].find("ul")
    for index, contents in enumerate(summary_contents.find_all("li")):
        key = re.sub(r'[\r\n\t]', '',contents.find(class_="list_tit").text).strip()
        value = contents.find(class_="list_cont").find_all(string=True)
        if len(value)==0:
            value = None
        elif len(value)==1:
            value = re.sub(r'[\r\n\t]', '',value[0].text).strip()
        else:
            newvalue=""
            for v in value:
                v = re.sub(r'[\r\n\t]', '',v.text).strip()
                newvalue += v
                if v != '':
                    newvalue += '\n'
            value = newvalue.strip('\n')
        summary_dict[key] = value
    
    #QUALIFICATION dictionary
    qualification_dict = defaultdict()
    
    qualification_contents = Tag_list.find_all(class_="table_wrap")[1].find("ul")
    for index, contents in enumerate(qualification_contents.find_all("li")):
        key = re.sub(r'[\r\n\t]', '',contents.find(class_="list_tit").text).strip()
        value = contents.find(class_="list_cont").find_all(string=True)
        if len(value)==0:
            value = None
        elif len(value)==1:
            value = re.sub(r'[\r\n\t]', '',value[0].text).strip()
        else:
            newvalue=""
            for v in value:
                v = re.sub(r'[\r\n\t]', '',v.text).strip()
                newvalue += v
                if v != '':
                    newvalue += '\n'
            value = newvalue.strip('\n')
        qualification_dict[key] = value

    #METHODS dictionary
    methods_dict = defaultdict()
    
    methods_contents = Tag_list.find_all(class_="table_wrap")[2].find("ul")
    for index, contents in enumerate(methods_contents.find_all("li")):
        key = re.sub(r'[\r\n\t]', '',contents.find(class_="list_tit").text).strip()
        value = contents.find(class_="list_cont").find_all(string=True)
        if len(value)==0:
            value = None
        elif len(value)==1:
            value = re.sub(r'[\r\n\t]', '',value[0].text).strip()
        else:
            newvalue=""
            for v in value:
                v = re.sub(r'[\r\n\t]', '',v.text).strip()
                newvalue += v
                if v != '':
                    newvalue += '\n'
            value = newvalue.strip('\n')
        methods_dict[key] = value

    #ETC dictionary
    etc_dict = defaultdict()
    
    etc_contents = Tag_list.find_all(class_="table_wrap")[3].find("ul")
    for index, contents in enumerate(etc_contents.find_all("li")):
        key = re.sub(r'[\r\n\t]', '',contents.find(class_="list_tit").text).strip()
        value = contents.find(class_="list_cont").find_all(string=True)
        if len(value)==0:
            value = None
        elif len(value)==1:
            value = re.sub(r'[\r\n\t]', '',value[0].text).strip()
        else:
            newvalue=""
            for v in value:
                v = re.sub(r'[\r\n\t]', '',v.text).strip()
                newvalue += v
                if v != '':
                    newvalue += '\n'
            value = newvalue.strip('\n')
        etc_dict[key] = value

    #store into return_dictionary
    return_dict['url'] = url
    return_dict['main_title'] = main_title
    return_dict['short_description'] = short_description
    return_dict['summary'] = summary_dict
    return_dict['qualification'] = qualification_dict
    return_dict['methods'] = methods_dict
    return_dict['etc'] = etc_dict

    return return_dict

if __name__ == '__main__':
    print("Start crawling...")
    YPlist = get_id()

    print(f"The number of data : {len(YPlist)}")

    result_list = list()

    for index, contents in enumerate(tqdm(YPlist)):
        #print(index,contents)
        parsed_data = doc_parser(contents)
        result_list.append({
            'YP': index,
            'title': contents[0],
            'R-number': contents[1],
            'contents': parsed_data,
        })


