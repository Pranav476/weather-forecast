document.addEventListener('DOMContentLoaded', () => {
    const cityInput = document.getElementById('city-input');
    const searchBtn = document.getElementById('search-btn');
    
    const cityNameEl = document.getElementById('city-name');
    const conditionEl = document.getElementById('condition');
    const tempEl = document.getElementById('temperature');
    const humidityEl = document.getElementById('humidity');
    const windEl = document.getElementById('wind-speed');

    let weatherChart;
    let updateInterval;

    const ctx = document.getElementById('weatherChart').getContext('2d');

    function createOrUpdateChart(labels, tempData, humidityData, windData) {
        if (weatherChart) {
            weatherChart.data.labels = labels;
            weatherChart.data.datasets[0].data = tempData;
            weatherChart.data.datasets[1].data = humidityData;
            weatherChart.data.datasets[2].data = windData;
            weatherChart.update();
        } else {
            weatherChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Temperature (°C)',
                            data: tempData,
                            borderColor: 'rgba(255, 99, 132, 1)',
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            yAxisID: 'y',
                        },
                        {
                            label: 'Humidity (%)',
                            data: humidityData,
                            borderColor: 'rgba(54, 162, 235, 1)',
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            yAxisID: 'y1',
                        },
                        {
                            label: 'Wind Speed (m/s)',
                            data: windData,
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            yAxisID: 'y',
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            type: 'linear',
                            display: true,
                            position: 'left',
                            title: { display: true, text: 'Temp (°C) / Wind (m/s)' }
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            title: { display: true, text: 'Humidity (%)' },
                            grid: { drawOnChartArea: false }
                        }
                    }
                }
            });
        }
    }

    async function fetchAndUpdateWeather() {
        const city = cityInput.value.trim();
        if (!city) {
            alert('Please enter a city name.');
            return;
        }

        try {
            const response = await fetch(`/weather/${city}`);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'City not found');
            }
            const data = await response.json();

            // Update text elements
            cityNameEl.textContent = data.city;
            conditionEl.textContent = data.condition;
            tempEl.textContent = `${data.temperature.toFixed(1)} °C`;
            humidityEl.textContent = `${data.humidity.toFixed(1)} %`;
            windEl.textContent = `${data.windSpeed.toFixed(1)} m/s`;

            // Update chart
            const now = new Date().toLocaleTimeString();
            const labels = weatherChart ? [...weatherChart.data.labels, now] : [now];
            const tempData = weatherChart ? [...weatherChart.data.datasets[0].data, data.temperature] : [data.temperature];
            const humidityData = weatherChart ? [...weatherChart.data.datasets[1].data, data.humidity] : [data.humidity];
            const windData = weatherChart ? [...weatherChart.data.datasets[2].data, data.windSpeed] : [data.windSpeed];

            // Keep only the last 10 data points
            if (labels.length > 10) {
                labels.shift();
                tempData.shift();
                humidityData.shift();
                windData.shift();
            }

            createOrUpdateChart(labels, tempData, humidityData, windData);

        } catch (error) {
            alert(error.message);
            clearInterval(updateInterval);
        }
    }

    function startLiveUpdates() {
        // Clear previous chart and interval
        if (weatherChart) {
            weatherChart.destroy();
            weatherChart = null;
        }
        if (updateInterval) {
            clearInterval(updateInterval);
        }
        
        fetchAndUpdateWeather(); // Fetch immediately
        updateInterval = setInterval(fetchAndUpdateWeather, 15000); // Then every 15 seconds
    }

    searchBtn.addEventListener('click', startLiveUpdates);
    cityInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            startLiveUpdates();
        }
    });

    // Initial load
    startLiveUpdates();
});