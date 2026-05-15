import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';

function NavItem({ to, label, icon, onClick }) {
  const { pathname } = useLocation();
  const active = pathname === to;
  const cls = `flex flex-col items-center gap-0.5 text-xs font-medium px-2 py-1 rounded-lg transition-colors ${
    active ? 'text-blue-700' : 'text-gray-500 hover:text-blue-600'
  }`;
  if (onClick) return <button onClick={onClick} className={cls}><span className="text-2xl">{icon}</span>{label}</button>;
  return <Link to={to} className={cls}><span className="text-2xl">{icon}</span>{label}</Link>;
}

const MORE_LINKS = [
  { to: '/calendar',   icon: '📅',  key: 'calendar' },
  { to: '/travel',     icon: '✈️',  key: 'travel' },
  { to: '/finance',    icon: '💼',  key: 'finance' },
  { to: '/technology', icon: '💻',  key: 'technology' },
  { to: '/learning',   icon: '🎓',  key: 'learning' },
];

export default function MobileNav() {
  const { t } = useTranslation();
  const { isAuthenticated } = useAuth();
  const [showMore, setShowMore] = useState(false);
  const navigate = useNavigate();

  const handleMoreLink = (to) => { setShowMore(false); navigate(to); };

  return (
    <>
      {/* More drawer */}
      {showMore && (
        <div className="md:hidden fixed inset-0 z-40" onClick={() => setShowMore(false)}>
          <div
            className="absolute bottom-16 left-0 right-0 bg-white border-t border-gray-200 shadow-xl px-4 py-3 grid grid-cols-4 gap-2"
            onClick={(e) => e.stopPropagation()}
          >
            {MORE_LINKS.map((l) => (
              <button
                key={l.to}
                onClick={() => handleMoreLink(l.to)}
                className="flex flex-col items-center gap-1 py-2 px-1 rounded-xl text-gray-600 hover:bg-blue-50 hover:text-blue-700 transition-colors"
              >
                <span className="text-2xl">{l.icon}</span>
                <span className="text-xs font-medium">{t(`nav.${l.key}`)}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 flex justify-around items-center py-2 px-2 z-50 shadow-lg">
        <NavItem to="/"           label={t('nav.home')}       icon="🏠" />
        <NavItem to="/health"     label={t('nav.health')}     icon="❤️" />
        <NavItem to="/activities" label={t('nav.activities')} icon="🎉" />
        {isAuthenticated ? (
          <>
            <NavItem to="/expenses"  label={t('nav.expenses')}  icon="💰" />
            <NavItem to="/dashboard" label={t('nav.dashboard')} icon="👤" />
          </>
        ) : (
          <NavItem to="/login" label={t('nav.login')} icon="🔑" />
        )}
        <NavItem
          label={t('nav.more', 'More')}
          icon="⋯"
          onClick={() => setShowMore((v) => !v)}
        />
      </nav>
    </>
  );
}
