import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from utils import save_model, load_model
import joblib

#---------------------------------------------Load Model đã được huấn luyện-------------------------------------------------->

    
#--------------------------------------------Kế thừa và sử dụng model đã train----------------------------------------------->

#def train_and_predict_with_predicted_causes(csv_file):
#    predicted_data = pd.read_csv(csv_file)
#
#    if 'sea_level_rise' not in predicted_data.columns:
#        predicted_data['sea_level_rise'] = None
#
#    #Thêm các if nếu muốn thêm các biến đích
#    #if 'new_var' not in predicted_data.columns:
#        #predicted_data['new_var'] = None
#    #....
#
#
#    # Tải mô hình đã huấn luyện
#    model = load_model('climate_change_impact_model.pkl')
#
#    if model is None:
#        return None 
#def train_and_predict_with_predicted_causes(csv_file):
#    predicted_data = pd.read_csv(csv_file)
#
#    if 'sea_level_rise' not in predicted_data.columns:
#        predicted_data['sea_level_rise'] = None
#
#    # Tải mô hình đã huấn luyện
#    model = load_model('climate_change_impact_model.pkl')
#
#    if model is None:
#        return None
#
#    # Biến đầu vào mà mô hình đã huấn luyện
#    feature_columns = ['greenhouse gas emissions person', 'methane emissions person', 'nitrous oxide emissions person', 'Annual CO2 emission', 'Annual greenhouse gas emissions','Annual nitrous emissions']
#
#    # Lặp qua từng hàng và cập nhật các biến nguyên nhân dựa trên dự đoán của năm trước
#    for index, row in predicted_data.iterrows():
#        if pd.isnull(row['sea_level_rise']):  # Chỉ dự đoán nếu chưa có giá trị
#            # Lấy các biến đầu vào cho năm hiện tại và in ra để kiểm tra
#            features = pd.DataFrame([row[feature_columns]], columns=feature_columns)
#            print(f"Year: {row['year']}, Features: {features}")  # In giá trị của các biến đầu vào để kiểm tra
#
#            # Dự đoán giá trị sea_level_rise với các biến đầu vào của năm hiện tại
#            predicted_value = model.predict(features)[0]
#
#            # Cập nhật giá trị dự đoán cho năm hiện tại
#            predicted_data.at[index, 'sea_level_rise'] = predicted_value
#
#    # Lưu lại dữ liệu đã được dự đoán
#    predicted_data.to_csv(csv_file, index=False)
#    return predicted_data

#--------------------------------------------------------------------------------------------------------------------------->

#Lưu ý: Hàm này không tồn tại song song với hàm phía trên
#===================================Hàm này để huấn luyện mô hình==========================================================>


 
def train_and_predict_with_predicted_causes(csv_file,predicted_file, target_year):
    # Đọc dữ liệu từ file CSV
    train_data = pd.read_csv(csv_file)
    predicted_data = pd.read_csv(predicted_file)

    # Xác định rõ ràng các biến đặc trưng (input features) và biến kết quả (output)
    feature_columns = ['greenhouse gas emissions person', 'methane emissions person', 'nitrous oxide emissions person', 'Annual CO2 emission', 'Annual greenhouse gas emissions','Annual nitrous emissions']  # Biến đặc trưng
    target_columns = ['Global average temperature anomaly','Sea surface temperature anomaly (relative to 1961-90 average)','Maximum Antarctic sea ice extent','Maximum Arctic sea ice extent','Global sea level as an average of Church and White (2011) and UHSLC data']  # Biến kết quả (có thể mở rộng nếu cần nhiều biến kết quả)

    # Kiểm tra nếu các cột mục tiêu không tồn tại thì thêm các cột với giá trị None
    for target_col in target_columns:
        if target_col not in train_data.columns:
            train_data[target_col] = None

    start_year = 2020
    # Huấn luyện mô hình từ dữ liệu hiện có và dự đoán cho các năm từ start_year đến target_year
    for year in range(start_year, target_year + 1):
        # Lọc dữ liệu của năm hiện tại
        current_year_data = train_data[train_data['year'] == year][feature_columns].dropna().astype(float)

        if not current_year_data.empty:
            # Huấn luyện mô hình với toàn bộ dữ liệu đã có
            X_train = train_data[feature_columns].dropna().astype(float)
            y_train = train_data[target_columns].dropna().astype(float)

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            # Dự đoán cho từng cột kết quả
            #for target_col in target_columns:
            #    predicted_value = model.predict(current_year_data)[0]
            #    predicted_data.loc[predicted_data['year'] == year, target_col] = predicted_value

    # Lưu lại dữ liệu đã được dự đoán vào CSV
    #predicted_data.to_csv(csv_file, index=False)

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