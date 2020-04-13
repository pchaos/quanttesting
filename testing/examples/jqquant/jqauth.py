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
print("验证：{}".format(is_auth()))
print("JoinQuant 使用情况：", get_query_count())
