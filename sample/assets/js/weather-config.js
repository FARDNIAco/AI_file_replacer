// ==========================================
// Build: 2026-10-01 17:00:00
// Changes: 2 of 4
// Location: /test_nrz/assets/js/weather-config.js
// ==========================================

/**
 * تنظیمات ماژول اب و هوا
 * این فایل به‌صورت جداگانه قابل ویرایش است
 */
var WeatherConfig = {
    // آدرس API (Open-Meteo - رایگان و بدون API Key)
    apiUrl: 'https://api.open-meteo.com/v1/forecast',

    // پارامترهای درخواست
    params: {
        current: 'temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code',
        timezone: 'auto'
    },

    // واحدها
    temperatureUnit: 'celsius',
    windSpeedUnit: 'kmh',

    // متن‌ها
    texts: {
        loading: 'در حال دریافت اب و هوا...',
        error: 'اب و هوا در دسترس نیست',
        humidity: 'رطوبت',
        wind: 'باد'
    },

    // آیکون‌ها بر اساس کد وضعیت آب و هوا (WMO Weather Code)
    icons: {
        0:  '☀️',   // صاف
        1:  '🌤️',  // کمی ابری
        2:  '⛅',   // نیمه ابری
        3:  '☁️',   // ابری
        45: '🌫️',  // مه
        48: '🌫️',  // مه یخ‌زده
        51: '🌦️',  // نم‌نم باران
        53: '🌦️',
        55: '🌧️',
        61: '🌧️',  // باران
        63: '🌧️',
        65: '🌧️',
        71: '🌨️',  // برف
        73: '🌨️',
        75: '❄️',
        80: '🌦️',  // رگبار
        81: '🌧️',
        82: '⛈️',
        95: '⛈️',  // رعد و برق
        96: '⛈️',
        99: '⛈️'
    },

    // آیکون پیش‌فرض
    defaultIcon: '❓'
};