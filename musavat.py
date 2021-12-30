import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from multiprocessing import Pool
import random
from fuzzywuzzy import fuzz


# options

url_list_output = []

output_data = []
options = webdriver.FirefoxOptions()

# user-agent
options.set_preference("general.useragent.override",
                       "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

# disable webdriver mode
options.set_preference("dom.webdriver.enabled", True)


# headless mode
options.headless = True



def func_chunks_generators(seq, size):
    return (seq[i::size] for i in range(size))



# data_master_scan = []
def get_data(url_list):
    try:
        driver = webdriver.Firefox(
            executable_path=fr"{os.getcwd()}/geckodriver",
            options=options
        )

        # "C:\\users\\selenium_python\\chromedriver\\chromedriver.exe"
        # r"C:\users\selenium_python\chromedriver\chromedriver.exe"
        for url, caunt, data_master_scan in url_list:
            driver.get(url=url)
            time.sleep(2)
            src = driver.page_source
            soup = BeautifulSoup(src, 'html.parser')
            titul = soup.find("title").text
            txt = soup.find(class_="news-content").text.replace('\n', ' ')
            print(txt)
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

            # moderator меняем на название сайта

            if exit_data.count(1) != 0:
                if os.listdir('files/Musavat.com') == []:
                    try:
                        with open(f'files/Musavat.com/text_{caunt}.txt', 'w', encoding='utf-8') as file:
                            file.write(f'{url}\n\n{titul}\n\n{txt}')
                        # caunt += 1
                    except Exception as a:
                        print(a)
                    output_data.append([exit_data, url])
                    # return [exit_data, url]
                    # url_list_output.append(url)

                # ----------------------------------------------не трогать-------------------------------------------------------------

                else:
                    try:
                        for dir_site in os.listdir('files'):
                            for dir_page in os.listdir(f'files/{dir_site}'):
                                with open(f'files/{dir_site}/{dir_page}', 'r',encoding="utf-8") as file:
                                    file.readline()
                                    file.readline()
                                    file.readline()
                                    if fuzz.ratio(txt, file.read()) >= 50:
                                        nsjrjrn=100/0

                        # ******************************************************************************************************************************************

                        # musavat меняем на название сайта

                        try:
                            with open(f'files/Musavat.com/text_{caunt}.txt', 'w', encoding='utf-8') as file:
                                file.write(f'{url}\n\n{titul}\n\n{txt}')
                                output_data.append([exit_data, url])
                                # return [exit_data, url]
                                # url_list_output.append(url)
                            # caunt += 1


                        except Exception as a:
                            print(a)
                    except:
                        print('статья уже есть')
                # ******************************************************************************************************************************************

                print(output_data)

        time.sleep(random.randrange(3, 10))


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()



def pars_one(data_master_scan_in, data_time=(time.time())):
    try:
        data_time2 = time.localtime(data_time + 24*60*60)
        data_time = time.localtime(data_time)
        print(data_time)
        print(data_time[0])
        print(data_time)
        url_list_out = []
        driver = webdriver.Firefox(
            executable_path=fr"{os.getcwd()}/geckodriver",
            options=options
        )

        # "C:\\users\\selenium_python\\chromedriver\\chromedriver.exe"
        # r"C:\users\selenium_python\chromedriver\chromedriver.exe"

        driver.get(url='https://musavat.com/archive')
        time.sleep(4)
        caunt_l = 0
        for i in range(1, 1000):
            url = f'https://musavat.com/search?text=&type=news&date_begin={data_time[2]}.{data_time[1]}.{data_time[0]}&date_end={data_time2[2]}.{data_time2[1]}.{data_time2[0]}&id_news_category=&id_author=&page={i}'
            driver.get(url=url)
            time.sleep(4)
            src = driver.page_source
            # print(data_master_scan_in)
            try:
                soup = BeautifulSoup(src, 'html.parser')

                if int(soup.find(class_='pagination').find_all('li')[-2].text) == i:

                    return url_list_out



                for data in soup.find_all(class_='form-group col-sm-3 col-md-3'):
                    if data.find('a') != None:
                        ur = 'https://musavat.com' + data.find('a').get('href')
                        print(ur)
                        url_list_out.append([ur, caunt_l, data_master_scan_in])
                        caunt_l += 1

                print(url_list_out)


            except:
                print('NO')


        return url_list_out

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def parsing(data_master_scan_in, data_time=(time.time()), process_count = 1):

    url_list_output = []

    with open(f'files/Musavat.com/123.txt', 'w', encoding='utf-8') as file:
        file.write('')


    # exit()

    # process_count = int(input("Enter the number of processes: "))
    #process_count = 6


    urls_list = list(func_chunks_generators(pars_one(data_master_scan_in, data_time), process_count))
    print(urls_list)
    p = Pool(processes=process_count)
    p.map(get_data, urls_list)



    out_data_list = []

    for file_l in os.listdir('files/Musavat.com'):
        print(file_l)

        if file_l != '123.txt':
            with open(f'files/Musavat.com/{file_l}', 'r', encoding='utf-8') as file:
                url = file.readline()
                file.readline()

                txt = file.read()
            # print(url, txt)

            text_list = txt.lower().split(' ')
            # print(text_list)
            # caunt_local = 0
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

            out_data_list.append([exit_data,url])

    return [],out_data_list



if __name__ == "__main__":
    ojr = [['əlaqəsini', 'həyata'], ['edən'], ['k']]
    print(parsing(data_master_scan_in = ojr, data_time=int(time.time() - 20*24*60*60), process_count = 10))