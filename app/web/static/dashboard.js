function getColorForPercentage(pct) {
    let hue;
    if (pct < 0.5) {
        hue = 120 - (pct / 0.5) * 60;
    } else {
        hue = 60 - ((pct - 0.5) / 0.5) * 60;
    }
    hue = Math.max(0, Math.min(120, hue));
    return `hsl(${hue}, 85%, 45%)`;
}

function getProgressGradient(pct) {
    const startColor = "hsl(120, 85%, 40%)";
    const midColor = "hsl(60, 85%, 45%)";
    const endColor = getColorForPercentage(pct);
    
    if (pct <= 0.5) {
        return `linear-gradient(to right, ${startColor}, ${endColor})`;
    } else {
        const midPercent = (0.5 / pct) * 100;
        return `linear-gradient(to right, ${startColor} 0%, ${midColor} ${midPercent}%, ${endColor} 100%)`;
    }
}

// Config references:
const config = window.dashboardConfig || {
    refreshIntervalSeconds: 300,
    limitText: "Limit",
    loadingText: "Loading..."
};

let timeLeft = config.refreshIntervalSeconds;

async function fetchTraffic() {
    try {
        const response = await fetch('/traffic');
        const data = await response.json();
        
        // Day
        document.getElementById('day-text').innerText = data.day_gb + ' GB';
        document.getElementById('day-limit').innerText = data.day_limit + ' GB ' + config.limitText;
        const dayBar = document.getElementById('day-progress-bar');
        const dayPercent = data.day_gb / (data.day_limit || 1);
        dayBar.style.width = Math.min(100, dayPercent * 100) + '%';
        dayBar.style.background = getProgressGradient(dayPercent);

        // Month
        document.getElementById('month-text').innerText = data.month_gb + ' GB';
        document.getElementById('month-limit').innerText = data.month_limit + ' GB ' + config.limitText;
        const monthBar = document.getElementById('month-progress-bar');
        const monthPercent = data.month_gb / (data.month_limit || 1);
        monthBar.style.width = Math.min(100, monthPercent * 100) + '%';
        monthBar.style.background = getProgressGradient(monthPercent);
    } catch (error) {
        console.error("Error fetching traffic:", error);
    }
}

function updateTimerDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    const minutesStr = String(minutes).padStart(2, '0');
    const secondsStr = String(seconds).padStart(2, '0');
    document.getElementById('timer').innerText = `${minutesStr}:${secondsStr}`;
}

function resetTimer() {
    timeLeft = config.refreshIntervalSeconds;
    updateTimerDisplay();
}

// Countdown tick every second
setInterval(() => {
    timeLeft--;
    if (timeLeft < 0) {
        fetchTraffic();
        resetTimer();
    } else {
        updateTimerDisplay();
    }
}, 1000);

// Manual refresh button
document.getElementById('btn-refresh').addEventListener('click', () => {
    fetchTraffic();
    resetTimer();
});

// Theme switching handler
const themeSelect = document.getElementById('theme-select');
function applyTheme(theme) {
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
    localStorage.setItem('theme', theme);
    themeSelect.value = theme;
}

// Set initial selector state
themeSelect.value = localStorage.getItem('theme') || 'system';
themeSelect.addEventListener('change', (e) => {
    applyTheme(e.target.value);
});

// Fetch immediately and start timer
fetchTraffic();
updateTimerDisplay();
