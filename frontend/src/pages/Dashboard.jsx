import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import api from '../utils/api';
import Card from '../components/common/Card';

export default function Dashboard() {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [summary, setSummary] = useState({ expenses: null, activities: null, investments: null });

  useEffect(() => {
    Promise.all([
      api.get('/expenses'),
      api.get('/activities'),
      api.get('/investments'),
    ]).then(([e, a, i]) => {
      const total = e.data.data.reduce((s, x) => s + parseFloat(x.amount), 0);
      setSummary({ expenses: total.toFixed(2), activities: a.data.data.length, investments: i.data.data.length });
    }).catch(() => {});
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{t('nav.dashboard')}</h1>
          {user?.name && <p className="text-xl text-gray-500 mt-1">Welcome back, {user.name}</p>}
        </div>
        <Link
          to="/profile"
          className="bg-blue-700 hover:bg-blue-600 text-white font-semibold px-5 py-2.5 rounded-lg text-lg transition-colors"
        >
          {t('nav.profile')} →
        </Link>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-8">
        {[
          { label: 'Total Expenses',       value: summary.expenses    !== null ? `$${summary.expenses}` : '—', color: 'text-red-600',   icon: '💰', to: '/expenses' },
          { label: 'Upcoming Activities',  value: summary.activities  ?? '—',                                  color: 'text-blue-600',  icon: '🎉', to: '/activities' },
          { label: 'Investments Tracked',  value: summary.investments ?? '—',                                  color: 'text-green-600', icon: '📈', to: '/investments' },
        ].map((s) => (
          <Link to={s.to} key={s.label}>
            <Card className="text-center hover:shadow-md transition-shadow cursor-pointer">
              <span className="text-4xl">{s.icon}</span>
              <p className={`text-3xl font-bold ${s.color} mt-2 mb-1`}>{s.value}</p>
              <p className="text-gray-600 text-lg">{s.label}</p>
            </Card>
          </Link>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-5">
        {[
          { to: '/expenses',    icon: '💰', label: 'Expense Tracker',    desc: 'Log and track your daily expenses.' },
          { to: '/investments', icon: '📈', label: 'Investment Tracker',  desc: 'Monitor your investment portfolio.' },
          { to: '/reports',     icon: '📊', label: 'Expense Reports',     desc: 'View charts and spending summaries.' },
          { to: '/calendar',    icon: '📅', label: 'Events Calendar',     desc: 'Browse upcoming community events.' },
        ].map((item) => (
          <Link to={item.to} key={item.to}>
            <Card className="flex items-start gap-4 hover:shadow-md transition-shadow cursor-pointer">
              <span className="text-3xl">{item.icon}</span>
              <div>
                <h3 className="text-xl font-semibold text-gray-900">{item.label}</h3>
                <p className="text-gray-500 text-lg">{item.desc}</p>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
