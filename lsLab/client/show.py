import pandas as pd
from beautifultable import BeautifulTable

import urllib
import json
import sys
import codecs


url = 'http://172.21.39.128/phpapi/index.php'

# readObj = urllib.request.urlopen(url)

# response = readObj.read()

# data = json.loads(response.decode())

# member = pd.read_csv('member.csv', index_col=0)
# status = ["In Lab", "In School", "Disapper"]
#member = pd.read_json('member.json')

# member = pd.DataFrame(data)
status = ["No Lab", "In Lab"]

member = pd.read_json('./member.json', convert_dates=['lastin', 'lastout'])

print('')
print('===============================================================================')
print('================================ Yoshida Lab ==================================')
print('===============================================================================')
print('')

table = BeautifulTable()
table.column_headers = ["Name", "Status", "Last In", "Last Out", "Total"]

# [Ploblem] pandasの小数点切り落とし
for number, data in member.iterrows():
	table.append_row([str(data['name']), status[data['status']],str(data['lastin']),str(data['lastout']), str(pd.Timedelta(data['totalStay']*1000000))])

print(table)



