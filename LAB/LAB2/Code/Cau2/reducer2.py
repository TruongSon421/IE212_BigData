#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import datetime

current_abbrev = None
current_full_name = None
current_exchange = None
printed_names = set()  # Tập hợp để lưu tên các công ty đã in

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

    # Nếu công ty đã in, bỏ qua
    if current_full_name in printed_names:
        continue

    # Nếu đang xử lý mã công ty hiện tại
    if current_abbrev == abbrev:
        if details_type == 'STOCK':
            date_str = details_values[1]
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                # Kiểm tra xem ngày có nằm trong khoảng từ tháng 01/2005 đến tháng 02/2005 không
                if current_exchange == 'NASDAQ' and date >= datetime(2005, 1, 1) and date <= datetime(2005, 2, 28):
                    # Chỉ in nếu tên chưa in trước đó
                    if current_full_name not in printed_names:
                        print "%s" % (current_full_name)
                        printed_names.add(current_full_name)  # Thêm tên vào tập hợp
                        continue  # Bỏ qua các bản ghi tiếp theo liên quan đến công ty này
            except ValueError:
                continue  # Bỏ qua nếu định dạng ngày không hợp lệ

    else:
        # Nếu gặp một công ty mới
        current_abbrev = abbrev
        current_full_name = None
        current_exchange = None

        if details_type == 'EXCHANGE':
            current_full_name = details_values[1]
            current_exchange = details_values[2]
