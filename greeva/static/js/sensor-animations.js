// ============================================
// SENSOR ANIMATION LIBRARY
// Premium animated visualizations for each sensor type
// ============================================

/**
 * Temperature Sensor - Mercury Thermometer Animation
 * Visual: Vertical thermometer with rising/falling mercury
 * Color gradient: Blue (cold) → Green (optimal) → Red (hot)
 */
function renderTemperatureAnimation(containerId, value, min = 0, max = 50) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const percentage = ((value - min) / (max - min)) * 100;

    // Determine color based on value
    let color = '#10b981'; // Green (optimal)
    if (value < 15) color = '#3b82f6'; // Blue (cold)
    else if (value > 30) color = '#ef4444'; // Red (hot)

    container.innerHTML = `
        <div class="thermometer-container" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding: 20px;">
            <div class="thermometer-bulb-container" style="position: relative; width: 60px; height: 250px;">
                <!-- Thermometer tube -->
                <div style="position: absolute; left: 50%; transform: translateX(-50%); width: 20px; height: 180px; background: rgba(200, 200, 200, 0.3); border-radius: 10px 10px 0 0; border: 2px solid #ccc;"></div>
                
                <!-- Mercury fill -->
                <div class="mercury-fill" style="position: absolute; left: 50%; transform: translateX(-50%); bottom: 50px; width: 16px; background: ${color}; border-radius: 8px 8px 0 0; transition: height 0.8s cubic-bezier(0.4, 0, 0.2, 1), background 0.8s ease; height: ${percentage * 1.8}px;"></div>
                
                <!-- Thermometer bulb -->
                <div style="position: absolute; left: 50%; bottom: 0; transform: translateX(-50%); width: 50px; height: 50px; background: ${color}; border-radius: 50%; border: 3px solid #ccc; transition: background 0.8s ease;"></div>
                
                <!-- Temperature markers -->
                <div style="position: absolute; right: -30px; top: 0; height: 180px; display: flex; flex-direction: column; justify-content: space-between; font-size: 10px; color: #999;">
                    <span>${max}°</span>
                    <span>${Math.round((max + min) / 2)}°</span>
                    <span>${min}°</span>
                </div>
            </div>
            
            <!-- Value display -->
            <div style="margin-top: 20px; text-align: center;">
                <div style="font-size: 32px; font-weight: bold; color: ${color}; transition: color 0.8s ease;">${value.toFixed(1)}°C</div>
                <div style="font-size: 12px; color: #999; margin-top: 5px;">
                    ${value < 15 ? 'Cold' : value > 30 ? 'Hot' : 'Optimal'}
                </div>
            </div>
        </div>
    `;
}

/**
 * pH Sensor - Speedometer/Gauge Animation
 * Visual: Semicircular gauge with needle
 * Color zones: Acidic (red) → Neutral (green) → Alkaline (orange)
 */
