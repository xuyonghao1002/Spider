
from ast import If
import os
import re
import string
import requests
import const


# 处理返回
back_re = re.compile(r"您所访问页面出错啦，或者被删除。")

def check_stop(text):
	res = back_re.search(text)
	return res is not None


def load_img(dir_path, url):
	if not os.path.exists(dir_path):
		print("%s not exist, return" % dir_path)
		return
	
	img_name = url.split("/")[-1]
	img_path = os.path.join(dir_path, img_name)

	if os.path.exists(img_path):
		print("img %s exist, return" % img_path)
		return

	img_resp = requests.get(url=url, headers=const.headers)
	with open(img_path, mode="wb") as f:
		f.write(img_resp.content)
		f.close()

	print("download img %s over!!!" % img_path)


def get_requests_resp(url):
	resp = requests.get(url=url, headers=const.headers)
	resp.encoding = "UTF-8"
	return resp