import csv
import matplotlib.pyplot as plt
import numpy as np

def BarChart_h(x, y, title, x_label, y_label):
    bar = plt.barh(x, y)
    plt.bar_label(bar, y)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.show()

print('================[RawData]================')

totalnum_weeks_in_top100, num_songs = 0, 0
num_weeks = []
max_weeks, max_0to100 = 0, 0

with open('result_data.csv', newline='', encoding = 'utf8') as csvfile_r:
    dict_rows = csv.DictReader(csvfile_r)
    for id, row in enumerate(dict_rows):   
        data = [v for v in dict(row).values()]
        weeks = [int(w) for w in data[5:]]
        num_songs += 1
        num_weeks_in_top100 = 0
        for w in weeks:
            if w != 0:
                totalnum_weeks_in_top100 += 1
                num_weeks_in_top100 += 1
        if num_weeks_in_top100 > max_weeks:
            max_weeks = num_weeks_in_top100
        num_weeks.append(num_weeks_in_top100)

print('total num song:', num_songs)
print('maximum #week: {}'.format(max_weeks))
print('average weeks: {:.1f}'.format(totalnum_weeks_in_top100/num_songs))

num_songs_in_weeks = [0 for i in range(5, 71, 5)]
for w in num_weeks:
    num_songs_in_weeks[(w - 1) // 5] += 1

x = np.array(['{:02d}-{:02d}'.format(i-4, i) for i in range(5, 71, 5)])
y = np.array(num_songs_in_weeks)

BarChart_h(x, y, 'Raw data', 'Num of songs', 'Weeks')

print('================[0-100-0]================')
num_songs = 0
num_weeks = []
max_weeks = 0
complete_info = []
with open('result_data_100.csv', newline='', encoding = 'utf8') as csvfile_r:
    dict_rows = csv.DictReader(csvfile_r)
    for id, row in enumerate(dict_rows):   
        data = [v for v in dict(row).values()]
        info, weeks = data[:4], [int(w) for w in data[5:]]
        num_songs += 1
        num_weeks_in_top100 = 0
        max_num_weeks_in_top100 = 0
        for w in weeks:
            if w != 0:
                num_weeks_in_top100 += 1
            else:
                if num_weeks_in_top100 > max_num_weeks_in_top100:
                    max_num_weeks_in_top100 = num_weeks_in_top100
                num_weeks_in_top100 = 0
        if max_num_weeks_in_top100 > max_weeks:
            max_weeks = max_num_weeks_in_top100
        num_weeks.append(max_num_weeks_in_top100)
        complete_info.append(info + [max_num_weeks_in_top100])
        
print('total num song:', num_songs) # 3290
print('maximum #week: {}'.format(max_weeks)) # 56
print('average weeks: {:.1f}'.format(sum(num_weeks)/num_songs)) # 8.2

num_songs_in_weeks = [0 for i in range(4, 69, 4)]
for w in num_weeks:
    num_songs_in_weeks[(w - 1) // 4] += 1

x = np.array(['{:02d}-{:02d}'.format(i-3, i) for i in range(4, 69, 4)])
y = np.array(num_songs_in_weeks)

BarChart_h(x, y, '0-100-0', 'Num of songs', 'Weeks')

print('finding top 5 ...')
complete_info.sort(key=lambda x: x[-1], reverse=True)
for i in complete_info[:5]:
    print(i)
index_row = ['YT URL', 'Artist', 'Song', 'Publish', '#Week']
with open('top5_data.csv', 'w', newline = '', encoding = 'utf8') as csvfile_w:
    writer = csv.writer(csvfile_w)
    writer.writerow(index_row)
    for content in complete_info[:5]: # list ['data', 'data2',...]
        writer.writerow(content)