function renderPHAnimation(containerId, value, min = 0, max = 14) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const percentage = ((value - min) / (max - min)) * 100;
    const angle = -90 + (percentage * 1.8); // -90 to 90 degrees

    // Determine color and zone
    let color = '#10b981'; // Neutral (green)
    let zone = 'Neutral';
    if (value < 5.5) {
        color = '#ef4444'; // Acidic (red)
        zone = 'Acidic';
    } else if (value > 7.5) {
        color = '#f59e0b'; // Alkaline (orange)
        zone = 'Alkaline';
    }

    container.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding: 20px;">
            <!-- Gauge container -->
            <div style="position: relative; width: 200px; height: 120px;">
                <!-- Background arc -->
                <svg width="200" height="120" style="position: absolute; top: 0; left: 0;">
                    <!-- Acidic zone (red) -->
                    <path d="M 20,100 A 80,80 0 0,1 73,28" fill="none" stroke="#ef4444" stroke-width="20" opacity="0.3"/>
                    <!-- Neutral zone (green) -->
                    <path d="M 73,28 A 80,80 0 0,1 127,28" fill="none" stroke="#10b981" stroke-width="20" opacity="0.3"/>
                    <!-- Alkaline zone (orange) -->
                    <path d="M 127,28 A 80,80 0 0,1 180,100" fill="none" stroke="#f59e0b" stroke-width="20" opacity="0.3"/>
                </svg>
                
                <!-- Needle -->
                <div style="position: absolute; bottom: 10px; left: 50%; width: 2px; height: 70px; background: ${color}; transform-origin: bottom center; transform: translateX(-50%) rotate(${angle}deg); transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1), background 0.8s ease;">
                    <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 8px; height: 8px; background: ${color}; border-radius: 50%; box-shadow: 0 0 10px ${color};"></div>
                </div>
                
                <!-- Center dot -->
                <div style="position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); width: 12px; height: 12px; background: #333; border-radius: 50%; border: 2px solid #fff;"></div>
                
                <!-- Scale markers -->
                <div style="position: absolute; bottom: 5px; left: 10px; font-size: 10px; color: #999;">0</div>
                <div style="position: absolute; bottom: 5px; left: 50%; transform: translateX(-50%); font-size: 10px; color: #999;">7</div>
                <div style="position: absolute; bottom: 5px; right: 10px; font-size: 10px; color: #999;">14</div>
            </div>
            
            <!-- Value display -->
            <div style="margin-top: 20px; text-align: center;">
                <div style="font-size: 32px; font-weight: bold; color: ${color}; transition: color 0.8s ease;">${value.toFixed(1)} pH</div>
                <div style="font-size: 12px; color: #999; margin-top: 5px;">${zone}</div>
            </div>
        </div>
    `;
}

/**
 * Humidity/Moisture Sensor - Droplet/Tank Fill Animation
 * Visual: Water droplet or tank with rising fill level
 * Includes subtle wave/ripple motion
 */
function renderHumidityAnimation(containerId, value, min = 0, max = 100) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const percentage = ((value - min) / (max - min)) * 100;

    // Determine color based on value
    let color = '#10b981'; // Optimal (green)
    if (value < 30) color = '#ef4444'; // Low (red)
    else if (value > 70) color = '#3b82f6'; // High (blue)

    container.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding: 20px;">
            <!-- Droplet container -->
            <div style="position: relative; width: 120px; height: 160px;">
                <!-- Droplet outline -->
                <svg width="120" height="160" style="position: absolute; top: 0; left: 0;">
                    <path d="M 60,10 C 60,10 20,60 20,100 C 20,133 40,150 60,150 C 80,150 100,133 100,100 C 100,60 60,10 60,10 Z" 
                          fill="rgba(200, 200, 200, 0.2)" stroke="#ccc" stroke-width="2"/>
                </svg>
                
                <!-- Water fill with clip path -->
                <svg width="120" height="160" style="position: absolute; top: 0; left: 0; overflow: hidden;">
                    <defs>
                        <clipPath id="droplet-clip-${containerId}">
                            <path d="M 60,10 C 60,10 20,60 20,100 C 20,133 40,150 60,150 C 80,150 100,133 100,100 C 100,60 60,10 60,10 Z"/>
                        </clipPath>
                    </defs>
                    <rect x="0" y="${160 - (percentage * 1.4)}" width="120" height="${percentage * 1.4}" 
                          fill="${color}" opacity="0.7" clip-path="url(#droplet-clip-${containerId})"
                          style="transition: y 0.8s cubic-bezier(0.4, 0, 0.2, 1), height 0.8s cubic-bezier(0.4, 0, 0.2, 1), fill 0.8s ease;">
                        <animate attributeName="y" 
                                 values="${160 - (percentage * 1.4)};${160 - (percentage * 1.4) - 2};${160 - (percentage * 1.4)}" 
                                 dur="2s" repeatCount="indefinite"/>
                    </rect>
                </svg>
                
                <!-- Percentage text inside droplet -->
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 24px; font-weight: bold; color: #333; z-index: 10;">
                    ${Math.round(percentage)}%
                </div>
            </div>
            
            <!-- Value display -->
            <div style="margin-top: 20px; text-align: center;">
                <div style="font-size: 32px; font-weight: bold; color: ${color}; transition: color 0.8s ease;">${value.toFixed(1)}%</div>
                <div style="font-size: 12px; color: #999; margin-top: 5px;">
                    ${value < 30 ? 'Low' : value > 70 ? 'High' : 'Optimal'}
                </div>
            </div>
        </div>
    `;
}

/**
 * CO2/Gas Sensor - Pulsing Density Rings Animation
 * Visual: Concentric circles with pulsing intensity
 * Ring intensity increases with value
 */
