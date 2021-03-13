# realestateslabel
```
git clone https://github.com/khuongvo2305/realestateslabel
cd realestateslabel
source .venv/bin/activate
pip install pymongo[srv]
python app.py
```
Gán nhãn ở: http://127.0.0.1:5000/label?dataset={dataset}&id={id} <br>
example: http://127.0.0.1:5000/label?id=294317&dataset=all0<br>
Trong trường hợp tập all0 chưa phân bố đều, em đã generate ra các dataset là all1,all2,all3,all4,all5 để anh Hùng chọn. Các dataset này gồm 100 pos mỗi quận<br>
Các bước label:<br>
Bước 1: Truy cập vào đường dẫn example, post có id=294317 sẽ được set icon khác các marker còn lại<br>
Bước 2: Chọn marker khác và chọn lớp tương quan ứng với post có id=294317 và chọn gán nhãn, data có dạng dưới sẽ được lưu vào MongoDB<br>
```
_id:604c53e997e9b8d0f11c87ce
id1:"294317"
id2:"281974"
class:"1"
date:2021-03-13T05:55:53.345+00:00
```
Bước 3: Sau khi chọn xong các post liên quan vơi id=294317, chọn một post khác làm gốc bằng cách chọn "Gán nhãn cho BĐS này" trong pop-up của post mới hoặc thay đổi tham số id trên đường dẫn.

