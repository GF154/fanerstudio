/**
 * 🌍 Internationalization (i18n) System
 * Sistèm entènasyonalizasyon pou Kreyòl IA
 */

const translations = {
    // Haitian Creole
    ht: {
        // Navigation
        'nav.home': 'Akèy',
        'nav.voices': 'Vwa',
        'nav.text_to_speech': 'Tèks an Paròl',
        'nav.voice_changer': 'Chanje Vwa',
        'nav.sound_effects': 'Efè Son',
        'nav.voice_isolator': 'Izole Vwa',
        'nav.studio': 'Estidyo',
        'nav.music': 'Mizik',
        'nav.dubbing': 'Doublaj',
        'nav.speech_to_text': 'Paròl an Tèks',
        'nav.audio_native': 'Odyo Natif',
        
        // Page titles
        'page.studio': 'Estidyo',
        'page.welcome': 'Byenvini',
        
        // Buttons
        'btn.upload': 'Telechaje',
        'btn.new_project': 'Nouvo pwojè vid',
        'btn.create': 'Kreye',
        'btn.download': 'Telechaje',
        'btn.cancel': 'Anile',
        'btn.save': 'Sove',
        'btn.back': 'Retounen',
        
        // Audio section
        'audio.title': 'Odyo',
        'audio.new_audiobook': 'Nouvo liv odyo',
        'audio.new_audiobook_desc': 'Kòmanse de zewo oswa enpòte fichye',
        'audio.create_podcast': 'Kreye yon podcast',
        'audio.create_podcast_desc': 'Jenere otomatikman podcast soti nan dokiman',
        'audio.url_to_audio': 'URL an odyo',
        'audio.url_to_audio_desc': 'Kreye vwadeyò soti nan nenpòt paj wèb',
        'audio.ai_script': 'Jeneratè Skrip IA',
        'audio.ai_script_desc': 'Jenere yon skrip soti nan yon pwonp',
        
        // Video section
        'video.title': 'Videyo',
        'video.new_voiceover': 'Nouvo vwadeyò videyo',
        'video.new_voiceover_desc': 'Ajoute paròl nan videyo ou yo',
        'video.add_sfx': 'Ajoute efè son ak mizik',
        'video.add_sfx_desc': 'Ajoute vwadeyò, mizik, ak efè son',
        'video.add_captions': 'Ajoute soutit',
        'video.add_captions_desc': 'Soutit otomatik pou videyo ou',
        'video.remove_noise': 'Retire bri background',
        'video.remove_noise_desc': 'Netwaye videyo ki gen bri',
        'video.fix_voiceover': 'Korije erè vwadeyò',
        'video.fix_voiceover_desc': 'Korije erè ak kòreksyon paròl',
        'video.ai_soundtrack': 'Jeneratè Mizik IA',
        'video.ai_soundtrack_desc': 'Jenere mizik pou videyo ou otomatikman',
        
        // Common
        'common.loading': 'Chaje...',
        'common.error': 'Erè',
        'common.success': 'Siksè',
        'common.search': 'Chèche',
        'common.recent_projects': 'Pwojè Resan',
        'common.no_projects': 'Poko gen pwojè. Kreye premye pwojè w anwo a!',
        'common.creative_tools': 'Zouti Kreyatif',
        'common.products': 'Pwodui',
        'common.new': 'Nouvo',
        
        // Form labels
        'form.text': 'Tèks',
        'form.voice': 'Vwa',
        'form.language': 'Lang',
        'form.file': 'Fichye',
        'form.title': 'Tit',
        'form.description': 'Deskripsyon',
        
        // Messages
        'msg.upload_success': 'Fichye telechaje avèk siksè!',
        'msg.processing': 'Ap pwosese...',
        'msg.complete': 'Konplete!',
        'msg.error_occurred': 'Yon erè rive',
    },
    
    // English
    en: {
        // Navigation
        'nav.home': 'Home',
        'nav.voices': 'Voices',
        'nav.text_to_speech': 'Text to Speech',
        'nav.voice_changer': 'Voice Changer',
        'nav.sound_effects': 'Sound Effects',
        'nav.voice_isolator': 'Voice Isolator',
        'nav.studio': 'Studio',
        'nav.music': 'Music',
        'nav.dubbing': 'Dubbing',
        'nav.speech_to_text': 'Speech to Text',
        'nav.audio_native': 'Audio Native',
        
        // Page titles
        'page.studio': 'Studio',
        'page.welcome': 'Welcome',
        
        // Buttons
        'btn.upload': 'Upload',
        'btn.new_project': 'New Empty Project',
        'btn.create': 'Create',
        'btn.download': 'Download',
        'btn.cancel': 'Cancel',
        'btn.save': 'Save',
        'btn.back': 'Back',
        
        // Audio section
        'audio.title': 'Audio',
        'audio.new_audiobook': 'New Audiobook',
        'audio.new_audiobook_desc': 'Start from scratch or import file',
        'audio.create_podcast': 'Create a Podcast',
        'audio.create_podcast_desc': 'Generate podcast automatically from document',
        'audio.url_to_audio': 'URL to Audio',
        'audio.url_to_audio_desc': 'Create voiceover from any web page',
        'audio.ai_script': 'AI Script Generator',
        'audio.ai_script_desc': 'Generate a script from a prompt',
        
        // Video section
        'video.title': 'Video',
        'video.new_voiceover': 'New Video Voiceover',
        'video.new_voiceover_desc': 'Add voice to your videos',
        'video.add_sfx': 'Add SFX and Music',
        'video.add_sfx_desc': 'Add voiceover, music, and sound effects',
        'video.add_captions': 'Add Captions',
        'video.add_captions_desc': 'Automatic captions for your video',
        'video.remove_noise': 'Remove Background Noise',
        'video.remove_noise_desc': 'Clean noisy videos',
        'video.fix_voiceover': 'Fix Voiceover Errors',
        'video.fix_voiceover_desc': 'Fix errors with speech correction',
        'video.ai_soundtrack': 'AI Soundtrack Generator',
        'video.ai_soundtrack_desc': 'Generate music for your video automatically',
        
        // Common
        'common.loading': 'Loading...',
        'common.error': 'Error',
        'common.success': 'Success',
        'common.search': 'Search',
        'common.recent_projects': 'Recent Projects',
        'common.no_projects': 'No projects yet. Create your first project above!',
        'common.creative_tools': 'Creative Tools',
        'common.products': 'Products',
        'common.new': 'New',
        
        // Form labels
        'form.text': 'Text',
        'form.voice': 'Voice',
        'form.language': 'Language',
        'form.file': 'File',
        'form.title': 'Title',
        'form.description': 'Description',
        
        // Messages
        'msg.upload_success': 'File uploaded successfully!',
        'msg.processing': 'Processing...',
        'msg.complete': 'Complete!',
        'msg.error_occurred': 'An error occurred',
    },
    
    // French
    fr: {
        // Navigation
        'nav.home': 'Accueil',
        'nav.voices': 'Voix',
        'nav.text_to_speech': 'Texte vers Parole',
        'nav.voice_changer': 'Changeur de Voix',
        'nav.sound_effects': 'Effets Sonores',
        'nav.voice_isolator': 'Isolateur de Voix',
        'nav.studio': 'Studio',
        'nav.music': 'Musique',
        'nav.dubbing': 'Doublage',
        'nav.speech_to_text': 'Parole vers Texte',
        'nav.audio_native': 'Audio Natif',
        
        // Page titles
        'page.studio': 'Studio',
        'page.welcome': 'Bienvenue',
        
        // Buttons
        'btn.upload': 'Télécharger',
        'btn.new_project': 'Nouveau Projet Vide',
        'btn.create': 'Créer',
        'btn.download': 'Télécharger',
        'btn.cancel': 'Annuler',
        'btn.save': 'Sauvegarder',
        'btn.back': 'Retour',
        
        // Audio section
        'audio.title': 'Audio',
        'audio.new_audiobook': 'Nouveau Livre Audio',
        'audio.new_audiobook_desc': 'Commencer de zéro ou importer un fichier',
        'audio.create_podcast': 'Créer un Podcast',
        'audio.create_podcast_desc': 'Générer automatiquement podcast depuis document',
        'audio.url_to_audio': 'URL vers Audio',
        'audio.url_to_audio_desc': 'Créer voix off depuis n\'importe quelle page web',
        'audio.ai_script': 'Générateur de Script IA',
        'audio.ai_script_desc': 'Générer un script depuis un prompt',
        
        // Video section
        'video.title': 'Vidéo',
        'video.new_voiceover': 'Nouvelle Voix Off Vidéo',
        'video.new_voiceover_desc': 'Ajouter une voix à vos vidéos',
        'video.add_sfx': 'Ajouter Effets et Musique',
        'video.add_sfx_desc': 'Ajouter voix off, musique et effets sonores',
        'video.add_captions': 'Ajouter Sous-titres',
        'video.add_captions_desc': 'Sous-titres automatiques pour votre vidéo',
        'video.remove_noise': 'Supprimer Bruit de Fond',
        'video.remove_noise_desc': 'Nettoyer vidéos bruyantes',
        'video.fix_voiceover': 'Corriger Erreurs Voix Off',
        'video.fix_voiceover_desc': 'Corriger erreurs avec correction vocale',
        'video.ai_soundtrack': 'Générateur Bande Son IA',
        'video.ai_soundtrack_desc': 'Générer musique pour votre vidéo automatiquement',
        
        // Common
        'common.loading': 'Chargement...',
        'common.error': 'Erreur',
        'common.success': 'Succès',
        'common.search': 'Rechercher',
        'common.recent_projects': 'Projets Récents',
        'common.no_projects': 'Pas encore de projets. Créez votre premier projet ci-dessus!',
        'common.creative_tools': 'Outils Créatifs',
        'common.products': 'Produits',
        'common.new': 'Nouveau',
        
        // Form labels
        'form.text': 'Texte',
        'form.voice': 'Voix',
        'form.language': 'Langue',
        'form.file': 'Fichier',
        'form.title': 'Titre',
        'form.description': 'Description',
        
        // Messages
        'msg.upload_success': 'Fichier téléchargé avec succès!',
        'msg.processing': 'Traitement en cours...',
        'msg.complete': 'Terminé!',
        'msg.error_occurred': 'Une erreur s\'est produite',
    }
};

