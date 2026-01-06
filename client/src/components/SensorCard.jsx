import React from 'react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';

const SensorCard = ({ icon: Icon, label, value, unit, range, data, color = "#27ae60" }) => {
    return (
        <div className="flex items-center justify-between p-2">
            <div className="flex items-start">
                <div className={`p-3 rounded-xl bg-${color}/10 text-${color} mr-4`}>
                    <Icon size={24} color={color} />
                </div>
                <div>
                    <p className="text-gray-500 text-sm font-medium">{label}</p>
                    <div className="flex items-baseline mt-1">
                        <span className="text-2xl font-bold text-gray-800">{value}</span>
                        <span className="text-sm text-gray-400 ml-1">{unit}</span>
                    </div>
                    <p className="text-xs text-gray-400 mt-1">{range}</p>
                </div>
            </div>

            <div className="h-12 w-24">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <Line
                            type="monotone"
                            dataKey="value"
                            stroke={color}
                            strokeWidth={2}
                            dot={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default SensorCard;
