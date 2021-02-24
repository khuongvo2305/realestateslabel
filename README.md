# realestateslabel
```
git clone https://github.com/khuongvo2305/realestateslabel
cd realestateslabel
source .venv/bin/activate
pip install pymongo[srv]
python app.py
```
Gán nhãn ở: http://127.0.0.1:5000/label?district={district}
trong đó, district là id của quận, giá trị từ 1 đến 24
Mỗi quận lấy 50-100 điểm đúng, chú ý điểm lấy phân phối đều trên cả quận, có hẻm và mặt tiền.
Quang bắt đầu label quận nào thì nhăn cho anh
