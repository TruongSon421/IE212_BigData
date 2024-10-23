#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

current_abbrev = None
current_full_name = None
current_exchange = None
printed_names = set()  # Sử dụng set để lưu trữ tên đã in

# Đọc từng dòng từ stdin
for line in sys.stdin:
    if not line.strip():
        continue

    data = line.strip().split('\t')
    if len(data) != 2:
        continue

    abbrev, details = data
    details_values = details.split(',')  # Chia tách phần còn lại của dữ liệu

    details_type = details_values[0]  # Loại dữ liệu (EXCHANGE hoặc STOCK)

    # Nếu đã gặp mã viết tắt hiện tại
    if current_abbrev == abbrev:
        if details_type == 'STOCK':
            open_price = float(details_values[1])  # Giá mở
            close_price = float(details_values[2])  # Giá đóng
            # Kiểm tra xem giá mở có lớn hơn giá đóng và sàn là NYSE không
            if open_price > close_price and current_exchange == 'NYSE':
                if current_full_name not in printed_names:
                    print "%s" % (current_full_name)  # In ra tên đầy đủ
                    printed_names.add(current_full_name)  # Đánh dấu tên đã in

    else:
        # Nếu đang xử lý một mã viết tắt khác
        if current_abbrev is not None:
            # Không cần làm gì ở đây
            pass
        
        current_abbrev = abbrev
        current_full_name = None  # Reset tên đầy đủ
        current_exchange = None  # Reset sàn giao dịch

        if details_type == 'EXCHANGE':
            current_full_name = details_values[1]  # Lưu tên đầy đủ
            current_exchange = details_values[2]  # Lưu sàn giao dịch

# In ra tên đầy đủ cuối cùng nếu cần
if current_abbrev is not None and current_full_name is not None:
    if current_full_name not in printed_names and current_exchange == 'NYSE':
        print "%s" % (current_full_name)  # Chỉ in ra tên đầy đủ cuối cùng nếu chưa in
