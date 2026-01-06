// Smart IoT Dashboard - Main JavaScript
// Handles all frontend interactions, API calls, and real-time updates

// CSRF Token Helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// ============================================
// SENSOR POPUP FUNCTIONALITY
// ============================================

let sensorUpdateInterval = null;
let currentSensorDevice = null;

function openSensorPopup(deviceId, sensorType, sensorName, currentValue, unit) {
    currentSensorDevice = deviceId;

    // Create modal HTML
    const modalHTML = `
        <div class="modal fade" id="sensorModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${sensorName}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-center">
                        <p class="text-muted mb-4">${getSensorDescription(sensorType)}</p>
                        
                        <!-- Speedometer Gauge -->
                        <div id="sensorGauge" style="height: 250px;"></div>
                        
                        <!-- Current Value Display -->
                        <div class="mt-3">
                            <h2 id="sensorValue" class="mb-0">${currentValue}</h2>
                            <p class="text-muted">${unit}</p>
                            <small class="text-muted">Last updated: <span id="lastUpdated">Just now</span></small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remove existing modal if any
    const existingModal = document.getElementById('sensorModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('sensorModal'));
    modal.show();

    // Initialize gauge
    initializeSensorGauge(sensorType, currentValue);

    // Start real-time updates
    startSensorUpdates(deviceId, sensorType);

    // Stop updates when modal is closed
    document.getElementById('sensorModal').addEventListener('hidden.bs.modal', function () {
        stopSensorUpdates();
        this.remove();
    });
}

function getSensorDescription(sensorType) {
    const descriptions = {
        'temperature': 'Monitors the ambient temperature of your hydroponic system',
        'humidity': 'Tracks the relative humidity levels in the environment',
        'ph': 'Measures the pH level of the nutrient solution',
        'ec': 'Electrical Conductivity - indicates nutrient concentration',
        'nitrogen': 'Nitrogen (N) content in the nutrient solution',
        'phosphorus': 'Phosphorus (P) content in the nutrient solution',
        'potassium': 'Potassium (K) content in the nutrient solution',
        'moisture': 'Soil/substrate moisture level',
        'light_hours': 'Daily light exposure duration'
    };
    return descriptions[sensorType] || 'Real-time sensor monitoring';
}

function initializeSensorGauge(sensorType, value) {
    const ranges = {
        'temperature': { min: 0, max: 50, zones: [[0, 15, '#3b82f6'], [15, 30, '#10b981'], [30, 50, '#ef4444']] },
        'humidity': { min: 0, max: 100, zones: [[0, 30, '#ef4444'], [30, 70, '#10b981'], [70, 100, '#3b82f6']] },
        'ph': { min: 0, max: 14, zones: [[0, 5.5, '#ef4444'], [5.5, 7.5, '#10b981'], [7.5, 14, '#f59e0b']] },
        'ec': { min: 0, max: 5, zones: [[0, 1, '#3b82f6'], [1, 3, '#10b981'], [3, 5, '#ef4444']] },
        'nitrogen': { min: 0, max: 300, zones: [[0, 100, '#ef4444'], [100, 200, '#10b981'], [200, 300, '#f59e0b']] },
        'phosphorus': { min: 0, max: 100, zones: [[0, 30, '#ef4444'], [30, 70, '#10b981'], [70, 100, '#f59e0b']] },
        'potassium': { min: 0, max: 400, zones: [[0, 150, '#ef4444'], [150, 250, '#10b981'], [250, 400, '#f59e0b']] },
        'moisture': { min: 0, max: 100, zones: [[0, 30, '#ef4444'], [30, 70, '#10b981'], [70, 100, '#3b82f6']] },
        'light_hours': { min: 0, max: 24, zones: [[0, 8, '#ef4444'], [8, 16, '#10b981'], [16, 24, '#f59e0b']] }
    };

    const range = ranges[sensorType] || { min: 0, max: 100, zones: [[0, 50, '#10b981'], [50, 100, '#ef4444']] };

    const options = {
        series: [parseFloat(value)],
        chart: {
            type: 'radialBar',
            height: 250,
            offsetY: -10
        },
        plotOptions: {
            radialBar: {
                startAngle: -135,
                endAngle: 135,
                dataLabels: {
                    name: {
                        fontSize: '16px',
                        color: undefined,
                        offsetY: 120
                    },
                    value: {
                        offsetY: 76,
                        fontSize: '22px',
                        color: undefined,
                        formatter: function (val) {
                            return val.toFixed(1);
                        }
                    }
                },
                track: {
                    background: '#e7e7e7',
                    strokeWidth: '97%',
                    margin: 5
                }
            }
        },
        fill: {
            type: 'gradient',
            gradient: {
                shade: 'dark',
                type: 'horizontal',
                shadeIntensity: 0.5,
                gradientToColors: ['#10b981'],
                inverseColors: true,
                opacityFrom: 1,
                opacityTo: 1,
                stops: [0, 100]
            }
        },
        stroke: {
            lineCap: 'round'
        },
        labels: ['Value']
    };

    const chart = new ApexCharts(document.querySelector("#sensorGauge"), options);
    chart.render();

    // Store chart instance for updates
    window.currentSensorChart = chart;
}

function startSensorUpdates(deviceId, sensorType) {
    // Update every second
    sensorUpdateInterval = setInterval(() => {
        fetchSensorData(deviceId, sensorType);
    }, 1000);
}

function stopSensorUpdates() {
    if (sensorUpdateInterval) {
        clearInterval(sensorUpdateInterval);
        sensorUpdateInterval = null;
    }
}

async function fetchSensorData(deviceId, sensorType) {
    try {
        const response = await fetch(`/hydroponics/api/latest/${deviceId}/`);
        const data = await response.json();

        if (data && data[sensorType] !== undefined) {
            const value = data[sensorType];

            // Update gauge
            if (window.currentSensorChart) {
                window.currentSensorChart.updateSeries([parseFloat(value)]);
            }

            // Update value display
            document.getElementById('sensorValue').textContent = parseFloat(value).toFixed(1);
            document.getElementById('lastUpdated').textContent = 'Just now';
        }
    } catch (error) {
        // console.error('Error fetching sensor data:', error);
    }
}

// ============================================
// ADD DEVICE FUNCTIONALITY
// ============================================

function showAddDeviceModal() {
    const modalHTML = `
        <div class="modal fade" id="addDeviceModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Add New Device</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="addDeviceForm">
                            <div class="mb-3">
                                <label for="deviceName" class="form-label">Device Name *</label>
                                <input type="text" class="form-control" id="deviceName" required placeholder="e.g., Greenhouse A">
                            </div>
                            <div class="mb-3">
                                <label for="deviceLatitude" class="form-label">Latitude</label>
                                <input type="number" step="0.000001" class="form-control" id="deviceLatitude" value="20.59" placeholder="20.59">
                            </div>
                            <div class="mb-3">
                                <label for="deviceLongitude" class="form-label">Longitude</label>
                                <input type="number" step="0.000001" class="form-control" id="deviceLongitude" value="78.96" placeholder="78.96">
                            </div>
                            <div id="addDeviceError" class="alert alert-danger d-none"></div>
                            <div id="addDeviceSuccess" class="alert alert-success d-none"></div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="submitAddDevice()">
                            <span id="addDeviceText">Add Device</span>
                            <span id="addDeviceSpinner" class="spinner-border spinner-border-sm d-none" role="status"></span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remove existing modal if any
    const existingModal = document.getElementById('addDeviceModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('addDeviceModal'));
    modal.show();
}

async function submitAddDevice() {
    const deviceName = document.getElementById('deviceName').value;
    const latitude = document.getElementById('deviceLatitude').value;
    const longitude = document.getElementById('deviceLongitude').value;

    const errorDiv = document.getElementById('addDeviceError');
    const successDiv = document.getElementById('addDeviceSuccess');
    const addText = document.getElementById('addDeviceText');
    const addSpinner = document.getElementById('addDeviceSpinner');

    // Hide previous messages
    errorDiv.classList.add('d-none');
    successDiv.classList.add('d-none');

    // Validate
    if (!deviceName) {
        errorDiv.textContent = 'Device name is required';
        errorDiv.classList.remove('d-none');
        return;
    }

    // Show loading
    addText.classList.add('d-none');
    addSpinner.classList.remove('d-none');

    try {
        const response = await fetch('/api/devices/add-device/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                device_name: deviceName,
                latitude: parseFloat(latitude),
                longitude: parseFloat(longitude)
            })
        });

        const data = await response.json();

        if (response.ok) {
            successDiv.textContent = 'Device added successfully!';
            successDiv.classList.remove('d-none');

            // Reload page after 1 second
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            errorDiv.textContent = data.error || 'Failed to add device';
            errorDiv.classList.remove('d-none');
            addText.classList.remove('d-none');
            addSpinner.classList.add('d-none');
        }
    } catch (error) {
        errorDiv.textContent = 'An error occurred. Please try again.';
        errorDiv.classList.remove('d-none');
        addText.classList.remove('d-none');
        addSpinner.classList.add('d-none');
    }
}

