import pandas as pd
import datetime
import sys


# (予備) データの生成
def cre_csvfile():
	member = pd.DataFrame(
		{'name': ['SASATANI', 'NAKAYAMA', 'ZHUO', 'RYONAI'],
		 'lastin': [pd.to_datetime('2017-9-19 10:00'), pd.to_datetime('2017-9-19 11:00'), pd.to_datetime('2017-9-19 12:00'), pd.to_datetime('2017-9-19 13:00')],
		 'lastout': [pd.to_datetime('2017-9-19 09:00'), pd.to_datetime('2017-9-19 10:00'), pd.to_datetime('2017-9-19 11:00'), pd.to_datetime('2017-9-19 12:00')],
		 'status': [0, 0, 0, 0],
		 'totalStay': [pd.to_timedelta(0), pd.to_timedelta(0), pd.to_timedelta(0), pd.to_timedelta(0)]},
		 columns=['name', 'status', 'lastin', 'lastout', 'totalStay'])
	print(member)

	member.to_json('member.json')

# ファイル読み込み
def setup():

	member = pd.read_json('./member.json', convert_dates=['lastin', 'lastout', 'totalStay'])

	return member

# 入室処理
def in_upload(member, target):

	# 現在時刻を取得
	nowtime = datetime.datetime.now()

	member.loc[(member.name == str(target), 'lastin')] = pd.to_datetime(nowtime.strftime("%Y-%m-%d %H:%M:%S"))
	member.loc[(member.name == str(target), 'status')] = 1

	member.to_json('member.json')

# 外出処理
def out_upload(member, target):

	# 現在時刻を取得
	nowtime = datetime.datetime.now()
	
	# lastin - lastout
	add_time = pd.to_datetime(nowtime) - pd.to_datetime(member.loc[(member.name == str(target), 'lastin')].values[0])
	
	print(add_time)
	print(pd.to_timedelta(member.loc[(member.name == str(target), 'totalStay')]))

	member.loc[(member.name == str(target), 'lastout')] = pd.to_datetime(nowtime.strftime("%Y-%m-%d %H:%M:%S"))
	member.loc[(member.name == str(target), 'status')] = 0
	member.loc[(member.name == str(target), 'totalStay')] = (pd.to_timedelta(member.loc[(member.name == str(target), 'totalStay')]*1000000) + pd.to_timedelta(add_time))
	 
	member.to_json('member.json')




if __name__ == '__main__':

	argvs = sys.argv
	argc = len(argvs)
	if (argc != 3):
		print("Usage:" + argvs[0])
		quit()

	target = argvs[1]

	method = argvs[2]

	member = setup()

	if(method == "in"):
		in_upload(member, target)
	elif(method == "out"):
		out_upload(member, target)
	else:
		print("Unknown option " + str(argvs[2]))



