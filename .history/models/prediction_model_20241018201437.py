import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from utils import save_model
import joblib

#---------------------------------------------Load Model đã được huấn luyện-------------------------------------------------->

def load_model(filename='climate_change_impact_model.pkl'):
    try:
        model = joblib.load(filename)
        print(f"Model loaded from {filename}")
        return model
    except FileNotFoundError:
        print(f"Model file {filename} not found. Please train the model first.")
        return None
    
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
#    model = load_model()
#
#    if model is None:
#        return None 
#    variables_to_predict = ['sea_level_rise'] #thêm các biến đích vào đây  
#    # Thực hiện dự đoán sea_level_rise với các biến nguyên nhân được dự đoán
#    for index, row in predicted_data.iterrows():
#        for variable in variables_to_predict:
#            if pd.isnull(row[variable]):  # Chỉ dự đoán nếu biến chưa có giá trị
#                # Sử dụng các biến nguyên nhân để dự đoán
#                features = row[['global_temperature', 'forest_cover', 'co2_emissions']].values.reshape(1, -1)
#                predicted_value = model.predict(features)[0]
#                predicted_data.at[index, variable] = predicted_value
#
#
#    # Lưu lại dữ liệu đã được dự đoán
#    predicted_data.to_csv(csv_file, index=False)
#    return predicted_data

#--------------------------------------------------------------------------------------------------------------------------->

#Lưu ý: Hàm này không tồn tại song song với hàm phía trên
#===================================Hàm này để huấn luyện mô hình==========================================================>


def train_and_predict_with_predicted_causes(csv_file, target_year):
    predicted_data = pd.read_csv(csv_file)

    if 'sea_level_rise' not in predicted_data.columns:
        predicted_data['sea_level_rise'] = None

    start_year = 2020
    for year in range(start_year, target_year + 1):
        current_year_data = predicted_data[predicted_data['year'] == year][['global_temperature', 'forest_cover', 'co2_emissions']].astype(float)
        
        if not current_year_data.empty:
            X_train = predicted_data[['global_temperature', 'forest_cover', 'co2_emissions']].dropna().astype(float)
            y_train = predicted_data['sea_level_rise'].dropna().astype(float)

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            predicted_sea_level_rise = model.predict(current_year_data)[0]

            predicted_data.loc[predicted_data['year'] == year, 'sea_level_rise'] = predicted_sea_level_rise
    
    predicted_data.to_csv(csv_file, index=False)

    save_model(model, 'climate_change_impact_model.pkl')  # Lưu model sau khi huấn luyện
    return predicted_data

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