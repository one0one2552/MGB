// WebSocket-Verbindung
const socket = io();

// Globale Variablen
let tempChart, humidityChart, co2Chart;
const maxDataPoints = 50;

// Initialisierung beim Laden der Seite
document.addEventListener('DOMContentLoaded', function() {
    console.log('Seite geladen, initialisiere...');
    initCharts();
    loadInitialData();
    
    // Regelmäßige Aktualisierung
    setInterval(updateStatus, 5000);
});

// WebSocket Event-Handler
socket.on('connect', function() {
    console.log('WebSocket verbunden');
    updateConnectionStatus(true);
});

socket.on('disconnect', function() {
    console.log('WebSocket getrennt');
    updateConnectionStatus(false);
});

socket.on('connection_response', function(data) {
    console.log('Verbindungsbestätigung:', data);
});

socket.on('sensor_update', function(data) {
    console.log('Sensor-Update empfangen:', data);
    updateSensorDisplay(data);
});

socket.on('alarm', function(data) {
    console.log('Alarm empfangen:', data);
    addAlarm(data);
});

// Verbindungsstatus aktualisieren
function updateConnectionStatus(connected) {
    const statusDot = document.getElementById('connection-status');
    const statusText = document.getElementById('connection-text');
    
    if (connected) {
        statusDot.classList.remove('offline');
        statusDot.classList.add('online');
        statusText.textContent = 'Verbunden';
    } else {
        statusDot.classList.remove('online');
        statusDot.classList.add('offline');
        statusText.textContent = 'Getrennt';
    }
}

// Initiale Daten laden
async function loadInitialData() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        updateDisplay(data);
    } catch (error) {
        console.error('Fehler beim Laden der Daten:', error);
    }
}

// Status aktualisieren
async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        updateDisplay(data);
        updateLastUpdateTime();
    } catch (error) {
        console.error('Fehler beim Aktualisieren:', error);
    }
}

// Anzeige aktualisieren
function updateDisplay(data) {
    // Sensoren aktualisieren
    if (data.sensors) {
        updateSensor('temp', data.sensors.temperature);
        updateSensor('humidity', data.sensors.humidity);
        updateSensor('co2', data.sensors.co2);
    }
    
    // Aktoren aktualisieren
    if (data.actuators) {
        updateActuator('pump', data.actuators.pump);
        updateActuator('heater', data.actuators.heater);
        updateActuator('fan', data.actuators.fan);
    }
    
    // Alarme aktualisieren
    if (data.alarms && data.alarms.length > 0) {
        displayAlarms(data.alarms);
    }
}

// Einzelnen Sensor aktualisieren
function updateSensor(sensorId, sensorData) {
    const valueElement = document.getElementById(`${sensorId}-value`);
    const targetElement = document.getElementById(`${sensorId}-target`);
    const statusElement = document.getElementById(`${sensorId}-status`);
    
    if (valueElement && sensorData) {
        valueElement.textContent = sensorData.value.toFixed(1);
        targetElement.textContent = sensorData.target.toFixed(1);
        
        // Status-Klasse setzen
        statusElement.className = `sensor-status ${sensorData.status}`;
        statusElement.textContent = getStatusText(sensorData.status);
        
        // Diagramm aktualisieren
        updateChart(sensorId, sensorData.value);
    }
}

// Einzelnen Aktor aktualisieren
function updateActuator(actuatorId, actuatorData) {
    const statusElement = document.getElementById(`${actuatorId}-status`);
    
    if (statusElement && actuatorData) {
        const isActive = actuatorData.active;
        const i18n = window.i18n;
        const statusText = isActive ? 
            (i18n ? i18n.t('status_active') : 'Aktiv') : 
            (i18n ? i18n.t('status_inactive') : 'Inaktiv');
        
        statusElement.className = `actuator-status ${isActive ? 'active' : 'inactive'}`;
        statusElement.innerHTML = `
            <span class="status-indicator">●</span>
            <span>${statusText}</span>
        `;
        
        // Lüfter-Geschwindigkeit anzeigen
        if (actuatorId === 'fan' && actuatorData.speed !== undefined) {
            const speedElement = document.getElementById('fan-speed');
            if (speedElement) {
                speedElement.querySelector('span').textContent = actuatorData.speed;
            }
        }
    }
}

