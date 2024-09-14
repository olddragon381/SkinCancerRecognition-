from flask import Flask, request, render_template, flash, redirect, url_for
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import json

app = Flask(__name__)

# Cấu hình kích thước file tải lên tối đa là 5MB
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.secret_key = 'supersecretkey'  # Cần cho việc hiển thị thông báo

# Tải mô hình Keras
MODEL_PATH = "model/model1CNN.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Thư mục lưu ảnh tải lên
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tên các lớp tương ứng với dự đoán
class_names = ['actinic keratosis', 'basal cell carcinoma', 'dermatofibroma', 'melanoma',
               'nevus', 'pigmented benign keratosis', 'seborrheic keratosis',
               'squamous cell carcinoma', 'vascular lesion']

# Tải dữ liệu bệnh từ tệp JSON vào một từ điển
with open('data/diseases.json', 'r', encoding='utf-8') as file:
    content = file.read()  # Đọc nội dung JSON dưới dạng chuỗi
    disease_data = json.loads(content)  # Phân tích chuỗi JSON thành từ điển

# Xử lý ảnh và dự đoán với mô hình
def model_predict(img_path, model):
    img = Image.open(img_path)
    img = img.resize((176, 176))  # Thay đổi kích thước ảnh để phù hợp với mô hình
    img = np.asarray(img) / 255.0  # Chuẩn hóa ảnh
    img = np.expand_dims(img, axis=0)  # Thêm dimension cho batch size

    preds = model.predict(img)
    return preds

# Xử lý lỗi khi file tải lên quá kích thước
@app.errorhandler(413)
def file_too_large(e):
    flash("File quá lớn. Kích thước tối đa cho phép là 5MB.")
    return render_template('index.html', prediction=None), 413

# Trang chính với form tải ảnh lên
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            flash("Chưa chọn file ảnh để tải lên.")
            return render_template('index.html', prediction=None), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Dự đoán với mô hình
        preds = model_predict(file_path, model)
        prediction_index = np.argmax(preds, axis=1)[0]
        prediction_class = class_names[prediction_index]

        # Chuyển hướng đến trang thông tin chi tiết về bệnh
        return redirect(url_for('disease_info', disease=prediction_class))

    return render_template('index.html', prediction=None)

# Trang thông tin chi tiết về bệnh
@app.route('/disease/<disease>', methods=['GET'])
def disease_info(disease):
    # Tìm thông tin bệnh trong từ điển
    disease_detail = disease_data.get(disease, None)
    if disease_detail is None:
        flash("Thông tin về bệnh không được tìm thấy.")
        return redirect(url_for('index'))
    return render_template('disease_info.html', disease=disease_detail)

if __name__ == '__main__':
    app.run(debug=True)
