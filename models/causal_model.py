import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from utils import predicted_causes_file

#=======================Hàm dự đoán các biến nguyên nhân và tạo file predicted_causes.csv với năm được chọn==========================

def predict_causes(csv_file_path, target_year):
    climate_data = pd.read_csv(csv_file_path)
    cause_columns = ['co2_emissions', 'forest_cover', 'global_temperature','polar_ice_melt','climate_impact']  # Các biến nguyên nhân
    feature_columns = ['year']

    last_year = climate_data['year'].max()
    predicted_data = climate_data.copy()

    # Dự đoán dữ liệu từng năm từ năm cuối trong dữ liệu đến năm người dùng nhập
    for year in range(last_year + 1, target_year + 1):
        future_years = pd.DataFrame({'year': [year]})
        predictions = {}

        # Train Model
        for column in cause_columns:
            X = predicted_data[feature_columns]
            y = predicted_data[column]
            model = LinearRegression()
            model.fit(X, y)

            # Dự đoán
            future_prediction = model.predict(future_years)
            predictions[column] = future_prediction[0]

        # update dữ liệu dự đoán
        new_row = {'year': year}
        new_row.update(predictions)
        predicted_data = pd.concat([predicted_data, pd.DataFrame([new_row])], ignore_index=True)

    # Lưu dữ liệu dự đoán vào file predicted_causes.csv
    predicted_data.to_csv(predicted_causes_file, index=False)
    print(f"Predicted cause variables from {last_year} to {target_year} saved to '{predicted_causes_file}'")

#====================================================================================================================================