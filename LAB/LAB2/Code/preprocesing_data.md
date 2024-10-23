# Xử Lý File Trước Khi Đưa Lên HDFS

## A. Xử lý file Stock
Trước khi tải dữ liệu lên HDFS (Hadoop Distributed File System), xử lý các file stock thành một file do có chung cấu trúc

### Các Bước Xử Lý : Xử lý trên command line
#### 1. Xóa đi dòng đầu tiên của mỗi file stock và thêm tên file vào cuối mỗi dòng của mỗi file

- **File Stock ban đầu**


```plaintext
Date,Open,High,Low,Close,Volume,OpenInt
2016-03-31,9.95,9.95,9.95,9.95,400,0
2016-04-26,9.95,9.95,9.9499,9.9499,2700,0
```

```bash
for file in *.txt; do
    tail -n +2 "$file" > temp && mv -f temp "$file"
    awk -v filename="$file" '{sub(/\r$/,""); printf "%s,%s\n", $0, filename}' "$file" > temp && mv -f temp "$file"
done
```

- **Kết quả sau xử lý**


```plaintext
2016-03-31,9.95,9.95,9.95,9.95,400,0,rose.us.txt
2016-04-26,9.95,9.95,9.9499,9.9499,2700,0,rose.us.txt
```

#### 2. Gộp lại tất cả file stock lại thành một file lớn
```bash
cat Stocks/*.txt > merged_file.txt
```

#### 3. Xóa các cột không cần thiết
- Do yêu cầu trong analysis.ipynb không cần sử dụng các cột như : Low, Volume,OpenInt nên xóa đi để tối ưu dung lượng

```bash
cut -d',' -f1,2,3,5,8 merged_file.txt > filtered_merged_file.txt
```
- **Kết quả cuối cùng**

```plaintext
2016-03-31,9.95,9.95,9.95,rose.us.txt
2016-04-26,9.95,9.95,9.9499,rose.us.txt
```
## B. Xử lý file Stock_info.csv
- **File Stock_info.csv**

```plaintext
Ticker,Name,Exchange
ZNH,China Southern Airlines Company,NYSE
ZQK,Quiksilver,NYSE
ZTR,Zweig Total Return Fund,NYSE
ZTS,Zoetis Inc. Class A Common Stoc,NYSE
ZX,China Zenix Auto International,NYSE
AAIT,AC Asia Information Tech MSCI Ishares,NASDAQ
AAME,Atlantic American Corp.,NASDAQ
AAON,Aaon,NASDAQ
AAPL,Apple Inc.,NASDAQ
AAWW,Atlas Air Worldwide Holdings,NASDAQ
```

### 1. Xóa dòng đầu tiên 

```bash
sed -i '1d' stock_info.csv
```
- **Kết quả**
```plaintext
ZNH,China Southern Airlines Company,NYSE
ZQK,Quiksilver,NYSE
ZTR,Zweig Total Return Fund,NYSE
ZTS,Zoetis Inc. Class A Common Stoc,NYSE
ZX,China Zenix Auto International,NYSE
AAIT,AC Asia Information Tech MSCI Ishares,NASDAQ
AAME,Atlantic American Corp.,NASDAQ
AAON,Aaon,NASDAQ
AAPL,Apple Inc.,NASDAQ
AAWW,Atlas Air Worldwide Holdings,NASDAQ
```
### 2: Xử lý cột Ticker
- Chuyển chữ hoa thành chữ thường và chuyển '-' thành dấu '_' trong cột Ticker để có thể kết hợp với filtered_merged_file.txt

```bash
sed 's/^\([^,]*\)/\L\1/; s/-/_/g' stock_info.csv > process_stock_info.txt
```
- **Kết quả**

```plaintext
znh,China Southern Airlines Company,NYSE
zqk,Quiksilver,NYSE
ztr,Zweig Total Return Fund,NYSE
zts,Zoetis Inc. Class A Common Stoc,NYSE
zx,China Zenix Auto International,NYSE
aait,AC Asia Information Tech MSCI Ishares,NASDAQ
aame,Atlantic American Corp.,NASDAQ
aaon,Aaon,NASDAQ
aapl,Apple Inc.,NASDAQ
aaww,Atlas Air Worldwide Holdings,NASDAQ
```
# Đẩy file lên HDFS

```bash
hdfs dfs -mkdir inputLAB/LAB2
hdfs dfs -put filtered_merged_file.txt  inputLAB/LAB2
hdfs dfs -put process_stock_info.txt  inputLAB/LAB2
```

# Hadoop Streaming

```bash
hadoop jar usr/lib/hadoop-mapreduce/hadoop-streaming-2.6.0-cdh5.13.0.jar \
        -file home/cloudera/workspace/HadoopStreaming/mapper.py -mapper 'python mapper.py' \
        -file home/cloudera/workspace/HadoopStreaming/reducer.py -reducer 'python reducer.py' \
        -input inputLAB/LAB2/filtered_merged_file.txt -inputformat TextInputFormat \
        -input inputLAB/LAB2/process_stock_info.txt  \
        -output outputLAB/LAB2a
```