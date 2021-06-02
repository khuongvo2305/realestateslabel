# K-SOM Visualize
## Cách dùng:
```
git clone https://github.com/khuongvo2305/realestateslabel
cd realestateslabel
source .venv/bin/activate
pip install pandas
pip install pymongo[srv]
python app.py
```
### Chọn 1 điểm trên bản đồ nhập và update giá dựa vào mạng K-SOM tạihttp://127.0.0.1:5000/pickapoint
### Chọn 1 điểm trong DB, nhập và update giá dựa vào mạng K-SOM tại http://127.0.0.1:5000/pickapoint?dataset=all
### Option: 
- Dataset tại trang /pickapoint mặc định là render tất cả các điểm, muốn render 100 điểm mỗi quận  thì thay đổi param: dataset=all100
- Mặc định K-SOM map hiển thị những điểm trong bán kính 2000m, thêm params &radius=3000 nếu muôn đổi bán kính thành 3000.
- File kết quả K-SOM ứng với mỗi lân cập nhật sẽ được lưu vào thư mục Result/ để phục vụ việc Label
# Label
## Cách dùng:
```
git clone https://github.com/khuongvo2305/realestateslabel
cd realestateslabel
source .venv/bin/activate
pip install pandas
pip install pymongo[srv]
python app.py
```
Gán nhãn ở: http://127.0.0.1:5000/label?dataset={dataset}&id={id}&extend={extend} <br>
example: http://127.0.0.1:5000/label?id=533692&dataset=all100&extend=100<br>
Trường extend: Số bài post cùng quận với id=533692 muốn hiển thị thêm.
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
Thêm trường &limitview={numberofpoints} để hiển thị {numberofpoints} điểm<br>
Ví dụ: http://127.0.0.1:5000/label?id=533692&dataset=all100&limitview=500
