import asyncio
import os
import random
from fuzzywuzzy import fuzz
import time
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

us = UserAgent()
print(us.random)

def parsing(data_master_scan_in, data_time=(time.time())):

    url_list_output = []

    output_data = []

    async def fetch_url_data(session, url, caunt, data_master_scan):
        print(url, caunt)
        headers = {'Accept': '*/*', 'Connection': 'keep-alive',
                   'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
                   'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1'}
        try:


            async with session.get(url, headers=headers) as response:
                resp = await response.text()
                # print(resp)
                soup = BeautifulSoup(resp, 'html.parser')

                titul = soup.find("title").text

                # -----------------------------------------------------------------------------------
                # Достать статью в переменную txt



                tttt = ""
                tttt = soup.find(class_='nw_imtxt clearfix')
                txxt = ""
                txxt = BeautifulSoup(str(tttt),"html.parser").findAll("p")
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
                            if fuzz.ratio(master_text, twe) >= 85:
                                caunt_local += 1
                                break

                    if caunt_local == len(one_line):
                        exit_data.append(1)
                    else:
                        exit_data.append(0)

                print(exit_data, url)

                # ******************************************************************************************************************************************

                # moderator меняем на название сайта

                if exit_data.count(1) != 0:
                    if os.listdir('files/Modern.az') == []:
                        try:
                            with open(f'files/Modern.az/text_{caunt}.txt', 'w', encoding='utf-8') as file:
                                file.write(f'{url}\n\n{titul}\n\n{txt}')

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

                        # moderator меняем на название сайта

                        try:
                            with open(f'files/Modern.az/text_{caunt}.txt', 'w', encoding='utf-8') as file:
                                file.write(f'{url}\n\n{titul}\n\n{txt}')
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
        # moderator меняем на название сайта

        url_list_output = []
        output_data = []

        data_time = time.localtime(data_time)
        print(data_time)
        print(data_time[0])
        print(data_time)

        timer = time.time()
        urls_list = []
        caunt = 0


        # ******************************************************************************************************************************************
        # Тут нормальный парсинг, нужно достать ссылки на новости

        # УСЛОВНО РАЗВЕКАТЬСЯ МОЖНО ВОТ ТУТ ↓
        headers = {'Accept': '*/*', 'Connection': 'keep-alive',
                   'User-Agent': f'{us.random}',
                   'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1'}
        # url = f'https://moderator.az/all/?date={data_time[0]}-{data_time[1]}-{data_time[2]}&page={i}'
        url = f'https://modern.az/az/news/date/{data_time[0]}-{data_time[1]}-{data_time[2]}/page/1'
        print(url)

        req = requests.get(url, headers=headers)

        src = req.text
        # print(src)
        soup = BeautifulSoup(src, 'html.parser')

        page = soup.find(class_='news_divs clearfix')
        if page.find('a') != None:
            urls_list_local = []
            for url_n in page.find_all('a'):
                if urls_list.count(url_n.get('href')) == 0:
                    urls_list.append([url_n.get('href'), caunt, data_master_scan_in])
                    urls_list_local.append([url_n.get('href'), caunt, data_master_scan_in])
                    caunt += 1  # Это нужно оставить, так как по нему создаются файлы txt
                # break
            time.sleep(1)
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(fetch_async(urls_list_local))
            loop.run_until_complete(future)
            time.sleep(1)

        for i in range(2, int(str(soup.find(class_='pagination').find_all('li')[-1].find('a').get('href')).split('/')[-2]) + 1):
            headers = {'Accept': '*/*', 'Connection': 'keep-alive',
                       'User-Agent': f'{us.random}',
                       'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1'}
            # url = f'https://moderator.az/all/?date={data_time[0]}-{data_time[1]}-{data_time[2]}&page={i}'
            url = f'https://modern.az/az/news/date/{data_time[0]}-{data_time[1]}-{data_time[2]}/page/{i}/'
            print(url)

            req = requests.get(url, headers=headers)

            src = req.text
            # print(src)
            soup = BeautifulSoup(src, 'html.parser')

            page = soup.find(class_='news_divs clearfix')
            if page.find('a') != None:
                urls_list_local = []
                for url_n in page.find_all('a'):
                    if urls_list.count(url_n.get('href')) == 0:
                        urls_list.append([url_n.get('href'), caunt, data_master_scan_in])
                        urls_list_local.append([url_n.get('href'), caunt, data_master_scan_in])
                        caunt += 1  # Это нужно оставить, так как по нему создаются файлы txt
                    # break
                time.sleep(2)
                loop = asyncio.get_event_loop()
                future = asyncio.ensure_future(fetch_async(urls_list_local))
                loop.run_until_complete(future)
                time.sleep(0.5)
            else:
                break


            # print(urls_list)

        print(urls_list)

        # УСЛОВНО РАЗВЕКАТЬСЯ МОЖНО ВОТ ТУТ ↑

        # time.sleep(2)
        # loop = asyncio.get_event_loop()
        # future = asyncio.ensure_future(fetch_async(urls_list))
        # loop.run_until_complete(future)

        print(time.time() - timer)





    pars(data_master_scan_in, data_time)

    return url_list_output, output_data

if __name__ == "__main__":
    ojr = [['milyon', 'min'], ['ərazisində'], ['məlumatda']]
    parsing(data_master_scan_in = ojr, data_time=int(time.time() - 24*60*60*50))


# Ну потом можно принты почистить, просто не очень прикольно смотреть на пустую консоль

