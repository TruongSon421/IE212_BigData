#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

current_abbrev = None
open_price_20 = None
high_price_25 = None
company_full_name = None

# Đọc từng dòng từ stdin
for line in sys.stdin:
    if not line.strip():
        continue

    # Chia tách dữ liệu thành abbrev và các chi tiết khác
    data = line.strip().split('\t')
    if len(data) != 2:
        continue

    abbrev, details = data
    details_values = details.split(',')

    details_type = details_values[0]

    # Nếu đang xử lý cùng một công ty (abbrev)
    if current_abbrev == abbrev:
        if details_type == 'OPEN':
            open_price_20 = float(details_values[1])
        elif details_type == 'HIGH':
            high_price_25 = float(details_values[1])
        elif details_type == 'EXCHANGE':
            company_full_name = details_values[1]

        # Khi đã có giá mở phiên ngày 20/10 và giá cao nhất ngày 25/10
        if open_price_20 is not None and high_price_25 is not None and company_full_name is not None:
            profit = high_price_25 - open_price_20
            if profit > 0:
                # In ra tên công ty và lợi nhuận
                print "%s\t%.2f" % (company_full_name, profit)

            # Reset các giá trị sau khi xử lý xong công ty hiện tại
            open_price_20 = None
            high_price_25 = None

    else:
        # Chuyển sang công ty mới
        current_abbrev = abbrev
        open_price_20 = None
        high_price_25 = None
        company_full_name = None

        if details_type == 'OPEN':
            open_price_20 = float(details_values[1])
        elif details_type == 'HIGH':
            high_price_25 = float(details_values[1])
        elif details_type == 'EXCHANGE':
            company_full_name = details_values[1]
