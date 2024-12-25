// Tạo biểu đồ như cũ, chỉ cần giữ nguyên các hàm createChart đã có
function createChart(canvasId, label, data, labels) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Year' } },
                y: { title: { display: true, text: label } }
            }
        }
    });
}

// Tải dữ liệu từ server như cũ và hiển thị trên các biểu đồ
fetch('/chart-data')
    .then(response => response.json())
    .then(data => {
        console.log('Dữ liệu biểu đồ:', data);
        
        // Hiển thị biểu đồ đầu tiên cho tab đang mở mặc định
        createChart('temperatureChart', 'Global Temperature (°C)', data.global_temperature, data.years);
        
        // Khi chuyển tab, khởi tạo lại các biểu đồ tương ứng
        document.getElementById('sea-level-tab').addEventListener('shown.bs.tab', function () {
            createChart('seaLevelChart', 'Sea Level Rise (m)', data.sea_level_rise, data.years);
        });

        document.getElementById('co2-tab').addEventListener('shown.bs.tab', function () {
            createChart('co2Chart', 'CO2 Emissions (Gt)', data.co2_emissions, data.years);
        });

        // Thêm sự kiện cho các tab khác (nếu có)
        document.getElementById('polar-ice-tab').addEventListener('shown.bs.tab', function () {
            createChart('polarIceChart', 'Băng tan hai cực', data.polar_ice_melt, data.years);
        });

        document.getElementById('forest-cover-tab').addEventListener('shown.bs.tab', function () {
            createChart('forestCoverChart', 'Diện tích rừng', data.forest_cover, data.years);
        });

        document.getElementById('climate-impact-tab').addEventListener('shown.bs.tab', function () {
            createChart('climateImpactChart', 'Tác động khí hậu', data.climate_impact, data.years);
        });
        
        // Thêm sự kiện cho các tab bổ sung
        document.getElementById('new-tab-1').addEventListener('shown.bs.tab', function () {
            fetch('/additional-chart-data')
                .then(response => response.json())
                .then(predictedData => {
                    createChart('predictedCausesChart', 'Dự đoán Nhiệt độ toàn cầu', predictedData.global_temperature, predictedData.years);
                })
                .catch(error => console.error('Lỗi khi tải dữ liệu dự đoán:', error));
        });

        document.getElementById('new-tab-2').addEventListener('shown.bs.tab', function () {
            fetch('/additional-chart-data')
                .then(response => response.json())
                .then(predictedData => {
                    createChart('seaLevelChartPrediction', 'Dự đoán Mực nước biển', predictedData.sea_level_rise, predictedData.years);
                })
                .catch(error => console.error('Lỗi khi tải dữ liệu dự đoán:', error));
        });

        document.getElementById('new-tab-3').addEventListener('shown.bs.tab', function () {
            fetch('/additional-chart-data')
                .then(response => response.json())
                .then(predictedData => {
                    createChart('co2EmissionsChartPrediction', 'Dự đoán Khí thải CO2', predictedData.co2_emissions, predictedData.years);
                })
                .catch(error => console.error('Lỗi khi tải dữ liệu dự đoán:', error));
        });

        document.getElementById('new-tab-4').addEventListener('shown.bs.tab', function () {
            fetch('/additional-chart-data')
                .then(response => response.json())
                .then(predictedData => {
                    createChart('polarIceMeltChartPrediction', 'Dự đoán Băng tan hai cực', predictedData.polar_ice_melt, predictedData.years);
                })
                .catch(error => console.error('Lỗi khi tải dữ liệu dự đoán:', error));
        });

        document.getElementById('new-tab-5').addEventListener('shown.bs.tab', function () {
            fetch('/additional-chart-data')
                .then(response => response.json())
                .then(predictedData => {
                    createChart('forestCoverChartPrediction', 'Dự đoán Diện tích rừng', predictedData.forest_cover, predictedData.years);
                })
                .catch(error => console.error('Lỗi khi tải dữ liệu dự đoán:', error));
        });

        document.getElementById('new-tab-6').addEventListener('shown.bs.tab', function () {
            fetch('/additional-chart-data')
                .then(response => response.json())
                .then(predictedData => {
                    createChart('climateImpactChartPrediction', 'Dự đoán Tác động khí hậu', predictedData.climate_impact, predictedData.years);
                })
                .catch(error => console.error('Lỗi khi tải dữ liệu dự đoán:', error));
        });

        // Sự kiện cho nút dự đoán nguyên nhân
        document.getElementById('predictCausesBtn').addEventListener('click', function() {
            console.log('Predict button clicked'); // Kiểm tra xem sự kiện click có hoạt động
            const selectedYear = document.getElementById('yearSelect').value;
            const loadingElement = document.getElementById('loading');
            const predictionResult = document.getElementById('predictionResult');
            
            // Hiển thị thanh tải
            loadingElement.classList.remove('d-none');
            predictionResult.textContent = ''; // Xóa nội dung cũ
        
            fetch(`/train-causes?year=${selectedYear}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                // Ẩn thanh tải và hiển thị thông báo thành công
                loadingElement.classList.add('d-none');
                predictionResult.textContent = 'Dự đoán biến nguyên nhân thành công!';
                
                // Tự động ẩn thông báo sau 2 giây
                setTimeout(() => {
                    predictionResult.textContent = '';
                }, 2000);
            })
            .catch(error => {
                loadingElement.classList.add('d-none');
                console.error('Error:', error);
                predictionResult.textContent = 'Lỗi khi dự đoán biến nguyên nhân.';
            });
        });

        document.getElementById('trainModelWithPredictionsBtn').addEventListener('click', function() {
            const selectedYear = document.getElementById('yearSelect').value;
            fetch(`/train-predictions?year=${selectedYear}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('predictionResult').textContent = 'Model trained with predicted causes successfully';
                console.log('Prediction data received:', data);
            })
            .catch(error => console.error('Error training model with predictions:', error));
        });
        
    })
    .catch(error => console.error('Lỗi khi tải dữ liệu:', error));

// Hàm để cập nhật hiển thị năm khi thanh chọn thay đổi
function updateYearDisplay(year) {
    document.getElementById('selectedYear').textContent = year;
}