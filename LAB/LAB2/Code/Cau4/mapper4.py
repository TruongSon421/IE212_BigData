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
        print "%s\tEXCHANGE,%s" % (abbrev, full_name)

    elif len(data) == 5:
        # Đây là dữ liệu từ stock_data.csv (date, open, high, close, name_file_txt)
        date, open_price, high_price, close_price, name_file = data
        abbrev = name_file.strip().split('.')[0]
	if date == "2005-10-20":
        	print "%s\tOPEN,%s" % (abbrev,open_price)
	if date == "2005-10-25":
		print "%s\tHIGH,%s" % (abbrev,high_price)
