#!/usr/bin/python3
import book_change as bc

url = 'http://www.quanxue.cn/ct_nanhuaijin/XiChiIndex.html'
text = bc.get_index(url)
p = bc.ParserIndex(text)
print('-' * 70)
p.parser_title()
p.print_title_2()
