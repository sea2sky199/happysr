import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { LANGUAGES } from '../context/LanguageContext';
import api from '../utils/api';
import Card from '../components/common/Card';
import Button from '../components/common/Button';

const GENDER_KEYS = ['male', 'female', 'other', 'prefer_not_to_say'];

const emptyPwd = { currentPassword: '', newPassword: '', confirmPassword: '' };

export default function Profile() {
  const { t } = useTranslation();
  const { user, refreshUser } = useAuth();

  const [profile, setProfile] = useState({
    name: '', gender: '', age: '', zipcode: '', language_pref: 'en',
  });
  const [profileMsg, setProfileMsg] = useState(null);

  const [pwd, setPwd] = useState(emptyPwd);
  const [pwdMsg, setPwdMsg] = useState(null);
  const [pwdLoading, setPwdLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setProfile({
        name: user.name || '',
        gender: user.gender || '',
        age: user.age || '',
        zipcode: user.zipcode || '',
        language_pref: user.language_pref || 'en',
      });
    }
  }, [user]);

  const handleProfileSave = async (e) => {
    e.preventDefault();
    setProfileMsg(null);
    await api.put('/users/me', profile);
    await refreshUser();
    setProfileMsg({ type: 'success', text: t('profile.saved') });
    setTimeout(() => setProfileMsg(null), 3000);
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setPwdMsg(null);
    if (pwd.newPassword !== pwd.confirmPassword) {
      setPwdMsg({ type: 'error', text: t('profile.passwordMismatch') });
      return;
    }
    setPwdLoading(true);
    try {
      await api.put('/users/me/password', {
        currentPassword: pwd.currentPassword,
        newPassword: pwd.newPassword,
      });
      setPwd(emptyPwd);
      setPwdMsg({ type: 'success', text: t('profile.passwordChanged') });
      setTimeout(() => setPwdMsg(null), 3000);
    } catch (err) {
      setPwdMsg({ type: 'error', text: err.response?.data?.error || t('common.error') });
    } finally {
      setPwdLoading(false);
    }
  };

  const roleLabel = user?.role === 'admin' ? 'Administrator' : 'Member';

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-gray-900">{t('profile.title')}</h1>

      {/* Account info — read-only */}
      <Card>
        <h2 className="text-xl font-bold text-gray-800 mb-4">{t('profile.accountInfo')}</h2>
        <div className="grid md:grid-cols-2 gap-4 text-lg">
          <div>
            <p className="text-gray-500 text-sm font-medium uppercase tracking-wide mb-1">{t('profile.email')}</p>
            <p className="text-gray-900 font-medium">{user?.email}</p>
          </div>
          <div>
            <p className="text-gray-500 text-sm font-medium uppercase tracking-wide mb-1">{t('profile.role')}</p>
            <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
              user?.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
            }`}>
              {roleLabel}
            </span>
          </div>
          <div>
            <p className="text-gray-500 text-sm font-medium uppercase tracking-wide mb-1">{t('profile.memberSince')}</p>
            <p className="text-gray-900 font-medium">
              {user?.created_at
                ? new Date(user.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
                : '—'}
            </p>
          </div>
        </div>
      </Card>

      {/* Personal info — editable */}
      <Card>
        <h2 className="text-xl font-bold text-gray-800 mb-4">{t('profile.personalInfo')}</h2>
        {profileMsg && (
          <p className={`px-4 py-2 rounded-lg text-lg mb-4 ${
            profileMsg.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
          }`}>
            {profileMsg.text}
          </p>
        )}
        <form onSubmit={handleProfileSave} className="grid md:grid-cols-2 gap-5">
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('profile.name')}
            <input
              type="text" value={profile.name}
              onChange={(e) => setProfile({ ...profile, name: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>

          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('profile.gender')}
            <select
              value={profile.gender}
              onChange={(e) => setProfile({ ...profile, gender: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">—</option>
              {GENDER_KEYS.map((g) => (
                <option key={g} value={g}>{t(`profile.genderOptions.${g}`)}</option>
              ))}
            </select>
          </label>

          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('profile.age')}
            <input
              type="number" min="0" max="120" value={profile.age}
              onChange={(e) => setProfile({ ...profile, age: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>

          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('profile.zipcode')}
            <input
              type="text" maxLength={10} value={profile.zipcode}
              onChange={(e) => setProfile({ ...profile, zipcode: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>

          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700 md:col-span-2">
            {t('profile.language')}
            <select
              value={profile.language_pref}
              onChange={(e) => setProfile({ ...profile, language_pref: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 md:w-1/2"
            >
              {LANGUAGES.map((l) => (
                <option key={l.code} value={l.code}>{l.label}</option>
              ))}
            </select>
          </label>

          <div className="md:col-span-2">
            <Button type="submit">{t('profile.save')}</Button>
          </div>
        </form>
      </Card>

      {/* Change password */}
      <Card>
        <h2 className="text-xl font-bold text-gray-800 mb-4">{t('profile.changePassword')}</h2>
        {pwdMsg && (
          <p className={`px-4 py-2 rounded-lg text-lg mb-4 ${
            pwdMsg.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
          }`}>
            {pwdMsg.text}
          </p>
        )}
        <form onSubmit={handlePasswordChange} className="flex flex-col gap-4 max-w-md">
          {[
            { key: 'currentPassword', label: t('profile.currentPassword') },
            { key: 'newPassword',     label: t('profile.newPassword') },
            { key: 'confirmPassword', label: t('profile.confirmPassword') },
          ].map(({ key, label }) => (
            <label key={key} className="flex flex-col gap-1 text-lg font-medium text-gray-700">
              {label}
              <input
                type="password" required value={pwd[key]}
                onChange={(e) => setPwd({ ...pwd, [key]: e.target.value })}
                className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </label>
          ))}
          <div>
            <Button type="submit" disabled={pwdLoading}>
              {pwdLoading ? t('common.loading') : t('profile.changePassword')}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
