

import requests
import json
import pandas as pd
import os

os.makedirs("data", exist_ok=True) #create directory for exporting the csv

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CUUR0000SA0L1E','CEU0000000001','CEU0500000003','LNU04000000'],"startyear":"2020", "endyear":"2025"})
p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)
rows = []
for series in json_data['Results']['series']:
    seriesId = series['seriesID'] 
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes = ",".join(
            fn["text"] for fn in item.get("footnotes", []) if fn
        )
        if 'M01' <= period <= 'M12':
            rows.append({
                "seriesID": seriesId,
                "year": year,
                "period": period,
                "value": value,
                "footnotes": footnotes
            })
df = pd.DataFrame(rows)
df['month'] = df['period'].str.replace("M", "", regex=False)
df['month'] = df['month'].astype(int)
df['date'] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str), format="%Y-%m")

df.to_csv("data/bls_data.csv", index=False)
