import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import { useLang, LANGUAGES } from '../../context/LanguageContext';

function NavLink({ to, children }) {
  const { pathname } = useLocation();
  const active = pathname === to;
  return (
    <Link
      to={to}
      className={`hover:text-white transition-colors ${active ? 'text-white font-semibold underline underline-offset-4' : 'text-blue-100'}`}
    >
      {children}
    </Link>
  );
}

export default function Header() {
  const { t } = useTranslation();
  const { isAuthenticated, isAdmin, user, logout } = useAuth();
  const { lang, setLang } = useLang();
  const navigate = useNavigate();

  const handleLogout = () => { logout(); navigate('/'); };

  return (
    <header className="bg-blue-700 text-white shadow-lg">
      {/* Top bar — logo, language, auth */}
      <div className="max-w-6xl mx-auto px-4 pt-3 pb-1 flex items-center justify-between gap-4">
        <Link to="/" className="text-2xl font-bold tracking-tight hover:text-blue-100 flex-shrink-0">
          HappySR
        </Link>

        <div className="flex items-center gap-3">
          <select
            value={lang}
            onChange={(e) => setLang(e.target.value)}
            aria-label="Select language"
            className="bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold px-3 py-1.5 rounded-full border border-blue-400 focus:outline-none focus:ring-2 focus:ring-white cursor-pointer transition-colors"
          >
            {LANGUAGES.map((l) => (
              <option key={l.code} value={l.code} className="bg-gray-800 text-white">
                {l.label}
              </option>
            ))}
          </select>

          {isAuthenticated ? (
            <div className="flex items-center gap-3">
              <Link to="/profile" className="hidden md:block text-sm text-blue-100 hover:text-white font-medium truncate max-w-[140px]">
                {user?.name || user?.email}
              </Link>
              <button
                onClick={handleLogout}
                className="bg-white text-blue-700 hover:bg-blue-50 px-4 py-1.5 rounded-lg text-sm font-semibold transition-colors"
              >
                {t('nav.logout')}
              </button>
            </div>
          ) : (
            <div className="flex gap-2">
              <Link to="/login" className="bg-white text-blue-700 hover:bg-blue-50 px-4 py-1.5 rounded-lg text-sm font-semibold transition-colors">
                {t('nav.login')}
              </Link>
              <Link to="/register" className="border border-white hover:bg-blue-600 px-4 py-1.5 rounded-lg text-sm font-semibold transition-colors">
                {t('nav.register')}
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Nav bar — all section links */}
      <nav className="hidden md:block border-t border-blue-600">
        <div className="max-w-6xl mx-auto px-4 py-2 flex items-center gap-6 text-base font-medium flex-wrap">
          <NavLink to="/">{t('nav.home')}</NavLink>
          <NavLink to="/calendar">{t('nav.calendar')}</NavLink>
          <NavLink to="/activities">{t('nav.activities')}</NavLink>
          <NavLink to="/learning">{t('nav.learning')}</NavLink>
          <NavLink to="/health">{t('nav.health')}</NavLink>
          <NavLink to="/technology">{t('nav.technology')}</NavLink>
          <NavLink to="/travel">{t('nav.travel')}</NavLink>
          <NavLink to="/finance">{t('nav.finance')}</NavLink>
          {isAuthenticated && (
            <>
              <span className="text-blue-500 select-none">|</span>
              <NavLink to="/expenses">{t('nav.expenses')}</NavLink>
              <NavLink to="/investments">{t('nav.investments')}</NavLink>
              <NavLink to="/reports">{t('nav.reports')}</NavLink>
            </>
          )}
          {isAdmin && (
            <>
              <span className="text-blue-500 select-none">|</span>
              <NavLink to="/admin/users">{t('nav.admin')}</NavLink>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
