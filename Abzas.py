import asyncio
import os
import random
from fuzzywuzzy import fuzz
import time
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs
import requests
from fake_useragent import UserAgent

urls_list = []

us = UserAgent()
print(us.random)
def parsing(data_master_scan_in, data_time=(time.time())):
    headers = {'Accept': '*/*', 
                'Connection': 'keep-alive',
                'User-Agent': us.random,
                'Cache-Control': 'max-age=0', 'DNT': '1', 
                'Upgrade-Insecure-Requests': '1',
    }

    data_time = time.localtime(data_time)
    print(data_time)
    print(data_time[0])
    print(data_time)
    day = str(data_time[2])
    month = str(data_time[1])
    year = str(data_time[0])

    if(int(day)//10==0):day="0"+day
    if(int(month)//10==0):month="0"+month

    mo = 1
    m = "13"
    y = "3000"
    mi = 3000
    while int(month) <= int(m) and int(year) <= int(y):
        r = requests.get("https://www.abzas.net/page/" +str(mo)+ "/?s",headers=headers)
        y , m = bs(str(bs(r.text,"html.parser").findAll(class_="td_module_16 td_module_wrap td-animation-stack td-meta-info-hide")[-1]),"html.parser").find("a")["href"].split("/")[3:5]
        mo+=100
    print("[CHANGED]",mo)
    while int(month) > int(m) or int(year) > int(y):
        r = requests.get("https://www.abzas.net/page/" +str(mo)+ "/?s",headers=headers)
        y , m = bs(str(bs(r.text,"html.parser").findAll(class_="td_module_16 td_module_wrap td-animation-stack td-meta-info-hide")[-1]),"html.parser").find("a")["href"].split("/")[3:5]
        mo-=10
    print("[CHANGED]",mo)
    while int(month) <= int(m) and int(year) <= int(y):
        r = requests.get("https://www.abzas.net/page/" +str(mo)+ "/?s",headers=headers)
        y , m = bs(str(bs(r.text,"html.parser").findAll(class_="td_module_16 td_module_wrap td-animation-stack td-meta-info-hide")[-1]),"html.parser").find("a")["href"].split("/")[3:5]
        mo+=1
    mo-=1
    print("[CHANGED]",mo)
    mi = mo
    while int(month) >= int(m):
        r = requests.get("https://www.abzas.net/page/" +str(mi)+ "/?s",headers=headers)
        try:
            y , m = bs(str(bs(r.text,"html.parser").findAll(class_="td_module_16 td_module_wrap td-animation-stack td-meta-info-hide")[-1]),"html.parser").find("a")["href"].split("/")[3:5]
        except:
            break
        mi-=10
        print("[MI]",mi)
    print("[CHANGED]",mi)
    while int(month) < int(m):
        r = requests.get("https://www.abzas.net/page/" +str(mi)+ "/?s",headers=headers)
        y , m = bs(str(bs(r.text,"html.parser").findAll(class_="td_module_16 td_module_wrap td-animation-stack td-meta-info-hide")[-1]),"html.parser").find("a")["href"].split("/")[3:5]
        mi+=1
        print("[MI]",mi)
    mi-=1
    if(mi < 0 ): mi = 1
    print(mi,mo)
    caunt = 0
    for page in range(mi,mo+1):
        r = requests.get("https://www.abzas.net/page/" +str(page)+ "/?s",headers=headers)
        for stat in bs(r.text,"html.parser").findAll(class_="td_module_16 td_module_wrap td-animation-stack td-meta-info-hide"):
            m = bs(str(stat),"html.parser").find("a")["href"].split("/")[4]
            if(m == month):
                urls_list.append(bs(str(stat),"html.parser").find("a")["href"])
                caunt+=1
    time.sleep(5)
    caunt = 0
    for link in urls_list:
        caunt+=1
        headers = {'Accept': '*/*', 
                'Connection': 'keep-alive',
                'User-Agent': us.random,
                'Cache-Control': 'max-age=0', 'DNT': '1', 
                'Upgrade-Insecure-Requests': '1',
        }
        p = requests.get(link,headers=headers)
        soup = bs(p.text,"html.parser")
        d = soup.find(class_="td-post-date").text.split()[0]
        print(d)
        if(int(d) < int(day)):
            break
        if(int(d) == int(day)):
            titul = soup.find("title").text

            # -----------------------------------------------------------------------------------
            # Достать статью в переменную txt


            tttt = ""
            tttt = soup.find(class_='td-post-content tagdiv-type')
            txxt = ""
            txxt = bs(str(tttt),"html.parser").findAll("p")
            txt = ""
            for i in txxt:
                txt+=i.text+"\n"
            print(txt)
            text_list = txt.lower().split(' ')
            exit_data = []
            for one_line in data_master_scan_in:
                caunt_local = 0
                for twe in one_line:
                    for master_text in text_list:
                        if fuzz.ratio(master_text, twe) >= 80:
                            caunt_local += 1
                            break

                if caunt_local == len(one_line):
                    exit_data.append(1)
                else:
                    exit_data.append(0)

            print(exit_data, link)

            # ******************************************************************************************************************************************
            output_data = []
            url_list_output = []
            if exit_data.count(1) != 0:
                if os.listdir('files/'+"Abzas.net") == []:
                    try:
                        with open(f'files/'+ "Abzas.net" +'/text_'+ str(caunt) +'.txt', 'w', encoding='utf-8') as file:
                            file.write(f'{titul}\n\n{link}\n\n{txt}')

                    except Exception as a:
                        print(a)
                    output_data.append(exit_data)
                    url_list_output.append(link)

                # ----------------------------------------------не трогать-------------------------------------------------------------


                else:
                    for dir_site in os.listdir('files'):
                        for dir_page in os.listdir(f'files/{dir_site}'):
                            with open(f'files/{dir_site}/{dir_page}', 'r',encoding="utf-8") as file:
                                file.readline()
                                file.readline()
                                file.readline()
                                if fuzz.ratio(txt, file.read()) >= 50:
                                    break

                    # ******************************************************************************************************************************************

                    try:
                        with open(f'files/'+ "Abzas.net" +'/text_'+ str(caunt) +'.txt', 'w', encoding='utf-8') as file:
                            file.write(f'{titul}\n\n{link}\n\n{txt}')
                            output_data.append(exit_data)
                            url_list_output.append(link)


                    except Exception as a:
                        print(a)

                # ******************************************************************************************************************************************