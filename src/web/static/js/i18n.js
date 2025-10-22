/**
 * MGB - Mushroom Grow Box
 * Internationalization (i18n) System
 */

class I18n {
    constructor() {
        this.currentLanguage = this.loadLanguage();
        this.translations = {};
        this.availableLanguages = {};
        this.init();
    }

    /**
     * Initialize i18n system
     */
    async init() {
        await this.loadAvailableLanguages();
        await this.loadTranslations(this.currentLanguage);
        this.applyTranslations();
        this.setupLanguageSwitcher();
    }

    /**
     * Load available languages from API
     */
    async loadAvailableLanguages() {
        try {
            const response = await fetch('/api/languages');
            this.availableLanguages = await response.json();
        } catch (error) {
            console.error('Error loading languages:', error);
        }
    }

    /**
     * Load translations for a specific language
     */
    async loadTranslations(lang) {
        try {
            const response = await fetch(`/api/translations/${lang}`);
            this.translations = await response.json();
            this.currentLanguage = lang;
            this.saveLanguage(lang);
        } catch (error) {
            console.error('Error loading translations:', error);
        }
    }

    /**
     * Apply translations to all elements with data-i18n attribute
     */
    applyTranslations() {
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (this.translations[key]) {
                // Check if element is input placeholder
                if (element.hasAttribute('data-i18n-placeholder')) {
                    element.placeholder = this.translations[key];
                } else {
                    element.textContent = this.translations[key];
                }
            }
        });
    }

    /**
     * Get translation by key
     */
    t(key) {
        return this.translations[key] || key;
    }

    /**
     * Change language
     */
    async changeLanguage(lang) {
        await this.loadTranslations(lang);
        this.applyTranslations();
        
        // Update language switcher
        this.updateLanguageSwitcher();
        
        // Emit custom event for other components
        window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
    }

    /**
     * Setup language switcher UI
     */
    setupLanguageSwitcher() {
        const header = document.querySelector('header');
        if (!header) return;

        // Create language switcher container
        const langSwitcher = document.createElement('div');
        langSwitcher.className = 'language-switcher';
        langSwitcher.innerHTML = `
            <button class="lang-btn" id="langBtn">
                <span class="lang-flag">${this.availableLanguages[this.currentLanguage]?.flag || '🌐'}</span>
                <span class="lang-name">${this.availableLanguages[this.currentLanguage]?.name || this.currentLanguage.toUpperCase()}</span>
            </button>
            <div class="lang-dropdown" id="langDropdown" style="display: none;">
                ${Object.entries(this.availableLanguages).map(([code, info]) => `
                    <button class="lang-option" data-lang="${code}">
                        <span class="lang-flag">${info.flag}</span>
                        <span class="lang-name">${info.name}</span>
                    </button>
                `).join('')}
            </div>
        `;

        // Find status indicator or create controls container
        let controlsContainer = header.querySelector('.header-controls');
        if (!controlsContainer) {
            controlsContainer = document.createElement('div');
            controlsContainer.className = 'header-controls';
            header.appendChild(controlsContainer);
        }
        
        controlsContainer.appendChild(langSwitcher);

        // Add event listeners
        const langBtn = document.getElementById('langBtn');
        const langDropdown = document.getElementById('langDropdown');

        langBtn.addEventListener('click', () => {
            langDropdown.style.display = langDropdown.style.display === 'none' ? 'block' : 'none';
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!langSwitcher.contains(e.target)) {
                langDropdown.style.display = 'none';
            }
        });

        // Language selection
        langSwitcher.querySelectorAll('.lang-option').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const lang = btn.getAttribute('data-lang');
                this.changeLanguage(lang);
                langDropdown.style.display = 'none';
            });
        });
    }

    /**
     * Update language switcher button
     */
    updateLanguageSwitcher() {
        const langBtn = document.getElementById('langBtn');
        if (langBtn && this.availableLanguages[this.currentLanguage]) {
            const flag = langBtn.querySelector('.lang-flag');
            const name = langBtn.querySelector('.lang-name');
            flag.textContent = this.availableLanguages[this.currentLanguage].flag;
            name.textContent = this.availableLanguages[this.currentLanguage].name;
        }
    }

    /**
     * Load language preference from localStorage
     */
    loadLanguage() {
        return localStorage.getItem('mgb-language') || 'de';
    }

    /**
     * Save language preference to localStorage
     */
    saveLanguage(lang) {
        localStorage.setItem('mgb-language', lang);
    }
}

// Initialize i18n when DOM is ready
let i18nInstance;
document.addEventListener('DOMContentLoaded', () => {
    i18nInstance = new I18n();
});

// Export for use in other scripts
window.i18n = {
    getInstance: () => i18nInstance,
    t: (key) => i18nInstance ? i18nInstance.t(key) : key
};