function renderCO2Animation(containerId, value, min = 0, max = 2000) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const percentage = ((value - min) / (max - min)) * 100;

    // Determine color and intensity
    let color = '#10b981'; // Optimal (green)
    if (value < 400) color = '#3b82f6'; // Low (blue)
    else if (value > 1000) color = '#ef4444'; // High (red)

    const opacity1 = Math.min(percentage / 100, 1);
    const opacity2 = Math.min((percentage - 20) / 100, 0.7);
    const opacity3 = Math.min((percentage - 40) / 100, 0.5);

    container.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding: 20px;">
            <!-- Pulsing rings container -->
            <div style="position: relative; width: 200px; height: 200px;">
                <!-- Ring 3 (outermost) -->
                <div class="co2-ring" style="position: absolute; top: 0; left: 0; width: 200px; height: 200px; border: 3px solid ${color}; border-radius: 50%; opacity: ${opacity3}; animation: pulse-ring 3s ease-in-out infinite;"></div>
                
                <!-- Ring 2 (middle) -->
                <div class="co2-ring" style="position: absolute; top: 25px; left: 25px; width: 150px; height: 150px; border: 3px solid ${color}; border-radius: 50%; opacity: ${opacity2}; animation: pulse-ring 3s ease-in-out infinite 0.5s;"></div>
                
                <!-- Ring 1 (innermost) -->
                <div class="co2-ring" style="position: absolute; top: 50px; left: 50px; width: 100px; height: 100px; border: 3px solid ${color}; border-radius: 50%; opacity: ${opacity1}; animation: pulse-ring 3s ease-in-out infinite 1s;"></div>
                
                <!-- Center value -->
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                    <div style="font-size: 28px; font-weight: bold; color: ${color}; transition: color 0.8s ease;">${Math.round(value)}</div>
                    <div style="font-size: 12px; color: #999;">ppm</div>
                </div>
            </div>
            
            <!-- Status display -->
            <div style="margin-top: 20px; text-align: center;">
                <div style="font-size: 14px; color: #999;">
                    ${value < 400 ? 'Low CO₂' : value > 1000 ? 'High CO₂' : 'Optimal Range'}
                </div>
            </div>
        </div>
        
        <style>
            @keyframes pulse-ring {
                0%, 100% { transform: scale(1); opacity: ${opacity1}; }
                50% { transform: scale(1.1); opacity: ${opacity1 * 0.6}; }
            }
        </style>
    `;
}

/**
 * EC/TDS Sensor - Horizontal Energy Bar Animation
 * Visual: Horizontal bar with glow intensity
 * Smooth transitions based on value
 */
function renderECAnimation(containerId, value, min = 0, max = 5) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const percentage = ((value - min) / (max - min)) * 100;

    // Determine color based on value
    let color = '#10b981'; // Optimal (green)
    if (value < 1) color = '#3b82f6'; // Low (blue)
    else if (value > 3) color = '#ef4444'; // High (red)

    container.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding: 20px;">
            <!-- Energy bar container -->
            <div style="width: 100%; max-width: 300px;">
                <!-- Bar background -->
                <div style="position: relative; width: 100%; height: 40px; background: rgba(200, 200, 200, 0.2); border-radius: 20px; overflow: hidden; border: 2px solid #ccc;">
                    <!-- Animated fill -->
                    <div style="position: absolute; left: 0; top: 0; height: 100%; width: ${percentage}%; background: linear-gradient(90deg, ${color}, ${color}dd); border-radius: 20px; transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1), background 0.8s ease; box-shadow: 0 0 20px ${color}88;">
                        <!-- Glow effect -->
                        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent); animation: shimmer 2s infinite;"></div>
                    </div>
                    
                    <!-- Percentage text -->
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 14px; font-weight: bold; color: #333; z-index: 10;">
                        ${Math.round(percentage)}%
                    </div>
                </div>
                
                <!-- Scale markers -->
                <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 10px; color: #999;">
                    <span>${min}</span>
                    <span>${((max - min) / 2).toFixed(1)}</span>
                    <span>${max}</span>
                </div>
            </div>
            
            <!-- Value display -->
            <div style="margin-top: 30px; text-align: center;">
                <div style="font-size: 32px; font-weight: bold; color: ${color}; transition: color 0.8s ease;">${value.toFixed(2)} mS/cm</div>
                <div style="font-size: 12px; color: #999; margin-top: 5px;">
                    ${value < 1 ? 'Low Conductivity' : value > 3 ? 'High Conductivity' : 'Optimal Range'}
                </div>
            </div>
        </div>
        
        <style>
            @keyframes shimmer {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
        </style>
    `;
}

/**
 * Generic Sensor - Circular Progress Animation
 * Used for sensors without specific animations
 */
function renderGenericAnimation(containerId, value, min, max, unit, label) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const percentage = ((value - min) / (max - min)) * 100;
    const circumference = 2 * Math.PI * 70;
    const offset = circumference - (percentage / 100) * circumference;

    container.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding: 20px;">
            <!-- Circular progress -->
            <svg width="180" height="180" style="transform: rotate(-90deg);">
                <!-- Background circle -->
                <circle cx="90" cy="90" r="70" fill="none" stroke="rgba(200, 200, 200, 0.2)" stroke-width="12"/>
                <!-- Progress circle -->
                <circle cx="90" cy="90" r="70" fill="none" stroke="#10b981" stroke-width="12" 
                        stroke-dasharray="${circumference}" stroke-dashoffset="${offset}"
                        stroke-linecap="round"
                        style="transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1);"/>
            </svg>
            
            <!-- Center value -->
            <div style="position: absolute; text-align: center;">
                <div style="font-size: 32px; font-weight: bold; color: #10b981;">${value.toFixed(1)}</div>
                <div style="font-size: 14px; color: #999; margin-top: 5px;">${unit}</div>
            </div>
            
            <!-- Label -->
            <div style="margin-top: 20px; text-align: center;">
                <div style="font-size: 14px; color: #999;">${label}</div>
            </div>
        </div>
    `;
}

// Export animation functions
window.SensorAnimations = {
    temperature: renderTemperatureAnimation,
    ph: renderPHAnimation,
    humidity: renderHumidityAnimation,
    moisture: renderHumidityAnimation, // Same as humidity
    co2: renderCO2Animation,
    ec: renderECAnimation,
    tds: renderECAnimation, // Similar to EC
    generic: renderGenericAnimation
};
