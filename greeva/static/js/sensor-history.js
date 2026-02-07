/**
 * Sensor History Module
 * Handles fetching and displaying sensor readings in a stack format (newest first)
 */

const SensorHistoryManager = (() => {
    const API_BASE = '/api/devices';
    let currentDeviceId = null;

    /**
     * Fetch sensor history for a device
     */
    async function fetchHistory(deviceId) {
        try {
            const response = await fetch(
                `${API_BASE}/sensors/history/?device_id=${encodeURIComponent(deviceId)}`
            );

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();
            return data.readings || [];
        } catch (error) {
            console.error('Error fetching sensor history:', error);
            return [];
        }
    }

    /**
     * Format timestamp to readable string
     */
    function formatTimestamp(timestamp) {
        try {
            const date = new Date(timestamp);
            return date.toLocaleString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        } catch (e) {
            return timestamp;
        }
    }

    /**
     * Format date to readable string
     */
    function formatDate(dateStr) {
        try {
            const date = new Date(dateStr + 'T00:00:00');
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        } catch (e) {
            return dateStr;
        }
    }

    /**
     * Create HTML for a single reading card
     */
    function createReadingCard(reading, index) {
        const isLatest = index === 0;
        const badgeClass = isLatest ? 'bg-success-subtle text-success' : 'bg-secondary-subtle text-secondary';
        const badgeText = isLatest ? 'Latest' : `#${index}`;

        return `
            <div class="card sensor-reading-card mb-3 border-start border-4 ${isLatest ? 'border-success' : 'border-secondary'}" 
                 data-reading-id="${reading.id}">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h6 class="mb-0 fw-bold">${formatDate(reading.date)}</h6>
                            <small class="text-muted">${formatTimestamp(reading.timestamp)}</small>
                        </div>
                        <span class="badge ${badgeClass} px-3 py-2">${badgeText}</span>
                    </div>

                    <div class="row g-3">
                        <!-- Temperature -->
                        <div class="col-6 col-md-3">
                            <div class="text-center p-2 bg-light rounded">
                                <small class="text-muted d-block">Temperature</small>
                                <h5 class="mb-0 fw-bold">
                                    <span class="sensor-value-display">
                                        ${reading.temperature !== null ? reading.temperature.toFixed(1) : '--'}
                                    </span>
                                    <small class="text-muted">°C</small>
                                </h5>
                            </div>
                        </div>

                        <!-- Humidity -->
                        <div class="col-6 col-md-3">
                            <div class="text-center p-2 bg-light rounded">
                                <small class="text-muted d-block">Humidity</small>
                                <h5 class="mb-0 fw-bold">
                                    <span class="sensor-value-display">
                                        ${reading.humidity !== null ? reading.humidity.toFixed(1) : '--'}
                                    </span>
                                    <small class="text-muted">%</small>
                                </h5>
                            </div>
                        </div>

                        <!-- pH -->
                        <div class="col-6 col-md-3">
                            <div class="text-center p-2 bg-light rounded">
                                <small class="text-muted d-block">pH</small>
                                <h5 class="mb-0 fw-bold">
                                    <span class="sensor-value-display">
                                        ${reading.ph !== null ? reading.ph.toFixed(2) : '--'}
                                    </span>
                                </h5>
                            </div>
                        </div>

                        <!-- EC -->
                        <div class="col-6 col-md-3">
                            <div class="text-center p-2 bg-light rounded">
                                <small class="text-muted d-block">EC</small>
                                <h5 class="mb-0 fw-bold">
                                    <span class="sensor-value-display">
                                        ${reading.ec !== null ? reading.ec.toFixed(2) : '--'}
                                    </span>
                                </h5>
                            </div>
                        </div>

                        <!-- Water Temp -->
                        <div class="col-6 col-md-3">
                            <div class="text-center p-2 bg-light rounded">
                                <small class="text-muted d-block">Water Temp</small>
                                <h5 class="mb-0 fw-bold">
                                    <span class="sensor-value-display">
                                        ${reading.water_temp !== null ? reading.water_temp.toFixed(1) : '--'}
                                    </span>
                                    <small class="text-muted">°C</small>
                                </h5>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Display sensor reading history in a container
     */
    async function displayHistory(deviceId, containerId, limit = null) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.warn(`Container with id '${containerId}' not found`);
            return;
        }

        // Show loading state
        container.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="text-muted mt-2">Loading sensor history...</p>
            </div>
        `;

        const readings = await fetchHistory(deviceId);
        const totalReadings = readings.length;
        const displayReadings = (limit && readings.length > limit)
            ? readings.slice(0, limit)
            : readings;

        if (displayReadings.length === 0) {
            container.innerHTML = `
                <div class="alert alert-info" role="alert">
                    <i class="ti ti-info-circle me-2"></i>
                    No sensor readings available yet for this device.
                </div>
            `;
            return;
        }

        // Generate HTML for all readings
        let html = `
            <div class="sensor-history-container">
                <div class="mb-3">
                    <small class="text-muted">
                        <i class="ti ti-stack me-1"></i>
                        Total Readings: <strong>${totalReadings}</strong>
                    </small>
                    ${limit ? `<small class="text-muted ms-2">Showing: <strong>${displayReadings.length}</strong></small>` : ''}
                </div>
        `;

        displayReadings.forEach((reading, index) => {
            html += createReadingCard(reading, index);
        });

        html += '</div>';
        container.innerHTML = html;
    }

    /**
     * Update sensor display with latest reading
     */
    async function updateLatestReading(deviceId) {
        const readings = await fetchHistory(deviceId);

        if (readings.length === 0) {
            return null;
        }

        const latest = readings[0]; // Newest reading
        return {
            temperature: latest.temperature,
            humidity: latest.humidity,
            ph: latest.ph,
            ec: latest.ec,
            co2: latest.co2,
            water_temp: latest.water_temp,
            timestamp: latest.timestamp,
            date: latest.date
        };
    }

    /**
     * Set up periodic refresh of sensor history
     */
    function startAutoRefresh(deviceId, containerId, intervalMs = 10000, limit = null) {
        // Initial load
        displayHistory(deviceId, containerId, limit);

        // Refresh every interval
        const intervalId = setInterval(() => {
            displayHistory(deviceId, containerId, limit);
        }, intervalMs);

        return intervalId; // Return ID so it can be stopped later
    }

    /**
     * Stop auto-refresh
     */
    function stopAutoRefresh(intervalId) {
        if (intervalId) {
            clearInterval(intervalId);
        }
    }

    /**
     * Public API
     */
    return {
        fetchHistory,
        displayHistory,
        updateLatestReading,
        startAutoRefresh,
        stopAutoRefresh,
        formatTimestamp,
        formatDate
    };
})();

// Export for use
window.SensorHistoryManager = SensorHistoryManager;
