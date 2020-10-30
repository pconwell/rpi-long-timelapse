import pandas as pd
import glob
import csv
import datetime

pd.set_option('display.max_columns', None)


month = 1
start_year = 2019
end_year = 2038
country = 'usa'
city = 'nashville'

# Loop and download the year(s) you want
year = start_year
while year < end_year:

    while month < 13:

        data = pd.read_html(f"https://www.timeanddate.com/sun/{country}/{city}?month={month}&year={year}")

        df = data[0]

        # drop the last row, which is just a footnote
        df.drop(df.tail(n=1).index,inplace=True)

        # rename and drop columns
        df.columns = ['day', 'sunrise', 'sunset', 'length', 'difference', 'asunrise', 'asunset', 'nsunrise', 'nsunset', 'csunrise', 'csunset', 'noon', 'milmi']
        df = df.drop(['length', 'difference', 'noon', 'milmi'], axis = 1)

        # remove the arrows and degrees from times
        # this probably need to be fixed in case of locations that might have sunrise/sunset at a time
        # that has a 2 digit hour. e.g. a sunset at 10:15 pm.
        df['sunrise'] = df['sunrise'].str[:7]
        df['sunset'] = df['sunset'].str[:7]

        # rearrange columns to be in time order
        df = df[['asunrise', 'nsunrise', 'csunrise', 'sunrise', 'sunset', 'csunset', 'nsunset', 'asunset']]

        # drop columns with 'note'
        df.drop(df[df['asunrise'].str[:4] == "Note"].index, inplace=True)

        # zero pad the month so that the files sort correctly
        if len(str(month)) == 1:
            df.to_csv(f'./csv_files/{year}0{month}.csv')
        else:
            df.to_csv(f'./csv_files/{year}{month}.csv')

        # reset the month and start the loop over for the next year
        if month == 12:
            month = 1
            break
        else:
            month += 1

    year += 1


# read a list of all the csv files we just downlaoded
csv_files = glob.glob("./csv_files/*.csv")


# read over each csv file one by one and add the next one to the bottom
header_saved = False
with open(f'output.csv','w') as fout:
    for filename in csv_files:
        with open(filename) as fin:
            header = next(fin)
            if not header_saved:
                fout.write(header)
                header_saved = True
            for line in fin:
                fout.write(line)


# fix and clean up the csv file
i = -1

with open(f'{city}.csv', mode='w', newline='') as out_file:
    out_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    with open('output.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if i == -1: #write out header row
                out_writer.writerow(['date', row[1], row[2], row[3], row[4],row[5], row[6], row[7], row[8]])
            else:
                out_writer.writerow([
                                     str(datetime.date(start_year, month, 1) + datetime.timedelta(i)),
                                     row[1][:-3], #am
                                     row[2][:-3], #am
                                     row[3][:-3], #am
                                     row[4][:-3], #am
                                     f"{str(int(row[5][:-3].split(':')[0]) + 12)}:{row[5][:-3].split(':')[1]}",
                                     f"{str(int(row[6][:-3].split(':')[0]) + 12)}:{row[6][:-3].split(':')[1]}",
                                     f"{str(int(row[7][:-3].split(':')[0]) + 12)}:{row[7][:-3].split(':')[1]}",
                                     f"{str(int(row[8][:-3].split(':')[0]) + 12)}:{row[8][:-3].split(':')[1]}"
                                     ])

            i += 1

print('done')
