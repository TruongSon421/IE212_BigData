#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

# Đọc từng dòng từ stdin
for line in sys.stdin:
    if not line.strip():
        continue

    data = line.strip().split(',')

    if len(data) == 3:
        # Đây là dữ liệu từ exchanges.csv (ct, full_name, exchange)
        abbrev, full_name, exchange = data
	if exchange == "NYSE":
        	print "%s\tEXCHANGE,%s" % (abbrev, full_name)

    elif len(data) == 5:
        # Đây là dữ liệu từ stock_data.csv (date, open, high, close, name_file_txt)
        date, open_price, high_price, close_price, name_file = data
        term = name_file.strip().split('.')
        abbrev = term[0]  # Lấy phần viết tắt từ tên tệp
        print "%s\tSTOCK,%s,%s,%s" % (abbrev, date, open_price, close_price)
