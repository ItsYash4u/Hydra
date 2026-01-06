/**
 * Dashboard Initialization Script
 * Initializes ApexCharts and Leaflet Map using data provided via JSON script tag.
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Read Configuration Data
    const contextEl = document.getElementById('dashboard-context');
    if (!contextEl) {
        console.warn('Dashboard context not found');
        return;
    }

    let data;
    try {
        data = JSON.parse(contextEl.textContent);
    } catch (e) {
        console.error('Failed to parse dashboard context', e);
        return;
    }

    // 2. Initialize Environment Trends Chart
    const envTrendsOptions = {
        series: [{
            name: 'Temperature',
            data: [22, 24, 23, 25, 24, 26, 25]
        }, {
            name: 'Humidity',
            data: [65, 68, 70, 67, 69, 71, 68]
        }, {
            name: 'Wind Speed',
            data: [12, 15, 14, 16, 13, 15, 14]
        }],
        chart: {
            type: 'area',
            height: 300,
            toolbar: { show: false },
            background: 'transparent'
        },
        dataLabels: { enabled: false },
        stroke: {
            curve: 'smooth',
            width: 2
        },
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.4,
                opacityTo: 0.1,
            }
        },
        colors: ['#667eea', '#0acf97', '#fa5c7c'],
        xaxis: {
            categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            labels: { style: { colors: '#8e8da4' } }
        },
        yaxis: {
            labels: { style: { colors: '#8e8da4' } }
        },
        legend: {
            position: 'top',
            horizontalAlign: 'right',
            labels: { colors: '#8e8da4' }
        },
        grid: {
            borderColor: '#f1f3fa'
        }
    };

    const chartEl = document.querySelector("#environment-trends-chart");
    if (chartEl) {
        window.envTrendsChart = new ApexCharts(chartEl, envTrendsOptions);
        window.envTrendsChart.render();
    }


    // 3. Initialize Device Health Donut Chart
    const deviceHealthOptions = {
        series: [data.online_devices, data.offline_devices, 0, 0],
        chart: {
            type: 'donut',
            height: 300
        },
        labels: ['Online', 'Offline', 'Maintenance', 'Faulty'],
        colors: ['#0acf97', '#fa5c7c', '#ffbc00', '#39afd1'],
        legend: { show: false },
        plotOptions: {
            pie: {
                donut: {
                    size: '70%',
                    labels: {
                        show: true,
                        name: {
                            show: true,
                            fontSize: '16px',
                            color: '#8e8da4'
                        },
                        value: {
                            show: true,
                            fontSize: '24px',
                            fontWeight: 600,
                            color: '#313a46'
                        },
                        total: {
                            show: true,
                            label: 'Total',
                            fontSize: '14px',
                            color: '#8e8da4',
                            formatter: function (w) {
                                return data.total_devices;
                            }
                        }
                    }
                }
            }
        },
        dataLabels: { enabled: false }
    };

    const healthChartEl = document.querySelector("#device-health-chart");
    if (healthChartEl) {
        new ApexCharts(healthChartEl, deviceHealthOptions).render();
    }


    // 4. Initialize Farm Locations Map
    const mapEl = document.getElementById('farm-locations-map');
    if (mapEl && data.devices && data.devices.length > 0) {

        // Generate points with randomized coordinates (visual only)
        const centerLat = 20.59;
        const centerLon = 78.96;

        const map = L.map('farm-locations-map').setView([centerLat, centerLon], 5);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        data.devices.forEach(device => {
            // Logic moved from template: generic randomization for visualization
            const lat = centerLat + (Math.random() - 0.5) * 10;
            const lon = centerLon + (Math.random() - 0.5) * 10;
            const color = device.status === 'online' ? 'green' : 'red';

            const markerHtml = `
                <div style="
                    background-color: ${color};
                    width: 15px;
                    height: 15px;
                    border-radius: 50%;
                    border: 2px solid white;
                    box-shadow: 0 0 10px rgba(0,0,0,0.5);
                "></div>
            `;

            const icon = L.divIcon({
                className: 'custom-marker',
                html: markerHtml,
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            });

            const marker = L.marker([lat, lon], { icon: icon }).addTo(map);
            marker.bindPopup(`<b>${device.id}</b><br>Status: ${device.status}`);
        });
    }

    // 5. User Data Attributes (Optional Helper)
    if (data.user) {
        const userDataDiv = document.createElement('div');
        userDataDiv.setAttribute('data-user-name', data.user.name || data.user.email);
        userDataDiv.setAttribute('data-user-role', data.user.role);
        userDataDiv.style.display = 'none';
        document.body.appendChild(userDataDiv);
    }
});
