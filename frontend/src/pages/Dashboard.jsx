import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { LANGUAGES } from '../context/LanguageContext';
import api from '../utils/api';
import Card from '../components/common/Card';
import Button from '../components/common/Button';

const genderOptions = ['male', 'female', 'other', 'prefer_not_to_say'];

export default function Dashboard() {
  const { t } = useTranslation();
  const { user, refreshUser } = useAuth();
  const [profile, setProfile] = useState({ name: '', gender: '', age: '', zipcode: '', language_pref: 'en' });
  const [summary, setSummary] = useState({ expenses: null, activities: null, investments: null });
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (user) setProfile({ name: user.name || '', gender: user.gender || '', age: user.age || '', zipcode: user.zipcode || '', language_pref: user.language_pref || 'en' });
    Promise.all([
      api.get('/expenses'),
      api.get('/activities'),
      api.get('/investments'),
    ]).then(([e, a, i]) => {
      const total = e.data.data.reduce((s, x) => s + parseFloat(x.amount), 0);
      setSummary({ expenses: total.toFixed(2), activities: a.data.data.length, investments: i.data.data.length });
    }).catch(() => {});
  }, [user]);

  const handleSave = async (e) => {
    e.preventDefault();
    await api.put('/users/me', profile);
    await refreshUser();
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">{t('nav.dashboard')}</h1>

      <div className="grid grid-cols-3 gap-4 mb-8">
        {[
          { label: 'Total Expenses', value: summary.expenses !== null ? `$${summary.expenses}` : '—', color: 'text-red-600' },
          { label: 'Upcoming Activities', value: summary.activities ?? '—', color: 'text-blue-600' },
          { label: 'Investments Tracked', value: summary.investments ?? '—', color: 'text-green-600' },
        ].map((s) => (
          <Card key={s.label} className="text-center">
            <p className={`text-3xl font-bold ${s.color} mb-1`}>{s.value}</p>
            <p className="text-gray-600 text-lg">{s.label}</p>
          </Card>
        ))}
      </div>

      <Card>
        <h2 className="text-2xl font-bold text-gray-900 mb-5">{t('profile.title')}</h2>
        {saved && <p className="bg-green-50 text-green-700 px-4 py-2 rounded-lg text-lg mb-4">{t('profile.saved')}</p>}
        <form onSubmit={handleSave} className="grid md:grid-cols-2 gap-5">
          {[
            { key: 'name', label: t('profile.name'), type: 'text' },
            { key: 'age', label: t('profile.age'), type: 'number' },
            { key: 'zipcode', label: t('profile.zipcode'), type: 'text' },
          ].map(({ key, label, type }) => (
            <label key={key} className="flex flex-col gap-2 text-lg font-medium text-gray-700">
              {label}
              <input
                type={type} value={profile[key]}
                onChange={(e) => setProfile({ ...profile, [key]: e.target.value })}
                className="border border-gray-300 rounded-lg px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </label>
          ))}
          <label className="flex flex-col gap-2 text-lg font-medium text-gray-700">
            {t('profile.gender')}
            <select
              value={profile.gender}
              onChange={(e) => setProfile({ ...profile, gender: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">—</option>
              {genderOptions.map((g) => <option key={g} value={g}>{g.replace(/_/g, ' ')}</option>)}
            </select>
          </label>
          <label className="flex flex-col gap-2 text-lg font-medium text-gray-700">
            {t('profile.language')}
            <select
              value={profile.language_pref}
              onChange={(e) => setProfile({ ...profile, language_pref: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {LANGUAGES.map((l) => <option key={l.code} value={l.code}>{l.label}</option>)}
            </select>
          </label>
          <div className="md:col-span-2">
            <Button type="submit">{t('profile.save')}</Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
