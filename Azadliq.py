import asyncio
import os
import random
from fuzzywuzzy import fuzz
import time
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs
import requests
from fake_useragent import UserAgent

monthes = [

    "0",
    "Yanvar",
    "Fevral",
    "Mart",
    "Aprel",
    "May",
    "İyun",
    "İyul",
    "Avqust",
    "Sentyabr",
    "Oktyabr",
    "Noyabr",
    "Dekabr"

]

us = UserAgent()
print(us.random)

def parsing(data_master_scan_in, data_time=(time.time())):

    url_list_output = []

    output_data = []

    async def fetch_url_data(session, url, caunt, data_master_scan):
        print(url, caunt)
        headers = {'Accept': '*/*', 'Connection': 'keep-alive',
                   'User-Agent': f'{us.random}',
                   'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1'}
        try:


            async with session.get(url, headers=headers) as response:
                resp = await response.text()
                # print(resp)
                soup = bs(resp, 'html.parser')

                titul = soup.find("title").text
                print(titul)

                # -----------------------------------------------------------------------------------
                # Достать статью в переменную txt

                tttt = ""
                tttt = soup.find(class_='wsw')
                txxt = ""
                txxt = bs(str(tttt),"html.parser").findAll("p")
                txt = ""
                for i in txxt:
                    txt+=i.text+"\n"


                # ---------------------------------------Обработчик, можно не трогать----------------------------------------------

                text_list = txt.lower().split(' ')
                # print(text_list)
                # caunt_local = 0

                exit_data = []
                for one_line in data_master_scan:
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

                print(exit_data, url)

                # ******************************************************************************************************************************************

                if exit_data.count(1) != 0:
                    if os.listdir('files/'+"Azadliq.org") == []:
                        try:
                            with open(f'files/'+ "Azadliq.org" +'/text_'+ str(caunt) +'.txt', 'w', encoding='utf-8') as file:
                                file.write(f'{titul}\n\n{url}\n\n{txt}')

                        except Exception as a:
                            print(a)
                        output_data.append([exit_data, url])

                    # ----------------------------------------------не трогать-------------------------------------------------------------


                    else:
                        for dir_site in os.listdir('files'):
                            for dir_page in os.listdir(f'files/{dir_site}'):
                                with open(f'files/{dir_site}/{dir_page}', 'r',encoding="utf-8") as file:
                                    file.readline()
                                    file.readline()
                                    file.readline()
                                    if fuzz.ratio(txt, file.read()) >= 50:
                                        return 0

                        # ******************************************************************************************************************************************

                        try:
                            with open(f'files/'+ "Azadliq.org" +'/text_'+ str(caunt) +'.txt', 'w', encoding='utf-8') as file:
                                file.write(f'{url}\n\n{txt}')
                                output_data.append([exit_data, url])


                        except Exception as a:
                            print(a)

                    # ******************************************************************************************************************************************




                    print(output_data)


                    # типа проверка статьи






                # exit()





        except Exception as e:
            print(e, url, caunt)
        else:
            return resp
        return


    async def fetch_async(url_lists):
        tasks = []
        async with ClientSession() as session:
            for url, caint, data_master_scan_in in url_lists:
                # print(url)
                task = asyncio.ensure_future(fetch_url_data(session, url, caint, data_master_scan_in))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
        return responses






    def pars(data_master_scan_in, data_time=(time.time())):

        # ******************************************************************************************************************************************

        url_list_output = []
        output_data = []

        data_time = time.localtime(data_time)
        print(data_time)
        print(data_time[0])
        print(data_time)
        day = str(data_time[2])
        month = str(data_time[1])
        year = str(data_time[0])

        timer = time.time()
        urls_list = []
        caunt = 0


        # ******************************************************************************************************************************************
        # Тут нормальный парсинг, нужно достать ссылки на новости

        # УСЛОВНО РАЗВЕКАТЬСЯ МОЖНО ВОТ ТУТ ↓
        stop = 0
        page = 0
        while(not (stop)):
            headers = {'Accept': '*/*', 'Connection': 'keep-alive',
                    'User-Agent': f'{us.random}',
                    'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1'}
            url = 'https://www.azadliq.org/azadl%C4%B1q_radiosu_m%C9%99qal%C9%99l%C9%99r?p=' + str(page) + '&d=' + day + '&m=' + month + '&y='+ year

            print(url)

            req = requests.get(url, headers=headers)

            src = req.text
            # print(src)
            soup = bs(src, 'html.parser')
            if len(soup.findAll(class_="col-xs-12 col-sm-12 col-md-12 col-lg-12 fui-grid__inner")) > 0:
                for stat in soup.findAll(class_="col-xs-12 col-sm-12 col-md-12 col-lg-12 fui-grid__inner"):
                    soap = bs(str(stat), 'html.parser')
                    asd = soap.find(class_="date date--mb date--size-3")
                    m = monthes.index(asd.text.split()[0])
                    d = asd.text.split()[1].replace(",","")
                    y = asd.text.split()[2]
                    if(int(d) == int(day)):
                        print(str(stat).find('a'))
                        if str(stat).find('a') != None:
                            print("[DEBUG] find <a>")
                            for url_n in soap.findAll('a'):
                                if urls_list.count(url_n.get('href')) == 0:
                                    urls_list.append(["https://www.azadliq.org"+url_n.get('href'), caunt, data_master_scan_in])
                                    caunt += 1  # Это нужно оставить, так как по нему создаются файлы txt
                                # break
                        else:
                            stop = 1
                            break
                    elif (int(d) < int(day)):
                        stop = 1
                        print("[DEBUG] ", page)
                        break
            else:
                stop = 1
                print("[DEBUG] ", page)
                break

            page+=1
        
        print(urls_list)
        # УСЛОВНО РАЗВЕКАТЬСЯ МОЖНО ВОТ ТУТ ↑
    
        # time.sleep(2)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(fetch_async(urls_list))
        loop.run_until_complete(future)

        print(time.time() - timer)




    pars(data_master_scan_in, data_time)

    return url_list_output, output_data

if __name__ == "__main__":
    ojr = [['Kennedinin', 'əlaqədar'], ['Prezident'], ['k']]
    parsing(data_master_scan_in = ojr, data_time=int(time.time()))

# Ну потом можно принты почистить, просто не очень прикольно смотреть на пустую консоль