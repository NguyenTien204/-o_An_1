import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from utils import save_model, load_model
import joblib

#---------------------------------------------Load Model đã được huấn luyện-------------------------------------------------->

    
#--------------------------------------------Kế thừa và sử dụng model đã train----------------------------------------------->

def train_and_predict_with_predicted_causes(csv_file):
    predicted_data = pd.read_csv(csv_file)

    if 'sea_level_rise' not in predicted_data.columns:
        predicted_data['sea_level_rise'] = None

    #Thêm các if nếu muốn thêm các biến đích
    #if 'new_var' not in predicted_data.columns:
        #predicted_data['new_var'] = None
    #....


    # Tải mô hình đã huấn luyện
    model = load_model('climate_change_impact_model.pkl')

    if model is None:
        return None 
def train_and_predict_with_predicted_causes(csv_file):
    predicted_data = pd.read_csv(csv_file)

    if 'sea_level_rise' not in predicted_data.columns:
        predicted_data['sea_level_rise'] = None

    # Tải mô hình đã huấn luyện
    model = load_model('climate_change_impact_model.pkl')

    if model is None:
        return None

    # Biến đầu vào mà mô hình đã huấn luyện
    feature_columns = ['global_temperature', 'forest_cover', 'co2_emissions', 'climate_impact']

    # Lặp qua từng hàng và cập nhật các biến nguyên nhân dựa trên dự đoán của năm trước
    for index, row in predicted_data.iterrows():
        if pd.isnull(row['sea_level_rise']):  # Chỉ dự đoán nếu chưa có giá trị
            # Lấy các biến đầu vào cho năm hiện tại và in ra để kiểm tra
            features = pd.DataFrame([row[feature_columns]], columns=feature_columns)
            print(f"Year: {row['year']}, Features: {features}")  # In giá trị của các biến đầu vào để kiểm tra

            # Dự đoán giá trị sea_level_rise với các biến đầu vào của năm hiện tại
            predicted_value = model.predict(features)[0]

            # Cập nhật giá trị dự đoán cho năm hiện tại
            predicted_data.at[index, 'sea_level_rise'] = predicted_value

    # Lưu lại dữ liệu đã được dự đoán
    predicted_data.to_csv(csv_file, index=False)
    return predicted_data

#--------------------------------------------------------------------------------------------------------------------------->

#Lưu ý: Hàm này không tồn tại song song với hàm phía trên
#===================================Hàm này để huấn luyện mô hình==========================================================>


#def train_and_predict_with_predicted_causes(csv_file, target_year):
#    predicted_data = pd.read_csv(csv_file)
#
#    if 'sea_level_rise' not in predicted_data.columns:
#        predicted_data['sea_level_rise'] = None
#
#    start_year = 2020
#    # Huấn luyện mô hình với cả climate_impact
#    for year in range(start_year, target_year + 1):
#        current_year_data = predicted_data[predicted_data['year'] == year][['global_temperature', 'forest_cover', 'co2_emissions', 'climate_impact']].astype(float)
#        
#        if not current_year_data.empty:
#            # Huấn luyện mô hình với thêm climate_impact
#            X_train = predicted_data[['global_temperature', 'forest_cover', 'co2_emissions', 'climate_impact']].dropna().astype(float)
#            y_train = predicted_data['sea_level_rise'].dropna().astype(float)
#
#            model = RandomForestRegressor(n_estimators=100, random_state=42)
#            model.fit(X_train, y_train)
#
#            predicted_sea_level_rise = model.predict(current_year_data)[0]
#
#            predicted_data.loc[predicted_data['year'] == year, 'sea_level_rise'] = predicted_sea_level_rise
#    
#    predicted_data.to_csv(csv_file, index=False)
#
#    save_model(model, 'climate_change_impact_model.pkl')  # Lưu model sau khi huấn luyện
#    return predicted_data
#
#
#=========================================================================================================================>



#------------------------------------Hàm trả về dữ liệu để vẽ biểu đồ----------------------------------------------------->
def get_visualization_data(climate_data):
    data = {
        'years': climate_data['year'].tolist(),
        'sea_level_rise': climate_data['sea_level_rise'].tolist() if 'sea_level_rise' in climate_data.columns else [],
        'global_temperature': climate_data['global_temperature'].tolist(),
        'co2_emissions': climate_data['co2_emissions'].tolist(),
        'forest_cover': climate_data['forest_cover'].tolist(),
        'polar_ice_melt': climate_data['polar_ice_melt'].tolist(),
        'climate_impact': climate_data['climate_impact'].tolist()
    }
    return data

#------------------------------------------------------------------------------------------------------------------------->