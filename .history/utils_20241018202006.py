#----------------------------------File này chứa các hàm nhỏ dùng chung cho nhiều file----------------------------------------------->
import joblib
import os

# Đường dẫn tuyệt đối đến file data gốc
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
data_dir = os.path.join(BASE_DIR, 'data') 
predicted_causes_file = os.path.join(data_dir, 'predicted_causes.csv')  
print(BASE_DIR)
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Hàm kiểm tra file có tồn tại không
def check_file_exists(filepath):
    return os.path.isfile(filepath)\

# Hàm lưu model 
def save_model(model, filename='climate_change_impact_model.pkl'):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")

#Hàm load model
def load_model(filename):
    try:
        model = joblib.load(filename)
        print(f"Model loaded from {filename}")
        return model
    except FileNotFoundError:
        print(f"Model file {filename} not found. Please train the model first.")
        return None

#------------------------------------------------------------------------------------------------------------------------------------>