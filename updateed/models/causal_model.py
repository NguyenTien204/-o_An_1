import pandas as pd
from sklearn.linear_model import LinearRegression
from joblib import Parallel, delayed
from utils import predicted_causes_file, load_model, save_model

# =======================Hàm dự đoán các biến nguyên nhân và tạo file predicted_causes.csv với năm được chọn==========================

def predict_single_year(year, model, predicted_data, feature_columns, cause_columns):
    future_years = pd.DataFrame({'year': [year]})
    predictions = {}
    
    for column in cause_columns:
        X = predicted_data[feature_columns]
        y = predicted_data[column]
        model.fit(X, y)
        future_prediction = model.predict(future_years)
        predictions[column] = future_prediction[0]
    
    return year, predictions

def predict_causes(csv_file_path, target_year):
    # Đọc dữ liệu từ file CSV
    climate_data = pd.read_csv(csv_file_path)
    
    # Các biến nguyên nhân cần dự đoán
    cause_columns = ['greenhouse gas emissions person', 'methane emissions person', 'nitrous oxide emissions person', 'Annual CO2 emission', 'Annual greenhouse gas emissions','Annual nitrous emissions']
    
    # Cột đặc trưng (đặc điểm dựa trên đó để dự đoán)
    feature_columns = ['year']

    # Lấy năm cuối cùng từ dữ liệu hiện tại
    last_year = climate_data['year'].max()

    # Sao chép dữ liệu hiện tại để dự đoán
    predicted_data = climate_data.copy()

    # Kiểm tra xem model đã được lưu chưa
    model = load_model('linear_regression_model.pkl')  # Thay thế bằng tên file lưu trữ model của bạn
    
    # Nếu model chưa tồn tại, huấn luyện lại và lưu model
    if model is None:
        print("No saved model found. Training a new model...")
        model = LinearRegression()
        # Huấn luyện mô hình với toàn bộ dữ liệu hiện tại để dự đoán cho tương lai
        X_train = predicted_data[feature_columns]
        y_train = predicted_data[cause_columns]
        model.fit(X_train, y_train)
        # Lưu mô hình đã huấn luyện
        save_model(model, 'linear_regression_model.pkl')
        print("New model trained and saved.")
    else:
        print("Loaded saved model.")

    # Sử dụng Parallel processing để dự đoán cho các năm từ last_year đến target_year
    results = Parallel(n_jobs=4)(delayed(predict_single_year)(
        year, model, predicted_data, feature_columns, cause_columns
    ) for year in range(last_year + 1, target_year + 1))

    # Thêm các dự đoán vào dữ liệu dự đoán
    for year, predictions in results:
        new_row = {'year': year}
        new_row.update(predictions)
        predicted_data = pd.concat([predicted_data, pd.DataFrame([new_row])], ignore_index=True)

    # Lưu dữ liệu dự đoán vào file predicted_causes.csv
    predicted_data.to_csv(predicted_causes_file, index=False)
    print(f"Predicted cause variables from {last_year} to {target_year} saved to '{predicted_causes_file}'")
