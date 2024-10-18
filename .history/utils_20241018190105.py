#----------------------------------File này chứa các hàm nhỏ dùng chung cho nhiều file----------------------------------------------->

import os

# Đường dẫn tuyệt đối đến file data gốc
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
data_dir = os.path.join(BASE_DIR, 'data') 
predicted_causes_file = os.path.join(data_dir, 'predicted_causes.csv')  
climate_data_file = os.path.join(data_dir, 'climate_data.csv')
print(BASE_DIR)
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Hàm kiểm tra file có tồn tại không
def check_file_exists(filepath):
    return os.path.isfile(filepath)



#------------------------------------------------------------------------------------------------------------------------------------>