// ============================================
// WELCOME MESSAGE ANIMATION
// ============================================

function showWelcomeMessage() {
    // This will be called on page load
    const userName = document.querySelector('[data-user-name]')?.getAttribute('data-user-name');
    const userRole = document.querySelector('[data-user-role]')?.getAttribute('data-user-role');

    if (!userName) return;

    const message = userRole === 'admin' ? 'Welcome back, Admin' : `Welcome, ${userName}`;

    // Create welcome toast
    const toastHTML = `
        <div class="position-fixed top-0 end-0 p-3" style="z-index: 11000;">
            <div id="welcomeToast" class="toast align-items-center text-white bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="ti ti-hand-stop me-2"></i>${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', toastHTML);

    const toastElement = document.getElementById('welcomeToast');
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });
    toast.show();

    // Remove after hiding
    toastElement.addEventListener('hidden.bs.toast', function () {
        this.parentElement.remove();
    });
}

// ============================================
// INITIALIZE ON PAGE LOAD
// ============================================

document.addEventListener('DOMContentLoaded', function () {
    // Show welcome message
    showWelcomeMessage();

    // Make sensor cards clickable
    document.querySelectorAll('[data-sensor-card]').forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function () {
            const deviceId = this.getAttribute('data-device-id');
            const sensorType = this.getAttribute('data-sensor-type');
            const sensorName = this.getAttribute('data-sensor-name');
            const currentValue = this.getAttribute('data-sensor-value');
            const unit = this.getAttribute('data-sensor-unit');

            openSensorPopup(deviceId, sensorType, sensorName, currentValue, unit);
        });
    });
});

// Export functions for global use
window.showAddDeviceModal = showAddDeviceModal;
window.submitAddDevice = submitAddDevice;
window.openSensorPopup = openSensorPopup;
