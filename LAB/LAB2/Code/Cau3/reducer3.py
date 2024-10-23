#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import datetime

current_abbrev = None
current_full_name = None
july_open_price = None
august_close_price = None
printed_names = set()

# Đọc từng dòng từ stdin
for line in sys.stdin:
    if not line.strip():
        continue

    data = line.strip().split('\t')
    if len(data) != 2:
        continue

    abbrev, details = data
    details_values = details.split(',')

    details_type = details_values[0]

    # Nếu đang xử lý cùng một mã công ty
    if current_abbrev == abbrev:
        if details_type == 'STOCK':
            date_str = details_values[1]
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')

                # Xử lý tháng 07/2007
                if date.month == 7 and date.year == 2007:
                    july_open_price = float(details_values[2])
                # Xử lý tháng 08/2007
                elif date.month == 8 and date.year == 2007:
                    august_close_price = float(details_values[3])

                    # Nếu đã có giá mở phiên của tháng 07 và giá đóng phiên của tháng 08
                    if july_open_price is not None and august_close_price is not None:
                        if august_close_price < july_open_price:
                            # Kiểm tra công ty chưa được in ra
                            if current_full_name not in printed_names:
                                print "%s" % (current_full_name)
                                printed_names.add(current_full_name)
                                # Đặt lại giá trị để không bị nhầm với công ty khác
                                july_open_price = None
                                august_close_price = None
            except ValueError:
                continue  # Bỏ qua nếu có lỗi về ngày hoặc số liệu không hợp lệ

    else:
        # Chuyển sang công ty mới
        current_abbrev = abbrev
        current_full_name = None
        july_open_price = None
        august_close_price = None

        if details_type == 'EXCHANGE':
            current_full_name = details_values[1]
