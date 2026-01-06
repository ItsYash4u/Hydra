import React from 'react';
import { motion } from 'framer-motion';

const HealthGauge = ({ score = 94, status = "Excellent" }) => {
    const circumference = 2 * Math.PI * 40; // radius 40
    const strokeDashoffset = circumference - (score / 100) * circumference;

    return (
        <div className="bg-white rounded-3xl p-8 shadow-sm h-full flex flex-col justify-between relative overflow-hidden">
            {/* Background decoration */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-agri-success/5 rounded-bl-full -mr-8 -mt-8"></div>

            <div>
                <h3 className="text-gray-500 text-xs font-bold tracking-wider uppercase mb-1">Overall Health</h3>
                <h2 className="text-3xl font-bold text-agri-primary">{status}</h2>
            </div>

            <div className="flex items-center justify-center my-6 relative">
                {/* SVG Gauge */}
                <svg className="w-48 h-48 transform -rotate-90">
                    <circle
                        cx="96"
                        cy="96"
                        r="40"
                        stroke="#ecf0f1"
                        strokeWidth="8"
                        fill="transparent"
                        className="text-gray-100"
                    />
                    <motion.circle
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                        cx="96"
                        cy="96"
                        r="40"
                        stroke="currentColor"
                        strokeWidth="8"
                        fill="transparent"
                        strokeDasharray={circumference}
                        strokeLinecap="round"
                        className="text-agri-accent"
                    />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center flex-col">
                    <span className="text-5xl font-bold text-gray-800">{score}<span className="text-2xl text-gray-400">%</span></span>
                </div>
            </div>

            <div className="flex items-center justify-between bg-agri-bg/50 p-3 rounded-xl">
                <div className="flex items-center text-agri-success text-sm font-medium">
                    <div className="w-2 h-2 bg-agri-success rounded-full mr-2"></div>
                    All Systems Optimal
                </div>
                <span className="text-xs text-gray-400">Updated 2m ago</span>
            </div>
        </div>
    );
};

export default HealthGauge;
