// AdmitAI Configuration File
// Copy this file to config.local.js and update with your actual API keys

const config = {
    // Gemini AI API Configuration
    gemini: {
        apiKey: 'AIzaSyC-2jr4RlBvKWW8sdjdGjJBQ1ujHR-D2Xs', // Get from https://makersuite.google.com/app/apikey
        apiUrl: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
        enabled: true // Set to false to disable AI features
    },
    
    // Application Settings
    app: {
        name: 'AdmitAI',
        version: '1.0.0',
        defaultLanguage: 'en',
        supportedLanguages: ['en', 'hi', 'mr'],
        debug: false // Set to true for development
    },
    
    // College Data Settings
    colleges: {
        enableRealTimeUpdates: true,
        cacheTimeout: 3600000, // 1 hour in milliseconds
        maxCollegesPerRequest: 50
    },
    
    // UI Settings
    ui: {
        theme: 'light', // 'light' or 'dark'
        animations: true,
        showAIStatus: true
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = config;
} else {
    // For browser usage
    window.AdmitAIConfig = config;
} 