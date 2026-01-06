import React, { useState, useEffect } from 'react';
import { Thermometer, Droplets, Wind, Sun, Zap, Activity, Leaf, Loader } from 'lucide-react';
import HealthGauge from '../components/HealthGauge';
import SensorCard from '../components/SensorCard';
import { getDevices, getLatestReadings } from '../services/api';

const Dashboard = () => {
    const [loading, setLoading] = useState(true);
    const [device, setDevice] = useState(null);
    const [readings, setReadings] = useState({});
    const [error, setError] = useState(null);

    // Dummy data for sparklines (keep for now as API doesn't return history yet in this call)
    const sparkData = [
        { value: 20 }, { value: 22 }, { value: 24 }, { value: 23 }, { value: 25 }, { value: 24 }
    ];

    useEffect(() => {
        const fetchData = async () => {
            try {
                const devicesRes = await getDevices();
                if (devicesRes.data.results.length > 0) {
                    const firstDevice = devicesRes.data.results[0];
                    setDevice(firstDevice);

                    const readingsRes = await getLatestReadings(firstDevice.id);
                    setReadings(readingsRes.data);
                }
                setLoading(false);
            } catch (err) {
                console.error("Failed to fetch data", err);
                setError("Failed to load dashboard data. Ensure backend is running.");
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <Loader className="animate-spin text-agri-primary" size={48} />
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center h-full text-red-500">
                {error}
            </div>
        );
    }

    if (!device) {
        return (
            <div className="flex items-center justify-center h-full text-gray-500">
                No devices found. Please generate sample data.
            </div>
        );
    }

    const getReading = (type) => {
        const reading = readings[type]; // Type is display name from backend
        // Backend returns display names like "Temperature (°C)", need to match or adjust backend to return codes
        // Actually, the backend `latest_readings` action returns keys as `sensor.get_sensor_type_display()`.
        // Let's check what those are in models.py.
        // ('temperature', 'Temperature (°C)'),
        // ('ph', 'pH Level'),
        // ('humidity', 'Humidity (%)'),
        // ('moisture', 'Soil/Medium Moisture (%)'),
        // ('light_hours', 'Light Hours (hrs)'),
        // ('conductivity', 'Electrical Conductivity (mS/cm)'),

        // This is a bit fragile. Ideally backend should return codes.
        // For now, I'll try to match by partial string or just log what I get.
        // Let's iterate keys to find matches.

        const key = Object.keys(readings).find(k => k.toLowerCase().includes(type.toLowerCase()));
        return readings[key] ? readings[key].value : '--';
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column: Health Gauge */}
            <div className="lg:col-span-1 h-96">
                <HealthGauge score={94} status="Excellent" />
                <div className="mt-4 text-center">
                    <h2 className="text-xl font-bold text-gray-800">{device.name}</h2>
                    <p className="text-gray-500">{device.location}</p>
                </div>
            </div>

            {/* Right Column: Metrics Grid */}
            <div className="lg:col-span-2 flex flex-col gap-8">

                {/* Environmental Conditions */}
                <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100">
                    <div className="flex justify-between items-center mb-6">
                        <div className="flex items-center">
                            <div className="w-1 h-6 bg-agri-primary rounded-full mr-3"></div>
                            <h3 className="text-lg font-bold text-gray-800">Environmental Conditions</h3>
                        </div>
                        <button className="text-sm text-agri-primary font-medium hover:underline">View History</button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <SensorCard
                            icon={Thermometer}
                            label="Temperature"
                            value={getReading('Temperature')}
                            unit="°C"
                            range="18 - 30 °C"
                            data={sparkData}
                            color="#f39c12"
                        />
                        <SensorCard
                            icon={Wind}
                            label="Humidity"
                            value={getReading('Humidity')}
                            unit="%"
                            range="50 - 80 %"
                            data={sparkData}
                            color="#3498db"
                        />
                        <SensorCard
                            icon={Sun}
                            label="Light Hours"
                            value={getReading('Light')}
                            unit="hrs"
                            range="10 - 16 hrs"
                            data={sparkData}
                            color="#f1c40f"
                        />
                    </div>
                </div>

                {/* Water & Nutrients */}
                <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100">
                    <div className="flex justify-between items-center mb-6">
                        <div className="flex items-center">
                            <div className="w-1 h-6 bg-blue-500 rounded-full mr-3"></div>
                            <h3 className="text-lg font-bold text-gray-800">Water & Nutrients</h3>
                        </div>
                        <button className="text-sm text-blue-500 font-medium hover:underline">Calibrate</button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <SensorCard
                            icon={Droplets}
                            label="pH Level"
                            value={getReading('pH')}
                            unit="pH"
                            range="5.5 - 6.5 pH"
                            data={sparkData}
                            color="#3498db"
                        />
                        <SensorCard
                            icon={Zap}
                            label="EC (Conductivity)"
                            value={getReading('Conductivity')}
                            unit="mS/cm"
                            range="1 - 2.5 mS/cm"
                            data={sparkData}
                            color="#9b59b6"
                        />
                        <SensorCard
                            icon={Leaf}
                            label="Substrate Moisture"
                            value={getReading('Moisture')}
                            unit="%"
                            range="60 - 85 %"
                            data={sparkData}
                            color="#27ae60"
                        />
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Dashboard;