/**
 * i18n Manager Class
 */
class I18nManager {
    constructor(defaultLang = 'ht') {
        this.currentLang = this.detectLanguage() || defaultLang;
        this.translations = translations;
        this.loadFromLocalStorage();
    }
    
    /**
     * Detect user's preferred language
     */
    detectLanguage() {
        // Check localStorage first
        const saved = localStorage.getItem('kreyol_ia_lang');
        if (saved && this.translations[saved]) {
            return saved;
        }
        
        // Check browser language
        const browserLang = navigator.language || navigator.userLanguage;
        const lang = browserLang.split('-')[0]; // 'en-US' -> 'en'
        
        if (this.translations[lang]) {
            return lang;
        }
        
        return 'ht'; // Default to Haitian Creole
    }
    
    /**
     * Load language preference from localStorage
     */
    loadFromLocalStorage() {
        const saved = localStorage.getItem('kreyol_ia_lang');
        if (saved && this.translations[saved]) {
            this.currentLang = saved;
        }
    }
    
    /**
     * Save language preference to localStorage
     */
    saveToLocalStorage() {
        localStorage.setItem('kreyol_ia_lang', this.currentLang);
    }
    
    /**
     * Get translation for a key
     */
    t(key) {
        const translation = this.translations[this.currentLang]?.[key];
        if (translation) {
            return translation;
        }
        
        // Fallback to English if translation not found
        const fallback = this.translations['en']?.[key];
        if (fallback) {
            return fallback;
        }
        
        // Return key if no translation found
        console.warn(`Translation missing for key: ${key}`);
        return key;
    }
    
