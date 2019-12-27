import pandas
import os
from jqdatasdk import *
from dotenv import load_dotenv

def getEnvVar(key):
	load_dotenv(verbose=True)
	return os.getenv(key)

# .env  文件中写入相应的参数
userid=getEnvVar('jquserid')
passwd=getEnvVar('jqpasswd')
assert userid 
auth(userid,passwd)
# auth('userid','passwd')
# pd = get_price(security='399300.XSHE',frequency='60m')
pd = get_price(security='399300.XSHE',frequency='1d')
pd.to_csv('399300.csv', encoding = 'utf-8', index = False)
print(pd.head())
print(get_query_count())