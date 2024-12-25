import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from utils import predicted_causes_file, load_model, save_model
import joblib

#===================================Hàm này để huấn luyện mô hình==========================================================>


 
def train_and_predict_with_predicted_causes(csv_file,predicted_causes_file, target_year):
    # Đọc dữ liệu từ file CSV
    train_data = pd.read_csv(csv_file)
    predicted_data = pd.read_csv(predicted_causes_file)

    # Xác định rõ ràng các biến đặc trưng (input features) và biến kết quả (output)
    feature_columns = ['greenhouse gas emissions person', 'methane emissions person', 'nitrous oxide emissions person', 'Annual CO2 emission', 'Annual greenhouse gas emissions','Annual nitrous emissions']  # Biến đặc trưng
    target_columns = ['Global average temperature anomaly','Sea surface temperature anomaly (relative to 1961-90 average)','Maximum Antarctic sea ice extent','Maximum Arctic sea ice extent','Global sea level as an average of Church and White (2011) and UHSLC data']  # Biến kết quả (có thể mở rộng nếu cần nhiều biến kết quả)

    # Kiểm tra nếu các cột mục tiêu không tồn tại thì thêm các cột với giá trị None
    for target_col in target_columns:
        if target_col not in train_data.columns:
            train_data[target_col] = None

    start_year = 2020
    target_year = None
    # Huấn luyện mô hình từ dữ liệu hiện có và dự đoán cho các năm từ start_year đến target_year
    
    if target_year is None:
        target_year = start_year

    for year in range(start_year, target_year + 1):
        # Lọc dữ liệu của năm hiện tại
        current_year_data = train_data[train_data['year'] == year][feature_columns].dropna().astype(float)
        
        if not current_year_data.empty:
            # Huấn luyện mô hình với toàn bộ dữ liệu đã có
            X_train = train_data[feature_columns].dropna().astype(float)
            y_train = train_data[target_columns].dropna().astype(float)

            train_data.fillna(0, inplace=True)

            common_index = X_train.index.intersection(y_train.index)
            X_train = X_train.loc[common_index]
            y_train = y_train.loc[common_index]

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            # Dự đoán cho từng cột kết quả
            for target_col in target_columns:
                predicted_value = model.predict(current_year_data)[0]
                mask = predicted_data['year'] == year
                predicted_data.loc[mask, target_col] = predicted_value[:len(predicted_data[mask])]


    # Lưu lại dữ liệu đã được dự đoán vào CSV
    predicted_data.to_csv(predicted_causes_file, index=False)


    # Lưu mô hình đã huấn luyện
    save_model(model, 'climate_change_impact_model.pkl')
    print(f"Mô hình đã được huấn luyện và lưu thành công với các biến: {target_columns}")

    return predicted_data



#=========================================================================================================================>



#------------------------------------Hàm trả về dữ liệu để vẽ biểu đồ----------------------------------------------------->
def get_visualization_data(climate_data):
    data = {
        'years': climate_data['year'].tolist(),
        'greenhouse gas emissions person': climate_data['greenhouse gas emissions person'].tolist() if 'greenhouse gas emissions person' in climate_data.columns else [],
        'methane emissions person': climate_data['methane emissions person'].tolist(),
        'nitrous oxide emissions person': climate_data['nitrous oxide emissions person'].tolist(),
        'Annual CO2 emission': climate_data['Annual CO2 emission'].tolist(),
        'Annual greenhouse gas emissions': climate_data['Annual greenhouse gas emissions'].tolist(),
        'Annual nitrous emissions': climate_data['Annual nitrous emissions'].tolist()
    }
    return data

#------------------------------------------------------------------------------------------------------------------------->