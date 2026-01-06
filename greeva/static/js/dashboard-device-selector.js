/**
 * Dashboard Interaction Logic
 * Handles table row clicks, sensor customization, drag-and-drop, and detail views.
 */

// ----------------------------------------------------------------------------
// Global Functions for HTML Event Handlers
// ----------------------------------------------------------------------------

window.toggleSensor = function (sensorName) {
    const grid = document.getElementById('sensor-grid');
    if (!grid) return;

    // Normalize logic for matching
    // sensorName comes from checkbox e.g. 'Temperature'
    // data-sensor-type is 'temperature'

    const cards = grid.querySelectorAll('.sensor-col');
    let hiddenSensors = JSON.parse(localStorage.getItem('hiddenSensors') || '[]');
    const nameLower = sensorName.toLowerCase();

    cards.forEach(col => {
        const type = col.getAttribute('data-sensor-type').toLowerCase();

        // Flexible matching: 'light' matches 'light_hours', 'ec' matches 'ec'
        if (type.includes(nameLower)) {
            const checklistId = `check-${nameLower.replace(' ', '-')}`;
            // If mapping fails (e.g. EC -> ec vs check-ec), ensure IDs match params

            const checkbox = document.getElementById(`check-${sensorName.toLowerCase()}`); // Param is passed directly from HTML

            if (checkbox && checkbox.checked) {
                col.classList.remove('d-none');
                hiddenSensors = hiddenSensors.filter(s => s !== col.getAttribute('data-sensor-type'));
            } else if (checkbox && !checkbox.checked) {
                col.classList.add('d-none');
                const rawType = col.getAttribute('data-sensor-type');
                if (!hiddenSensors.includes(rawType)) hiddenSensors.push(rawType);
            }
        }
    });
    localStorage.setItem('hiddenSensors', JSON.stringify(hiddenSensors));
};

window.openSensorDetail = function (card) {
    const type = card.getAttribute('data-sensor-name');
    const value = card.getAttribute('data-sensor-value');
    // Try to find unit in the card
    const unitEl = card.querySelector('small.fs-16');
    const unit = unitEl ? unitEl.innerText.trim() : '';

    // Update Modal
    const titleEl = document.getElementById('detail-sensor-name');
    if (titleEl) titleEl.textContent = type + ' Details';

    const valEl = document.getElementById('detail-sensor-value');
    if (valEl) valEl.textContent = parseFloat(value).toFixed(1);

    const unitDisplay = document.getElementById('detail-sensor-unit');
    if (unitDisplay) unitDisplay.textContent = unit;

    // Mock Stats
    const v = parseFloat(value);
    document.getElementById('detail-min').textContent = (v * 0.9).toFixed(1);
    document.getElementById('detail-avg').textContent = v.toFixed(1);
    document.getElementById('detail-max').textContent = (v * 1.1).toFixed(1);

    // Render Chart
    if (window.ApexCharts) renderMiniChart(type, v);

    // Show Modal using Bootstrap API
    const modalEl = document.getElementById('sensorDetailModal');
    if (modalEl && window.bootstrap) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
};

function renderMiniChart(label, currentValue) {
    const chartEl = document.querySelector("#sensor-mini-chart");
    if (!chartEl) return;
    chartEl.innerHTML = '';

    // Generate trend data ending at current value
    const data = [];
    let val = currentValue;
    for (let i = 0; i < 15; i++) {
        data.unshift(val);
        val = val + (Math.random() - 0.5) * (currentValue * 0.1);
    }

    const options = {
        series: [{ name: label, data: data }],
        chart: {
            type: 'area', height: 150, sparkline: { enabled: true },
            fontFamily: 'inherit'
        },
        stroke: { curve: 'smooth', width: 2 },
        fill: { type: 'gradient', gradient: { opacityFrom: 0.5, opacityTo: 0.1 } },
        colors: ['#727cf5'],
        tooltip: { fixed: { enabled: false }, x: { show: false }, marker: { show: false } }
    };

    new ApexCharts(chartEl, options).render();
}

// ----------------------------------------------------------------------------
// Main Dashboard Logic
// ----------------------------------------------------------------------------