// Status-Text mit i18n
function getStatusText(status) {
    const i18n = window.i18n;
    const statusKeys = {
        'ok': 'status_ok',
        'warning': 'status_warning',
        'critical': 'status_critical'
    };
    return i18n ? i18n.t(statusKeys[status] || 'status_ok') : status;
}

// Aktor steuern
async function controlActuator(actuatorName, action) {
    try {
        const response = await fetch(`/api/actuator/${actuatorName}/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            console.log(`${actuatorName} ${action} erfolgreich`);
            // Status sofort aktualisieren
            updateStatus();
        } else {
            console.error('Fehler beim Steuern:', data.message);
            alert('Fehler: ' + data.message);
        }
    } catch (error) {
        console.error('Fehler beim Steuern des Aktors:', error);
        alert('Verbindungsfehler');
    }
}

// Diagramme initialisieren
function initCharts() {
    const chartConfig = {
        type: 'line',
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Zeit'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Wert'
                    }
                }
            }
        }
    };
    
    // Temperatur-Diagramm
    const tempCtx = document.getElementById('tempChart').getContext('2d');
    tempChart = new Chart(tempCtx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'Temperatur (°C)',
                data: [],
                borderColor: 'rgb(220, 53, 69)',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                tension: 0.4
            }]
        }
    });
    
    // Luftfeuchtigkeits-Diagramm
    const humidityCtx = document.getElementById('humidityChart').getContext('2d');
    humidityChart = new Chart(humidityCtx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'Luftfeuchtigkeit (%)',
                data: [],
                borderColor: 'rgb(13, 110, 253)',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                tension: 0.4
            }]
        }
    });
    
    // CO2-Diagramm
    const co2Ctx = document.getElementById('co2Chart').getContext('2d');
    co2Chart = new Chart(co2Ctx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'CO2 (ppm)',
                data: [],
                borderColor: 'rgb(25, 135, 84)',
                backgroundColor: 'rgba(25, 135, 84, 0.1)',
                tension: 0.4
            }]
        }
    });
}

// Diagramm aktualisieren
function updateChart(sensorId, value) {
    const charts = {
        'temp': tempChart,
        'humidity': humidityChart,
        'co2': co2Chart
    };
    
    const chart = charts[sensorId];
    if (!chart) return;
    
    const now = new Date().toLocaleTimeString('de-DE');
    
    // Label hinzufügen
    chart.data.labels.push(now);
    chart.data.datasets[0].data.push(value);
    
    // Alte Datenpunkte entfernen
    if (chart.data.labels.length > maxDataPoints) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    
    chart.update('none'); // 'none' für bessere Performance
}

// Alarme anzeigen
function displayAlarms(alarms) {
    const alarmList = document.getElementById('alarm-list');
    
    if (alarms.length === 0) {
        alarmList.innerHTML = '<p class="no-alarms">Keine aktiven Alarme</p>';
        return;
    }
    
    alarmList.innerHTML = alarms.map(alarm => `
        <div class="alarm-item ${alarm.type}">
            <div>
                <strong>${alarm.title}</strong><br>
                <small>${alarm.message}</small>
            </div>
            <div>
                <small>${new Date(alarm.timestamp).toLocaleString('de-DE')}</small>
            </div>
        </div>
    `).join('');
}

// Alarm hinzufügen
function addAlarm(alarm) {
    const alarmList = document.getElementById('alarm-list');
    
    // "Keine Alarme"-Nachricht entfernen
    const noAlarms = alarmList.querySelector('.no-alarms');
    if (noAlarms) {
        noAlarms.remove();
    }
    
    // Neuen Alarm hinzufügen
    const alarmElement = document.createElement('div');
    alarmElement.className = `alarm-item ${alarm.type}`;
    alarmElement.innerHTML = `
        <div>
            <strong>${alarm.title}</strong><br>
            <small>${alarm.message}</small>
        </div>
        <div>
            <small>${new Date().toLocaleString('de-DE')}</small>
        </div>
    `;
    
    alarmList.insertBefore(alarmElement, alarmList.firstChild);
}

// Letzte Aktualisierungszeit
function updateLastUpdateTime() {
    const lastUpdate = document.getElementById('last-update');
    if (lastUpdate) {
        lastUpdate.textContent = new Date().toLocaleString('de-DE');
    }
}
