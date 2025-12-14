import requests
import json
import pandas as pd
from datetime import datetime

csv_path = "data/bls_data.csv"

#Loading data
existing_df = pd.read_csv(csv_path)

#Ensuring month and year are ints
existing_df['month'] = existing_df['month'].astype(int)
existing_df['year'] = existing_df['year'].astype(int)

#Grabbing max year and month
last_year = existing_df['year'].max()
last_month = existing_df[existing_df['year'] == last_year]['month'].max()

# Determining API start year
start_year = last_year
start_month = last_month + 1

#Accounting for December
if start_month > 12:
    start_year += 1
    start_month = 1

print( last_year, last_month)


#Determining current year
end_year = datetime.now().year

#API call
headers = {'Content-type': 'application/json'}
data = json.dumps({
    "seriesid": ['CUUR0000SA0L1E','CEU0000000001', 'CEU0500000003', 'LNU04000000'],
    "startyear": str(start_year),
    "endyear": str(end_year)
})

p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/',
                  data=data, headers=headers)
json_data = json.loads(p.text)

#For loop to determine new records in API
rows = []
for series in json_data['Results']['series']:
    seriesId = series['seriesID']

    for item in series['data']:
        year = int(item['year'])
        period = item['period']
        #Making the month field an int
        month = int(period.replace("M", ""))

        # Appending new rows
        if (year > last_year) or (year == last_year and month > last_month):
            value = item['value']
            footnotes = ",".join(
                fn["text"] for fn in item.get("footnotes", []) if fn
            )
            
            rows.append({
                "seriesID": seriesId,
                "year": year,
                "period": period,
                "value": value,
                "footnotes": footnotes,
                "month": month
            })

# Converting new rows to dataframe
new_df = pd.DataFrame(rows)

#Creating date field to plot data
if not new_df.empty:
    new_df['date'] = pd.to_datetime(
        new_df["year"].astype(str) + "-" + new_df["month"].astype(str),
        format="%Y-%m"
    )

#Concatenating new rows with old dataframe
final_df = pd.concat([existing_df, new_df], ignore_index=True)
#Saving new file
final_df.to_csv(csv_path, index=False)

print("Updated CSV saved:", csv_path)
print("New rows added:", len(new_df))