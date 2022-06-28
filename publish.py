import csv
import matplotlib.pyplot as plt
import numpy as np

def DeltaWeeks(publish):
    year, month, day = publish['y'], publish['m'], publish['d']
    # print(year, month, day)
    if year == 2016:
        delta_month = {0:0, 1:4, 2:35, 3:65, 4:96, 5:126, 6:157, 7:188, 8:218, 9:249, 10:279}
        delta_day = delta_month[month - 2] + day
    elif year < 2020:
        delta_month = {1:0, 2:31, 3:28, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}
        delta_day = 310
        delta_day += day
        for i in range(1, month + 1):
            delta_day += delta_month[i]
        for i in range(2017, year):
            delta_day += 365
    elif year == 2020:
        delta_month = {1:0, 2:31, 3:29, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}
        delta_day = 1405
        delta_day += day
        for i in range(1, month + 1):
            delta_day += delta_month[i]
    else:
        delta_month = {1:0, 2:31, 3:28, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}
        delta_day = 1771
        delta_day += day
        for i in range(1, month + 1):
            delta_day += delta_month[i]
        for i in range(2021, year):
            delta_day += 365
    return delta_day // 7

def BarChart_h(x, y, title, x_label, y_label):
    bar = plt.barh(x, y)
    plt.bar_label(bar, y)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.show()

from_0to100_list = []
total_weeks_0to100, num_songs = 0, 0
max_0to100 = 0

with open('result_data.csv', newline='', encoding = 'utf8') as csvfile_r:
    dict_rows = csv.DictReader(csvfile_r)
    for id, row in enumerate(dict_rows):   
        data = [v for v in dict(row).values()]
        info, weeks = data[:4], [int(w) for w in data[5:]]
        date = info[3]
        publish = {'y':int(date[:4]), 'm':int(date[5:7]), 'd':int(date[8:])}
        from_0to100 = 0
        for w in weeks:
            if w != 0:
                break
            else:
                from_0to100 += 1
        from_0to100 -= DeltaWeeks(publish)
        if from_0to100 < 0:
            continue
        num_songs += 1
        total_weeks_0to100 += from_0to100
        from_0to100_list.append(from_0to100)
        if max_0to100 < from_0to100:
            max_0to100 = from_0to100

print('total num song:', num_songs)
print('maximum #week: {}'.format(max_0to100))
print('average weeks: {:.1f}'.format(total_weeks_0to100/num_songs))

num_songs_in_weeks = [0 for i in range(20, 301, 20)]
for w in from_0to100_list:
    num_songs_in_weeks[(w - 1) // 20] += 1

x = np.array(['{:03d}-{:03d}'.format(i-19, i) for i in range(20, 301, 20)])
y = np.array(num_songs_in_weeks)

BarChart_h(x, y, 'Weeks from published to Top100', 'Num of songs', 'Weeks')

        