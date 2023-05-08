
from time import sleep
import utils
import requests
from lxml import etree
import os
import const

def get_xiurenb_url():
	_tag = input("请输入套图类型：")
	_id = input("请输入编号：")

	root_url = const.xiuren_root_url
	option_url = "/%s/%s.html"
	real_url = root_url + option_url%(const.picture_tag[_tag], _id)

	return root_url, real_url





def get_img_url_in_page(page_rul):
	resp = utils.get_requests_resp(page_rul)
	tree = etree.HTML(resp.text)

	# 处理某一页
	img_url_list = []
	img_list = tree.xpath("/html/body/div[3]/div/div/div[5]/p/img")
	for item in img_list:
		img_url = item.xpath("./@src")
		if img_url:
			img_url = const.xiuren_root_url + img_url[0]
			if img_url not in img_url_list:
				img_url_list.append(img_url)

	return img_url_list


def download_xiuren():
	root_url, url = get_xiurenb_url()
	print(url)
	resp = utils.get_requests_resp(url)

	# 解析一套
	# 得到各个子url

	page_url_list = []
	tree = etree.HTML(resp.text)
	dir_name = tree.xpath("/html/body/div[3]/div/div/div[1]/h1")
	dir_name = dir_name[0].text
	person_name = tree.xpath("/html/body/div[3]/div/div/div[2]/div/a[3]/span")
	person_name = person_name[0].text

	page_list = tree.xpath("/html/body/div[3]/div/div/div[4]/div/div/a")
	for item in page_list:
		url_tail = item.xpath("./@href")
		if url_tail:
			url_tail = url_tail[0]
			page_url = root_url + url_tail
			if page_url not in page_url_list:
				page_url_list.append(page_url)

	dir_path = os.path.join(const.xiuren_img_root_path, person_name, dir_name)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	print("start load img in %s, dir path is %s" % (url, dir_path))
	for page_url in page_url_list:
		img_url_list = get_img_url_in_page(page_url)
		for img_url in img_url_list:
			utils.load_img(dir_path, img_url)
			sleep(1)
		sleep(1)

	print("download all img over!!!")