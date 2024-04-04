const cachedWeatherData = localStorage.getItem('weatherData');

if (cachedWeatherData) {
    displayWeatherData(JSON.parse(cachedWeatherData));
} else {
    fetchWeatherData();
}

function fetchWeatherData() {
    fetch('https://weather-data-m61g.onrender.com/weather')
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                // Save weather data to localStorage
                localStorage.setItem('weatherData', JSON.stringify(data));
                // Display weather data
                displayWeatherData(data);
            } else {
                document.getElementById("weatherInfo").innerHTML = "<p>No weather data available.</p>";
            }
        })
        .catch(err => {
            console.error("Failed to fetch weather data from server:", err);
            document.getElementById("weatherInfo").innerHTML = "<p class='alert alert-danger'>Failed to load weather data from server.</p>";
        });
}

function displayWeatherData(data) {
    const firstItem = data[0];
    const humidity = firstItem.humidity;
    const weatherInfo = `
        <div class="card">
            <div class="card-body">
                <p class="card-text" style="text-align: center; padding: 10px;"><strong>Humidity:</strong> ${humidity}%</p>
            </div>
        </div>
    `;
    document.getElementById("weatherInfo").innerHTML = weatherInfo;
}
