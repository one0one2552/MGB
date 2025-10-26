/**
 * MGB - Mushroom Grow Box
 * Theme Switcher System
 */

class ThemeSwitcher {
    constructor() {
        this.currentTheme = 'dark'; // Nur Dark Theme
        this.themes = {
            dark: {
                name: 'Dark',
                icon: '🌙',
                cssFile: '/static/css/theme-dark.css'
            }
        };
        this.init();
    }

    /**
     * Initialize theme switcher
     */
    init() {
        this.applyTheme(this.currentTheme);
        this.setupThemeSwitcher();
    }

    /**
     * Apply theme by loading the appropriate CSS file
     */
    applyTheme(themeName) {
        // Remove existing theme link
        const existingThemeLink = document.getElementById('theme-css');
        if (existingThemeLink) {
            existingThemeLink.remove();
        }

        // Add new theme link
        const theme = this.themes[themeName];
        if (theme) {
            const link = document.createElement('link');
            link.id = 'theme-css';
            link.rel = 'stylesheet';
            link.href = theme.cssFile;
            document.head.appendChild(link);

            this.currentTheme = themeName;
            this.saveTheme(themeName);

            // Emit custom event
            window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: themeName } }));
        }
    }

    /**
     * Setup theme switcher UI - Deaktiviert, da nur Dark Theme verfügbar
     */
    setupThemeSwitcher() {
        // Theme-Switcher nicht mehr benötigt - nur Dark Theme
        return;
    }

    /**
     * Change theme
     */
    changeTheme(themeName) {
        if (this.themes[themeName]) {
            this.applyTheme(themeName);
            this.updateThemeSwitcher();
        }
    }

    /**
     * Update theme switcher button
     */
    updateThemeSwitcher() {
        const themeBtn = document.getElementById('themeBtn');
        if (themeBtn && this.themes[this.currentTheme]) {
            const icon = themeBtn.querySelector('.theme-icon');
            const name = themeBtn.querySelector('.theme-name');
            icon.textContent = this.themes[this.currentTheme].icon;
            name.textContent = this.themes[this.currentTheme].name;
        }
    }

    /**
     * Load theme preference from localStorage
     */
    loadTheme() {
        return localStorage.getItem('mgb-theme') || 'dark';
    }

    /**
     * Save theme preference to localStorage
     */
    saveTheme(theme) {
        localStorage.setItem('mgb-theme', theme);
    }
}

// Initialize theme switcher when DOM is ready
let themeSwitcherInstance;
document.addEventListener('DOMContentLoaded', () => {
    themeSwitcherInstance = new ThemeSwitcher();
});

// Export for use in other scripts
window.themeSwitcher = {
    getInstance: () => themeSwitcherInstance,
    changeTheme: (theme) => themeSwitcherInstance ? themeSwitcherInstance.changeTheme(theme) : null
};
