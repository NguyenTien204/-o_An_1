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
    return os.path.isfile(filepath)

def save_model(model, filename='climate_change_impact_model.pkl'):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")



#------------------------------------------------------------------------------------------------------------------------------------>