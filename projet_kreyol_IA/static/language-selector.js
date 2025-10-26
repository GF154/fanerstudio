/**
 * 🌍 Language Selector Component
 * Konpozan pou chwazi lang
 */

class LanguageSelector {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            style: options.style || 'dropdown', // 'dropdown' or 'flags'
            position: options.position || 'top-right',
            ...options
        };
        
        this.render();
        this.attachEventListeners();
    }
    
    render() {
        if (!this.container) {
            console.error('Language selector container not found');
            return;
        }
        
        const languages = i18n.getAvailableLanguages();
        const currentLang = i18n.getLanguage();
        
        if (this.options.style === 'flags') {
            this.renderFlags(languages, currentLang);
        } else {
            this.renderDropdown(languages, currentLang);
        }
    }
    
    renderFlags(languages, currentLang) {
        const html = `
            <div class="language-selector language-flags">
                ${languages.map(lang => `
                    <button 
                        class="lang-flag ${lang.code === currentLang ? 'active' : ''}"
                        data-lang="${lang.code}"
                        title="${lang.name}"
                    >
                        ${lang.flag}
                    </button>
                `).join('')}
            </div>
        `;
        
        this.container.innerHTML = html;
        this.addFlagStyles();
    }
    
    renderDropdown(languages, currentLang) {
        const current = languages.find(l => l.code === currentLang);
        
        const html = `
            <div class="language-selector language-dropdown">
                <button class="lang-dropdown-button" id="lang-dropdown-btn">
                    <span class="lang-flag">${current.flag}</span>
                    <span class="lang-name">${current.name}</span>
                    <span class="lang-arrow">▼</span>
                </button>
                <div class="lang-dropdown-menu" id="lang-dropdown-menu">
                    ${languages.map(lang => `
                        <button 
                            class="lang-dropdown-item ${lang.code === currentLang ? 'active' : ''}"
                            data-lang="${lang.code}"
                        >
                            <span class="lang-flag">${lang.flag}</span>
                            <span class="lang-name">${lang.name}</span>
                            ${lang.code === currentLang ? '<span class="lang-check">✓</span>' : ''}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
        
        this.container.innerHTML = html;
        this.addDropdownStyles();
        this.setupDropdown();
    }
    
    setupDropdown() {
        const button = document.getElementById('lang-dropdown-btn');
        const menu = document.getElementById('lang-dropdown-menu');
        
        if (!button || !menu) return;
        
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('show');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            menu.classList.remove('show');
        });
    }
    
    attachEventListeners() {
        this.container.addEventListener('click', (e) => {
            const langButton = e.target.closest('[data-lang]');
            if (langButton) {
                const lang = langButton.getAttribute('data-lang');
                this.changeLanguage(lang);
            }
        });
    }
    
    changeLanguage(lang) {
        if (i18n.setLanguage(lang)) {
            this.render();
            
            // Show notification
            this.showNotification(`Language changed to ${i18n.getLanguageName(lang)}`);
        }
    }
    
    showNotification(message) {
        // Simple toast notification
        const toast = document.createElement('div');
        toast.className = 'lang-toast';
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    }
    
    addFlagStyles() {
        if (document.getElementById('lang-selector-flags-styles')) return;
        
        const style = document.createElement('style');
        style.id = 'lang-selector-flags-styles';
        style.textContent = `
            .language-flags {
                display: flex;
                gap: 8px;
            }
            
            .lang-flag {
                background: none;
                border: 2px solid transparent;
                font-size: 24px;
                cursor: pointer;
                padding: 4px 8px;
                border-radius: 6px;
                transition: all 0.2s;
            }
            
            .lang-flag:hover {
                border-color: #3b82f6;
                transform: scale(1.1);
            }
            
            .lang-flag.active {
                border-color: #3b82f6;
                background: rgba(59, 130, 246, 0.1);
            }
            
            .lang-toast {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #1a1a1a;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.3s;
                z-index: 10000;
            }
            
            .lang-toast.show {
                opacity: 1;
                transform: translateY(0);
            }
        `;
        document.head.appendChild(style);
    }
    
    addDropdownStyles() {
        if (document.getElementById('lang-selector-dropdown-styles')) return;
        
        const style = document.createElement('style');
        style.id = 'lang-selector-dropdown-styles';
        style.textContent = `
            .language-dropdown {
                position: relative;
            }
            
            .lang-dropdown-button {
                display: flex;
                align-items: center;
                gap: 8px;
                background: var(--bg-card, #1c1c1c);
                border: 1px solid var(--border-color, #2a2a2a);
                color: var(--text-primary, white);
                padding: 8px 16px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
                font-size: 14px;
            }
            
            .lang-dropdown-button:hover {
                background: var(--bg-hover, #252525);
            }
            
            .lang-flag {
                font-size: 18px;
            }
            
            .lang-arrow {
                font-size: 10px;
                transition: transform 0.2s;
            }
            
            .lang-dropdown-button:hover .lang-arrow {
                transform: translateY(2px);
            }
            
            .lang-dropdown-menu {
                position: absolute;
                top: calc(100% + 8px);
                right: 0;
                background: var(--bg-card, #1c1c1c);
                border: 1px solid var(--border-color, #2a2a2a);
                border-radius: 8px;
                padding: 8px;
                min-width: 200px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.4);
                opacity: 0;
                visibility: hidden;
                transform: translateY(-10px);
                transition: all 0.2s;
                z-index: 1000;
            }
            
            .lang-dropdown-menu.show {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
            }
            
            .lang-dropdown-item {
                display: flex;
                align-items: center;
                gap: 12px;
                width: 100%;
                background: none;
                border: none;
                color: var(--text-primary, white);
                padding: 10px 12px;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s;
                text-align: left;
                font-size: 14px;
            }
            
            .lang-dropdown-item:hover {
                background: var(--bg-hover, #252525);
            }
            
            .lang-dropdown-item.active {
                background: rgba(59, 130, 246, 0.1);
                color: #3b82f6;
            }
            
            .lang-check {
                margin-left: auto;
                color: #3b82f6;
                font-weight: bold;
            }
            
            .lang-toast {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #1a1a1a;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.3s;
                z-index: 10000;
            }
            
            .lang-toast.show {
                opacity: 1;
                transform: translateY(0);
            }
        `;
        document.head.appendChild(style);
    }
}

// Auto-initialize if container exists
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('language-selector');
    if (container) {
        new LanguageSelector('language-selector', {
            style: 'dropdown',
            position: 'top-right'
        });
    }
});

