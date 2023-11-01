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
import mysql.connector

from bs4 import BeautifulSoup
from collections import Counter, defaultdict
from fake_headers import Headers
from urllib3.exceptions import MaxRetryError
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm, trange
from pprint import pprint

TABLEINFO = ['YP_all_overview', 'YP_summary']

parser = argparse.ArgumentParser()

def get_id(conn):

    #ids will count all data in web.
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

            #get r_number by changing url
            for page_idx in range(2,2+pages):
                headers = Headers(headers=True).generate()
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                for index, contents in enumerate(soup.find_all(class_='tit-wrap')):
                    try:
                        #'title','r_number'
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

    #fetch data from database
    cursor = conn.cursor()
    sql = "SELECT title, r_number FROM yp_all_overview"
    cursor.execute(sql)
    data_in_db = set(cursor.fetchall())

    #new policies
    data_to_be_added = ids - data_in_db
    
    print(f"There are new {len(data_to_be_added)} policies.")

    #final dataset, origin dataset(could be updated) + new dataset(should be added)
    data_final = sorted(list(data_in_db)) + sorted(list(data_to_be_added))
    
    ret_list=[]
    for index, contents in enumerate(data_final):
        contents=list(contents)
        url = "https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do?pageIndex=1&bizId="
        #add R-number
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

    replace " to ' handle sql insertion error
    '''

    #main title
    main_title = Tag_list.find("h2").text
    main_title = main_title.replace("\"","'")

    #short description
    short_description = Tag_list.find(class_="doc_desc").text
    short_description = short_description.replace("\"","'")

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
        value = value.replace("\"","'")
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
        value = value.replace("\"","'")
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
        value = value.replace("\"","'")
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
        value = value.replace("\"","'")
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

def insert_yp_all_overview(conn, result_list):
    cursor = conn.cursor()
    scheme_format = ['yp', 'title', 'r_number', 'url', 'main_title', 'short_description']
    for index, contents in enumerate(tqdm(result_list)):
        yp = str(contents['yp'])
        title = contents['title']
        r_number = contents['r_number']
        url = contents['contents']['url']
        main_title = contents['contents']['main_title']
        short_description = contents['contents']['short_description']
        values_format = tuple([yp, title, r_number, url, main_title, short_description])

        sql = "INSERT INTO " + "yp_all_overview " + "VALUES " + \
        "(\"{}\")".format("\", \"".join(values_format)) + \
        " ON DUPLICATE KEY UPDATE " + \
        ", ".join([f'{scheme} = "{value}"' for scheme, value in zip(scheme_format, values_format) if scheme != 'YP'])
        
        cursor.execute(sql)
        
    conn.commit()
    return

def insert_yp_summary(conn, result_list):
    cursor = conn.cursor()
    scheme_format = ['yp', 'policy_area', 'support_content', 'operation_period', 'application_period', 'supprot_scale', 'remarks']
    for index, contents in enumerate(tqdm(result_list)):
        yp = str(contents['yp'])
        policy_area = contents['contents']['summary']['정책 분야']
        support_content = contents['contents']['summary']['지원 내용']
        operation_period = contents['contents']['summary']['사업 운영 기간']
        application_period = contents['contents']['summary']['사업 신청 기간']
        supprot_scale = contents['contents']['summary']['지원 규모(명)']
        remarks = contents['contents']['summary']['비고']
        values_format = tuple([yp, policy_area, support_content, operation_period, application_period, supprot_scale, remarks])

        sql = "INSERT INTO " + "yp_summary " + "VALUES " + \
        "(\"{}\")".format("\", \"".join(values_format)) + \
        " ON DUPLICATE KEY UPDATE " + \
        ", ".join([f'{scheme} = "{value}"' for scheme, value in zip(scheme_format, values_format) if scheme != 'YP'])
        
        cursor.execute(sql)
        
    conn.commit()
    return

def insert_yp_qualification(conn, result_list):
    cursor = conn.cursor()
    scheme_format = ['yp', 'age', 'residence_income', 'education', 'major', 'employment_status', 'specialization', 'additional_info', 'eligibility']
    for index, contents in enumerate(tqdm(result_list)):
        yp = str(contents['yp'])
        age = contents['contents']['qualification']['연령']
        residence_income = contents['contents']['qualification']['거주지 및 소득']
        education = contents['contents']['qualification']['학력']
        major = contents['contents']['qualification']['전공']
        employment_status = contents['contents']['qualification']['취업 상태']
        specialization = contents['contents']['qualification']['특화 분야']
        additional_info = contents['contents']['qualification']['추가 단서 사항']
        eligibility = contents['contents']['qualification']['참여 제한 대상']
        values_format = tuple([yp, age, residence_income, education, major, employment_status, specialization, additional_info, eligibility])

        sql = "INSERT INTO " + "yp_qualification " + "VALUES " + \
        "(\"{}\")".format("\", \"".join(values_format)) + \
        " ON DUPLICATE KEY UPDATE " + \
        ", ".join([f'{scheme} = "{value}"' for scheme, value in zip(scheme_format, values_format) if scheme != 'YP'])
        
        cursor.execute(sql)
        
    conn.commit()
    return

def insert_yp_methods(conn, result_list):
    cursor = conn.cursor()
    scheme_format = ['yp', 'application_procedure', 'evaluation_announcement', 'application_website', 'required_documents']
    for index, contents in enumerate(tqdm(result_list)):
        yp = str(contents['yp'])
        application_procedure = contents['contents']['methods']['신청 절차']
        evaluation_announcement = contents['contents']['methods']['심사 및 발표']
        application_website = contents['contents']['methods']['신청 사이트']
        required_documents = contents['contents']['methods']['제출 서류']
        values_format = tuple([yp, application_procedure, evaluation_announcement, application_website, required_documents])

        sql = "INSERT INTO " + "yp_methods " + "VALUES " + \
        "(\"{}\")".format("\", \"".join(values_format)) + \
        " ON DUPLICATE KEY UPDATE " + \
        ", ".join([f'{scheme} = "{value}"' for scheme, value in zip(scheme_format, values_format) if scheme != 'YP'])
        
        cursor.execute(sql)
        
    conn.commit()
    return

def insert_yp_etc(conn, result_list):
    cursor = conn.cursor()
    scheme_format = ['yp', 'other_info', 'host_organization', 'operating_organization', 'reference_1', 'reference_2', 'attachments']
    for index, contents in enumerate(tqdm(result_list)):
        yp = str(contents['yp'])
        other_info = contents['contents']['etc']['기타 유익 정보']
        host_organization = contents['contents']['etc']['주관 기관']
        operating_organization = contents['contents']['etc']['운영 기관']
        reference_1 = contents['contents']['etc']['사업관련 참고 사이트 1']
        reference_2 = contents['contents']['etc']['사업관련 참고 사이트 2']
        attachments = contents['contents']['etc']['첨부파일']
        values_format = tuple([yp, other_info, host_organization, operating_organization, reference_1, reference_2, attachments])

        sql = "INSERT INTO " + "yp_etc " + "VALUES " + \
        "(\"{}\")".format("\", \"".join(values_format)) + \
        " ON DUPLICATE KEY UPDATE " + \
        ", ".join([f'{scheme} = "{value}"' for scheme, value in zip(scheme_format, values_format) if scheme != 'YP'])
        
        cursor.execute(sql)
        
    conn.commit()
    return

def insert_table(conn, result_list):
    insert_yp_all_overview(conn, result_list)
    insert_yp_summary(conn, result_list)
    insert_yp_qualification(conn, result_list)
    insert_yp_methods(conn, result_list)
    insert_yp_etc(conn, result_list)


if __name__ == '__main__':
    start_time = time.time()
    print("This code is web crawler of ChatPub Service. Final updated date is 20231101.\n")
    print("Start crawling...")

    #connect with database
    try:
        conn = mysql.connector.connect(
            user='root',
            password='1234',
            host='localhost',
            port=3306,
            database='ChatPub',
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        exit(0)
    
    #title, r_number, yp, url
    YPlist = get_id(conn)

    print(f"The number of total data : {len(YPlist)}")

    result_list = list()

    for index, contents in enumerate(tqdm(YPlist)):
        parsed_data = doc_parser(contents)
        result_list.append({
            'yp': index,
            'title': contents[0],
            'r_number': contents[1],
            'contents': parsed_data,
        })

    print("\nStart insertion...")
    insert_table(conn, result_list)

    conn.close()
    print(f"Process was finished. It takes {time.time()-start_time} sec.")