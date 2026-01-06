/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                agri: {
                    primary: '#2d5016',    // Deep green
                    secondary: '#8b6914',  // Earth brown
                    accent: '#27ae60',     // Leaf green
                    alert: '#e74c3c',      // Red for alerts
                    warning: '#f39c12',    // Orange for warnings
                    success: '#27ae60',    // Green for success
                    light: '#ecf0f1',      // Light gray
                    bg: '#f5f7f6'          // Background
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