(function () {
    'use strict';
    let currentDeviceId = null;

    function initDashboard() {
        // 1. Table Interaction
        const deviceRows = document.querySelectorAll('.device-row');
        if (deviceRows.length > 0) {
            deviceRows.forEach(row => {
                row.addEventListener('click', function (e) {
                    // Prevent row click if clicking a button inside row (if any)
                    selectDevice(this, this.getAttribute('data-device-id'), this.getAttribute('data-device-name'));
                });
            });
        }

        // 2. Drag and Drop Config
        const grid = document.getElementById('sensor-grid');
        if (grid && window.Sortable) {
            new Sortable(grid, {
                animation: 150,
                handle: '.cursor-grab', // Drag handle targeting the card
                ghostClass: 'bg-light-subtle',
                onEnd: function () {
                    saveSensorOrder();
                }
            });
            restoreSensorOrder();
        }

        // 3. Restore Visibility Preferences
        restoreSensorVisibility();
    }

    function saveSensorOrder() {
        const grid = document.getElementById('sensor-grid');
        const order = [];
        grid.querySelectorAll('.sensor-col').forEach(col => {
            order.push(col.getAttribute('data-sensor-type'));
        });
        localStorage.setItem('sensorOrder', JSON.stringify(order));
    }

    function restoreSensorOrder() {
        const grid = document.getElementById('sensor-grid');
        const order = JSON.parse(localStorage.getItem('sensorOrder'));
        if (!order || !grid) return;

        const items = Array.from(grid.children);
        const itemsMap = {};
        items.forEach(item => itemsMap[item.getAttribute('data-sensor-type')] = item);

        order.forEach(type => {
            if (itemsMap[type]) grid.appendChild(itemsMap[type]);
        });
        // Append remaining
        items.forEach(item => {
            if (!order.includes(item.getAttribute('data-sensor-type'))) grid.appendChild(item);
        });
    }

    function restoreSensorVisibility() {
        // Initialize defaults if first time
        if (!localStorage.getItem('hiddenSensorsInitialized')) {
            // Default hidden sensors (Hydroponics extras)
            const defaultHidden = ['potassium', 'water_temp', 'dissolved_oxygen', 'tds', 'orp', 'co2', 'water_level', 'flow_rate'];
            localStorage.setItem('hiddenSensors', JSON.stringify(defaultHidden));
            localStorage.setItem('hiddenSensorsInitialized', 'true');
        }

        const hidden = JSON.parse(localStorage.getItem('hiddenSensors') || '[]');

        // Reset state: Show all, Check all (to handle un-hiding)
        document.querySelectorAll('.sensor-col').forEach(c => c.classList.remove('d-none'));
        document.querySelectorAll('#sensor-toggles input').forEach(c => c.checked = true);

        hidden.forEach(type => {
            const col = document.querySelector(`.sensor-col[data-sensor-type="${type}"]`);
            if (col) col.classList.add('d-none');

            let checkId = 'check-' + type.replace('_', '-');
            if (type === 'light_hours') checkId = 'check-light';

            const box = document.getElementById(checkId);
            if (box) box.checked = false;
        });
    }

    // Device Selection
    function selectDevice(rowElement, deviceId, deviceName) {
        document.querySelectorAll('.device-row').forEach(r => r.classList.remove('table-active'));
        if (rowElement) rowElement.classList.add('table-active');

        currentDeviceId = deviceId;
        const header = document.getElementById('live-sensor-header');
        if (header) header.innerHTML = `Live Sensor Data (Device ID: <span id="active-device-id" class="fw-bold text-primary">${deviceId}</span>)`;

        loadDeviceData(deviceId);
    }

    async function loadDeviceData(deviceId) {
        try {
            const response = await fetch(`/hydroponics/api/latest/${deviceId}/`);
            if (!response.ok) throw new Error('API Error');
            const data = await response.json();

            updateSensorCards(data);

            if (window.envTrendsChart && data.history) {
                window.envTrendsChart.updateSeries([
                    { name: 'Temperature', data: data.history.temperature },
                    { name: 'Humidity', data: data.history.humidity },
                    { name: 'Wind Speed', data: [12, 14, 13, 15, 12, 14, 13] } // Mock wind
                ]);
                if (data.history.dates) window.envTrendsChart.updateOptions({ xaxis: { categories: data.history.dates } });
            }
        } catch (e) { console.error(e); }
    }

    function updateSensorCards(data) {
        const cards = document.querySelectorAll('[data-sensor-card]');
        cards.forEach(card => {
            const type = card.getAttribute('data-sensor-type');
            let val = data[type];

            if (val !== undefined && val !== null) {
                const valEl = card.querySelector('.sensor-value');
                if (valEl) valEl.innerText = parseFloat(val).toFixed(1);

                card.setAttribute('data-sensor-value', val);

                const timeEl = card.querySelector('.sensor-time');
                if (timeEl) timeEl.innerText = 'Just now';

                // Highlight update
                const cardInner = card.querySelector('.sensor-card') || card;
                cardInner.style.transform = 'scale(1.02)';
                setTimeout(() => cardInner.style.transform = 'scale(1)', 300);
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDashboard);
    } else {
        initDashboard();
    }

})();
