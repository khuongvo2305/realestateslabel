# realestateslabel
## Cách dùng:
```
git clone https://github.com/khuongvo2305/realestateslabel
cd realestateslabel
source .venv/bin/activate
pip install pymongo[srv]
python app.py
```
Gán nhãn ở: http://127.0.0.1:5000/label?dataset={dataset}&id={id} <br>
example: http://127.0.0.1:5000/label?id=533692&dataset=all100<br>
Các bước label:<br>
Bước 1: Truy cập vào đường dẫn example, post có id=533692 sẽ được set icon khác các marker còn lại<br>
Bước 2: Chọn marker khác và chọn lớp tương quan ứng với post có id=533692 và chọn gán nhãn, data có dạng dưới sẽ được lưu vào MongoDB<br>
```
_id:604c53e997e9b8d0f11c87ce
id1:"533692"
id2:"281974"
class:"1"
date:2021-03-13T05:55:53.345+00:00
```
Bước 3: Sau khi chọn xong các post liên quan vơi id=533692, chọn một post khác làm gốc bằng cách chọn "Gán nhãn cho BĐS này" trong pop-up của post mới hoặc thay đổi tham số id trên đường dẫn.<br>
<br>
## Cách tạo dataset:<br>
Các dataset được lưu ở folder /dataset<br>
Ví dụ: /dataset/all100.csv là dataset chứa 100 posts mỗi quận.<br>
Để generate Dataset mới, gọi http://127.0.0.1:5000/dataset?limit={limit}, backend sẽ kiểm tra, nếu chưa có data set tên all{limit}.csv trong thư mục /dataset thì sẽ tạo ra file all{limit}.csv chứa {limit} post cho môi quận.<br>
Sau đó, truy cập http://127.0.0.1:5000/label?dataset={all{limit}} để bắt đầu gán nhãn.<br>
Ví dụ:<br>
Bước 1: http://127.0.0.1:5000/dataset?limit=150 <br>
Bước 2: Gán nhãn ở http://127.0.0.1:5000/label?dataset=all150
<br>
## Testing:<br>
Thêm trường &limitview{numberofpoints} để hiển thị {numberofpoints} điểm<br>
Ví dụ: http://127.0.0.1:5000/label?id=533692&dataset=all100&limitview=500
