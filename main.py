from flask import Flask, request, render_template
import tensorflow

from PIL import Image
import numpy as np
import os

app = Flask(__name__)

# Đường dẫn tới file model Keras đã lưu (my_keras_model.h5)
MODEL_PATH = "model/model1Darknet.h5"
model = tensorflow.keras.models.load_model(MODEL_PATH)

# Đường dẫn thư mục lưu ảnh tải lên
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hàm xử lý ảnh và dự đoán với model Keras
def model_predict(img_path, model):
    # Load ảnh và xử lý
    img = Image.open(img_path)
    img = img.resize((176, 176))  # Điều chỉnh kích thước ảnh phù hợp với model của bạn
    img = tensorflow.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)  # Thêm dimension cho batch size
    img = img / 255.0  # Chuẩn hóa ảnh (nếu cần)

    # Thực hiện dự đoán
    preds = model.predict(img)
    return preds

# Trang chính với form upload ảnh
@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Không tìm thấy file ảnh"
        file = request.files['file']

        if file.filename == '':
            return "Chưa có file ảnh nào được chọn"

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Dự đoán với model Keras
            preds = model_predict(file_path, model)
            prediction = np.argmax(preds, axis=1)[0]  # Lấy lớp dự đoán (chỉ số cao nhất)
            class_names = ['actinic keratosis', 'basal cell carcinoma', 'dermatofibroma', 'melanoma',
                           'nevus', 'pigmented benign keratosis', 'seborrheic keratosis',
                           'squamous cell carcinoma', 'vascular lesion']
            # Thực hiện dự đoán và ánh xạ với tên lớp
            prediction_index = np.argmax(preds, axis=1)[0]
            prediction_class = class_names[prediction_index]

            # Truyền kết quả và đường dẫn ảnh đến HTML
            return render_template('index.html', prediction=prediction_class, image_path=file.filename)

    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)
