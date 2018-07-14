#coding:utf-8
'''
created by starlee @ 2018-07-14 10:45
for fetching json infos
'''
import time
import logging
import sys
from config import config
import threading
lock = threading.RLock()

logger = logging.getLogger()
hdlr = logging.FileHandler("log/get_json_info.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)

INTERVAL_TIME = config["json_fetch_interval"]
REPO_ID = {}
PRJS = []
PRJS_DONE = [] #多线程干完活后放到这个里面
DEFAULT_THD_NUM = 3 # 默认线程个数

def _fetchJson(prj, dataType):

	# 获取 *_json_raw 的最大page值 -> last_page
	# 获取 *_info 中 last_page对应的数据集合 -> last_data
	# 如果 len(last_data)  == 100 则 next_page = last_page；否则next_pge = next_page

	while True:
		pass
		# 远程访问next page对应的数据
		# 先存储原始数据，再抽取存储条目数据
		# 抽取next url，不存在的话，退出


def fetchThread():
	logger.info("%s start to work"%( threading.current_thread().name))
	while True:
		lock.acquire()
		try:
			prj = PRJS.pop(0)
			logger.info("%s fetch %s"%( threading.current_thread().name,prj))
		except Exception,e:
			logger.info("%s no more prjs"%( threading.current_thread().name))
			break 
		finally:
			lock.release()

		_fetchJson(prj, "issues")
		_fetchJson(prj, "pulls")

		lock.acquire()
		try:
			PRJS_DONE.append(prj)
		finally:
			lock.release()


def fetchJsonInfo():
	global PRJS_DONE, PRJS
	# 用多线程进行并行操作
	if len(sys.argv) < 2:
		threading_num = DEFAULT_THD_NUM
	else:
		threading_num = int(sys.argv[1])

	thread_list = [] 
	if threading_num > len(PRJS):
		threading_num = len(PRJS)

	for i in range(0,threading_num):
		t = threading.Thread(target=fetchThread,name="Thread-%d"%i)
		thread_list.append(t)

	for thread in thread_list:
		thread.start()
	for thread in thread_list:
		thread.join()

	logger.info("all threads done work")
	PRJS = PRJS_DONE
	PRJS_DONE = []

	
def readPrjLists():
	prjs = []
	with open("prjs.txt","r") as fp:
		for prj_line in fp.readlines():
			prjls = prj_line.split("\t")
			prjs.append(prjls[1])
			REPO_ID[prjls[1]] = int(prjls[0])
	return prjs

def main():
	global PRJS
	while True:

		logger.info("start another round of work")
		# 爬完历史信息后，每个一天更新一次
		start_time = time.time()

		PRJS = readPrjLists()
		fetchJsonInfo()
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("not enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)

def launchTokenPool():
	pass
def createTable():
	pass
def init():
	# 启动token池 
	launchTokenPool()
	# 创建表
	createTable()
if __name__ == '__main__':
	init()
	main()