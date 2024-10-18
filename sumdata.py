import pandas as pd
import numpy as np

# Tạo dữ liệu giả
years = list(range(1900, 2021))
data = {
    'year': years,
    'global_temperature': np.random.uniform(13.0, 15.0, len(years)),
    'forest_cover': np.random.uniform(30.0, 50.0, len(years)),
    'co2_emissions': np.random.uniform(300, 500, len(years)),
    'polar_ice_melt': np.random.uniform(0.0, 2.0, len(years)),
    'climate_impact': np.random.uniform(0.0, 5.0, len(years)),
    'sea_level_rise': np.random.uniform(0.0,10.0, len(years))
}

# Tạo DataFrame
df = pd.DataFrame(data)

# Lưu DataFrame thành file CSV
df.to_csv('predicted_causes_generated.csv', index=False)
