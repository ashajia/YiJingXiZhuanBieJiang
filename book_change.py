#!/usr/bin/python3
import requests
from lxml import etree
import os, re, json

index_url = 'http://www.quanxue.cn/ct_nanhuaijin/XiChiIndex.html'
base_url = 'http://www.quanxue.cn/ct_nanhuaijin'
headers = {
		'User-Agent': 
		'Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36  \
		(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
		}

def get_index(url):
	# 获取目录页内容
	rps = requests.get(url, headers = headers)
	rps.encoding = 'utf-8'
	# 源站多了一个空li节点，此处删掉
	response = re.sub(r'<li class="index_left_td"></li>','',rps.text)
	return response

class ParserIndex:
	def __init__(self, text):
		self.html = etree.HTML(text, etree.HTMLParser())
		# 获取大标题
		self.title_0 = self.html.xpath('//div[@id="la" and @class="index_center_td"]/h3/text()')
		# 获取一级标题内容
		#self.title_1_node = self.html.xpath('//div[@class="index_center_td"]/h3/a')
		self.title_chap_node = self.html.xpath('//div[@class="chap"]')
	

	def parser_title(self):
		self.title_1_list = []
		self.index_dict = {}
		for chap1 in self.title_chap_node:
			title_1 = chap1.find('.div[@class="index_center_td"]/h3/a')
			self.title_1_list.append(title_1.text)

		# enumerate 遍历列表的下标和值
		for idx, chap2 in enumerate(self.title_chap_node):
			self.title_2_dict = {}
			title_2_number_list = chap2.findall('.ul/li')
			title_2_list = chap2.findall('.ul/li/a')
			for idx_2, title_2 in enumerate(title_2_list):
				title_2_full = title_2_number_list[idx_2].text + title_2.text
				self.title_2_dict[title_2_full] = title_2.attrib['href']
			
			self.index_dict[self.title_1_list[idx]] = self.title_2_dict
		return self.index_dict


	def print_title_2(self):
		print(self.parser_title())


def get_url(index):
	# 参数为目录字典
	content_name_url = {}
	chapter = 0
	for header_1,title_url in index.items():
		chapter += 1
		for title,url in title_url.items():
			if chapter <= 12:
				file_name = '系辞上传/{}/{}.md'.format(header_1, title)
			else:
				file_name = '系辞下传/{}/{}.md'.format(header_1, title)
			full_url = '{}/{}'.format(base_url, url)
			content_name_url[file_name] = full_url

	return content_name_url



if __name__ == '__main__':
	index_text = get_index(index_url)
	p = ParserIndex(index_text)
	index = p.parser_title()
	print(json.dumps(get_url(index),sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False))
