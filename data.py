from asyncore import write
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
from os import listdir

print('Generating concat file [concat_data.csv]')
data = pd.read_excel('data.xlsx', sheet_name = None)
xls = pd.ExcelFile('data.xlsx')
for sheetName in xls.sheet_names:
    vars()["data_" + sheetName] = data.get(sheetName)
df = pd.DataFrame()
for sheetName in xls.sheet_names:
    df = pd.concat([df, vars()["data_"+ sheetName]], ignore_index=True)  
  
data_path = './data'
files = listdir(data_path)
print(files)
for f in files:
    df = pd.concat([df, pd.read_csv(data_path + '/' + f)], ignore_index=True) 

df.to_csv('concat_data.csv', index = False)
print(df.shape)

index_row = ['YT URL', 'Artist', 'Song', 'Publish', 'Week']
num_week = df.shape[0] // 100
with open('concat_data.csv', newline='', encoding = 'utf8') as csvfile_r:
    Songs = set()
    dict_rows = csv.DictReader(csvfile_r)
    dict_rows_copy = dict_rows
    for id,row in enumerate(dict_rows):
        if id > 0:
            Songs.add((str(row['Track Name']), str(row['Artist Names']), str(row['YouTube URL'])))
    print('Total number of songs: {}'.format(len(Songs)))
    for i in range(num_week):
        index_row.append(str(i + 1))
    print('Total number of weeks: ', len(index_row)-5)  

WriteContent = []
WriteContent_0_100_0 = []
PublishDateNotFound = ['Track, Artist, URL\n--------------------------\n']

print('Analyzing data ...')
for song_id, song_info in enumerate(Songs):
    song, auth, url = (song_info[0], song_info[1], song_info[2])
    
    # get HTML of the webpage
    r = requests.get(url + "/index.html")  
    soup = BeautifulSoup(r.text,"html.parser")
    
    # get data in <div class='watch-main-col'> <meta>
    sel = soup.select("div.watch-main-col meta") 
    date = '*'
    for s in sel:
        if s['itemprop'] == 'datePublished':
            date = s['content']
    if date == '*':
        PublishDateNotFound.extend([song, ', ', auth, ', ', url, '\n'])
        print('Crawl[{:03d}]: {}({})'.format(song_id, date, song))
        continue
    else:
        print('Crawl[{:03d}]: {}'.format(song_id, date), end='')

        if (int(date[0])*1000 + int(date[1])*100 + int(date[2])*10 + int(date[3])) < 2016:
            print('(remove)')
            continue
        print('\n', end='')

    with open('concat_data.csv', newline='', encoding = 'utf8') as csvfile_r:
        dict_rows = csv.DictReader(csvfile_r)
        start_0, middle_0, end_0 = (False, True, False)
        write_row = [url, auth, song, date, '']
        intop100 = False
        cnt = -1
        for id,row in enumerate(dict_rows):
            if id >= 0:
                if song == str(row['Track Name']) and auth == str(row['Artist Names']) and url == str(row['YouTube URL']):
                    intop100 = True
                    if start_0 == True:
                        middle_0 = False
                        cnt = 0
                    write_row.append(row['Views'])
                if id % 100 == 99:
                    if intop100 == True:
                        intop100 = False
                    else: 
                        if id//100 == 0:
                            start_0 = True
                        if middle_0 == False:
                            cnt += 1
                            if cnt >= 4:
                                end_0 = True
                        write_row.append(0)
        if len(write_row) == (num_week + 5): # 某一周1-100名 有重複的歌曲
            WriteContent.append(write_row)
            if start_0 and end_0 and (not middle_0):
                WriteContent_0_100_0.append(write_row)

print('Writing songs without published date into [song.txt]')
with open('song.txt', 'w', newline='', encoding='utf8') as txtfile:
    txtfile.writelines(PublishDateNotFound)

print('Writing result into [result_data.csv]')
with open('result_data.csv', 'w', newline = '', encoding = 'utf8') as csvfile_w:
    writer = csv.writer(csvfile_w)
    writer.writerow(index_row)
    for content in WriteContent: # list ['data', 'data2',...]
        writer.writerow(content)

print('Writing result into [result_data_100.csv]')
with open('result_data_100.csv', 'w', newline = '', encoding = 'utf8') as csvfile_w:
    writer = csv.writer(csvfile_w)
    writer.writerow(index_row)
    for content in WriteContent_0_100_0:
        writer.writerow(content)

print("Done! ~^^")