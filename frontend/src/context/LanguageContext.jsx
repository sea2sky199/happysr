import { createContext, useContext, useState } from 'react';
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from '../i18n/en.json';
import es from '../i18n/es.json';
import zhCN from '../i18n/zh-CN.json';
import zhTW from '../i18n/zh-TW.json';
import vi from '../i18n/vi.json';
import ko from '../i18n/ko.json';

export const LANGUAGES = [
  { code: 'en',    label: 'English' },
  { code: 'es',    label: 'Español' },
  { code: 'zh-CN', label: '简体中文' },
  { code: 'zh-TW', label: '繁體中文' },
  { code: 'vi',    label: 'Tiếng Việt' },
  { code: 'ko',    label: '한국어' },
];

i18n.use(initReactI18next).init({
  resources: {
    en:    { translation: en },
    es:    { translation: es },
    'zh-CN': { translation: zhCN },
    'zh-TW': { translation: zhTW },
    vi:    { translation: vi },
    ko:    { translation: ko },
  },
  lng: localStorage.getItem('lang') || 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

const LanguageContext = createContext(null);

export function LanguageProvider({ children }) {
  const [lang, setLangState] = useState(localStorage.getItem('lang') || 'en');

  const setLang = (l) => {
    i18n.changeLanguage(l);
    localStorage.setItem('lang', l);
    setLangState(l);
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, languages: LANGUAGES }}>
      {children}
    </LanguageContext.Provider>
  );
}

export const useLang = () => useContext(LanguageContext);
