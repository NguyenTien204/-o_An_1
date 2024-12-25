import os
import pandas as pd
import numpy as np
from flask import jsonify, render_template, request, session
from models.causal_model import predict_causes
from models.prediction_model import train_and_predict_with_predicted_causes
from utils import check_file_exists, predicted_causes_file, data_dir
from models.prediction_model import get_visualization_data
from main import app

# Load file csv
# Đường dẫn file CSV
csv_file_path =  os.path.join(data_dir, 'climate_data.csv')

# Hàm đọc dữ liệu theo khối (chunking)
def read_data_in_chunks(file_path, chunk_size=1000):
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield chunk

# Hàm ghép tất cả các khối dữ liệu lại thành một dataframe
def get_all_data(file_path):
    data = pd.DataFrame()
    for chunk in read_data_in_chunks(file_path):
        data = pd.concat([data, chunk], ignore_index=True)
    return data

#------------------------------Load Template----------------------------------------------------------------------->

def setup_routes(app):
    # Trang index
    @app.route('/')
    def index():
        return render_template('index.html')
    
#------------------------------Lấy dữ liệu ban đầu để vẽ biểu đồ--------------------------------------------------->

    @app.route('/chart-data', methods=['GET'])
    def chart_data():
        if check_file_exists(csv_file_path):
            climate_data = get_all_data(csv_file_path)
            chart_data = get_visualization_data(climate_data)
            return jsonify(chart_data)
        else:
            return jsonify({'error': 'CSV file not found.'}), 400
        
#-----------------------------Dự đoán các dữ liệu đầu vào---------------------------------------------------------->

    @app.route('/train-causes', methods=['POST'])
    def train_causes():
        year = request.args.get('year', default=2050, type=int)
        session['year'] = year
        predict_causes(csv_file_path, year)
        return jsonify({'status': f'Cause variables predicted and saved successfully for year {year}'})
        
    
#------------------------------Dự đoán tác động của biến đổi khí hậu----------------------------------------------->

    @app.route('/train-predictions', methods=['POST'])
    def train_predictions():
        if not check_file_exists(predicted_causes_file):
            return jsonify({'error': 'Predicted causes file not found. Please run /train-causes first.'}), 401

        year = session.get('year')
        predicted_data = train_and_predict_with_predicted_causes(csv_file_path,predicted_causes_file,year)

        if predicted_data is None:
            return jsonify({'error': 'Model not trained yet. Please train the model first.'}), 402

        # Trả về dữ liệu vẽ biểu đồ
        chart_data = get_visualization_data(predicted_data)
        return jsonify(chart_data)
    
#-------------------------------------Vẽ các biểu đồ kết quả------------------------------------------------------->
    
    @app.route('/additional-chart-data', methods=['GET'])
    def additional_chart_data():
        # Kiểm tra nếu file predicted_causes.csv tồn tại
        if not check_file_exists(predicted_causes_file):
            return jsonify({'error': 'Predicted causes file not found.'}), 400
    
        # Tải dữ liệu từ file predicted_causes.csv
        predicted_data = pd.read_csv(predicted_causes_file)
    
        # Chuẩn bị dữ liệu để vẽ biểu đồ cho từng cột
        chart_data = {
            'years': predicted_data['year'].tolist(),
            'greenhouse gas emissions person': predicted_data['greenhouse gas emissions person'].replace({np.nan: None}).tolist(),
            'methane emissions person': predicted_data['methane emissions person'].replace({np.nan: None}).tolist(),
            'nitrous oxide emissions person': predicted_data['nitrous oxide emissions person'].replace({np.nan: None}).tolist(),
            'Annual CO2 emission': predicted_data['Annual CO2 emission'].replace({np.nan: None}).tolist(),
            'Annual greenhouse gas emissions': predicted_data['Annual greenhouse gas emissions'].replace({np.nan: None}).tolist(),
            'Annual nitrous emissions': predicted_data['Annual nitrous emissions'].replace({np.nan: None}).tolist() if 'Annual nitrous emissions' in predicted_data.columns else []
        }
    
        return jsonify(chart_data)

#-------------------------------------------------------------------------------------------------------------------->




