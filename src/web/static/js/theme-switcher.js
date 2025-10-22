/**
 * MGB - Mushroom Grow Box
 * Theme Switcher System
 */

class ThemeSwitcher {
    constructor() {
        this.currentTheme = this.loadTheme();
        this.themes = {
            dark: {
                name: 'Dark',
                icon: '🌙',
                cssFile: '/static/css/theme-dark.css'
            },
            psychedelic: {
                name: 'Psychedelic',
                icon: '🌈',
                cssFile: '/static/css/theme-psychedelic.css'
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
     * Setup theme switcher UI
     */
    setupThemeSwitcher() {
        const header = document.querySelector('header');
        if (!header) return;

        // Create theme switcher container
        const themeSwitcher = document.createElement('div');
        themeSwitcher.className = 'theme-switcher';
        themeSwitcher.innerHTML = `
            <button class="theme-btn" id="themeBtn">
                <span class="theme-icon">${this.themes[this.currentTheme].icon}</span>
                <span class="theme-name">${this.themes[this.currentTheme].name}</span>
            </button>
            <div class="theme-dropdown" id="themeDropdown" style="display: none;">
                ${Object.entries(this.themes).map(([key, info]) => `
                    <button class="theme-option" data-theme="${key}">
                        <span class="theme-icon">${info.icon}</span>
                        <span class="theme-name">${info.name}</span>
                    </button>
                `).join('')}
            </div>
        `;

        // Find or create controls container
        let controlsContainer = header.querySelector('.header-controls');
        if (!controlsContainer) {
            controlsContainer = document.createElement('div');
            controlsContainer.className = 'header-controls';
            header.appendChild(controlsContainer);
        }
        
        controlsContainer.insertBefore(themeSwitcher, controlsContainer.firstChild);

        // Add event listeners
        const themeBtn = document.getElementById('themeBtn');
        const themeDropdown = document.getElementById('themeDropdown');

        themeBtn.addEventListener('click', () => {
            themeDropdown.style.display = themeDropdown.style.display === 'none' ? 'block' : 'none';
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!themeSwitcher.contains(e.target)) {
                themeDropdown.style.display = 'none';
            }
        });

        // Theme selection
        themeSwitcher.querySelectorAll('.theme-option').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const theme = btn.getAttribute('data-theme');
                this.changeTheme(theme);
                themeDropdown.style.display = 'none';
            });
        });
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
