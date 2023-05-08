from time import sleep
import utils
import requests
from lxml import etree
import os
import const


img_root_path = "D:/Picture/3dm"
page_list_xpath = "/html/body/div[2]/div[2]/div[4]/ul/li"
img_list_xpath = "/html/body/div[2]/div[2]/div[3]/p"

current_url = "https://www.3dmgame.com/bagua/5857.html"

def get_img_url_in_page(page_rul):
	resp = utils.get_requests_resp(page_rul)
	tree = etree.HTML(resp.text)

	# 处理某一页
	img_url_list = []
	img_list = tree.xpath(img_list_xpath)
	for item in img_list:
		img_url = item.xpath("./img/@src")
		if img_url:
			img_url = img_url[0]
			if img_url not in img_url_list:
				img_url_list.append(img_url)

	return img_url_list

def down3dm():
	resp = utils.get_requests_resp(current_url)
	tree = etree.HTML(resp.text)

	dir_name = tree.xpath("/html/body/div[2]/div[2]/div[1]/h1")
	dir_name = dir_name[0].text

	page_url_list = []
	page_list = tree.xpath(page_list_xpath)
	for item in page_list:
		url_tail = item.xpath("./a/@href")
		if url_tail:
			page_url = url_tail[0]
			if page_url not in page_url_list:
				page_url_list.append(page_url)

	# print(page_url_list)
	dir_path = os.path.join(img_root_path, dir_name)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	print("start load img in %s, dir path is %s" % (current_url, dir_path))
	for page_url in page_url_list:
		img_url_list = get_img_url_in_page(page_url)
		for img_url in img_url_list:
			utils.load_img(dir_path, img_url)
			sleep(1)
		sleep(1)

	print("download all img over!!!")


if __name__ == '__main__':
	down3dm()