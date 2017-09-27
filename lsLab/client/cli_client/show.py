import pandas as pd
from texttable import Texttable

import urllib
import json
import sys
import codecs

"""
Get the json file from server

url: server url
jsonlist: gotten json object
"""

url = 'http://172.21.39.193/phpapi/index.php'

readObj = urllib.request.urlopen(url)

response = readObj.read()

jsonlist = response.decode()

status = ["No Lab", "In Lab"]

member = pd.read_json(jsonlist, convert_dates=['lastin', 'lastout'])

print('')
print('===============================================================================')
print('================================ Yoshida Lab ==================================')
print('===============================================================================')
print('')

# define the table object
table = Texttable()
table.column_headers = ["Name", "Status", "Last In", "Last Out", "Total"]

# add the each data
for number, data in member.iterrows():
	table.add_row([str(data['name']), status[data['status']],str(data['lastin']),str(data['lastout']), str(pd.Timedelta(data['totalStay']*1000000)).split(".")[0]])

# show table
print(table.draw())