    /**
     * Change current language
     */
    setLanguage(lang) {
        if (!this.translations[lang]) {
            console.error(`Language not supported: ${lang}`);
            return false;
        }
        
        this.currentLang = lang;
        this.saveToLocalStorage();
        this.updatePage();
        return true;
    }
    
    /**
     * Get current language
     */
    getLanguage() {
        return this.currentLang;
    }
    
    /**
     * Get available languages
     */
    getAvailableLanguages() {
        return Object.keys(this.translations).map(code => ({
            code: code,
            name: this.getLanguageName(code),
            flag: this.getLanguageFlag(code)
        }));
    }
    
    /**
     * Get language name
     */
    getLanguageName(code) {
        const names = {
            'ht': 'Kreyòl Ayisyen',
            'en': 'English',
            'fr': 'Français'
        };
        return names[code] || code;
    }
    
    /**
     * Get language flag emoji
     */
    getLanguageFlag(code) {
        const flags = {
            'ht': '🇭🇹',
            'en': '🇺🇸',
            'fr': '🇫🇷'
        };
        return flags[code] || '🌍';
    }
    
    /**
     * Update all translatable elements on the page
     */
    updatePage() {
        // Update elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            element.textContent = this.t(key);
        });
        
        // Update elements with data-i18n-placeholder attribute
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.t(key);
        });
        
        // Update elements with data-i18n-title attribute
        document.querySelectorAll('[data-i18n-title]').forEach(element => {
            const key = element.getAttribute('data-i18n-title');
            element.title = this.t(key);
        });
        
        // Update page language attribute
        document.documentElement.lang = this.currentLang;
        
        // Dispatch event for other components
        window.dispatchEvent(new CustomEvent('languageChanged', {
            detail: { language: this.currentLang }
        }));
    }
}

// Global instance
const i18n = new I18nManager();

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    i18n.updatePage();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { I18nManager, i18n, translations };
}

