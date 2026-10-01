// ==========================================
// Build: 2026-10-01 17:00:00
// Changes: 3 of 4
// Location: /test_nrz/assets/js/weather.js
// ==========================================

/**
 * ماژول اب و هوا - دریافت و نمایش داده
 * وابسته به: weather-config.js
 */
var WeatherModule = (function () {
    'use strict';

    // ==========================================
    // 1. دریافت مختصات (Reverse Geocoding)
    // ==========================================
    function getCoordinates(element) {
        var lat = element.getAttribute('data-lat');
        var lon = element.getAttribute('data-lon');

        if (!lat || !lon) {
            return null;
        }

        return { lat: lat, lon: lon };
    }

    // ==========================================
    // 2. ساخت URL درخواست
    // ==========================================
    function buildApiUrl(coords) {
        var params = new URLSearchParams();
        params.append('latitude', coords.lat);
        params.append('longitude', coords.lon);

        // پارامترهای اصلی
        params.append('current', WeatherConfig.params.current);
        params.append('timezone', WeatherConfig.params.timezone);

        return WeatherConfig.apiUrl + '?' + params.toString();
    }

    // ==========================================
    // 3. دریافت داده از API
    // ==========================================
    function fetchWeather(coords) {
        var url = buildApiUrl(coords);

        return fetch(url)
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('HTTP error: ' + response.status);
                }
                return response.json();
            });
    }

    // ==========================================
    // 4. استخراج و نگاشت داده
    // ==========================================
    function parseWeatherData(data) {
        var current = data.current;

        return {
            temperature: Math.round(current.temperature_2m),
            humidity: current.relative_humidity_2m,
            windSpeed: Math.round(current.wind_speed_10m),
            weatherCode: current.weather_code,
            icon: WeatherConfig.icons[current.weather_code] || WeatherConfig.defaultIcon
        };
    }

    // ==========================================
    // 5. نمایش داده در DOM
    // ==========================================
    function renderWeather(element, weather) {
        var contentEl = document.getElementById('weather-content');
        var loaderEl = document.getElementById('weather-loader');

        // مخفی کردن لودر
        if (loaderEl) {
            loaderEl.hidden = true;
        }

        // نمایش محتوا
        if (contentEl) {
            contentEl.hidden = false;
        }

        // مقداردهی عناصر
        var iconEl = document.getElementById('weather-icon');
        var tempEl = document.getElementById('weather-temp');
        var cityEl = document.getElementById('weather-city');
        var humidityEl = document.getElementById('weather-humidity');
        var windEl = document.getElementById('weather-wind');

        if (iconEl) iconEl.textContent = weather.icon;
        if (tempEl) tempEl.textContent = weather.temperature + '°C';
        if (cityEl) cityEl.textContent = element.getAttribute('data-city') || '';
        if (humidityEl) humidityEl.textContent = weather.humidity;
        if (windEl) windEl.textContent = weather.windSpeed;
    }

    // ==========================================
    // 6. نمایش خطا
    // ==========================================
    function renderError(element) {
        var loaderEl = document.getElementById('weather-loader');
        var contentEl = document.getElementById('weather-content');

        if (loaderEl) {
            loaderEl.textContent = WeatherConfig.texts.error;
        }
        if (contentEl) {
            contentEl.hidden = true;
        }
    }

    // ==========================================
    // 7. راه‌اندازی اولیه
    // ==========================================
    function init() {
        var element = document.getElementById('weather-widget');

        if (!element) {
            return;
        }

        var coords = getCoordinates(element);

        if (!coords) {
            renderError(element);
            return;
        }

        fetchWeather(coords)
            .then(function (data) {
                var weather = parseWeatherData(data);
                renderWeather(element, weather);
            })
            .catch(function (error) {
                console.error('Weather Error:', error);
                renderError(element);
            });
    }

    // API عمومی
    return {
        init: init,
        fetchWeather: fetchWeather,
        parseWeatherData: parseWeatherData
    };
})();

// راه‌اندازی خودکار پس از لود DOM
document.addEventListener('DOMContentLoaded', function () {
    WeatherModule.init();
});