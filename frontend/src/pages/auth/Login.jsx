import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import Button from '../../components/common/Button';

export default function Login() {
  const { t } = useTranslation();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(form.email, form.password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || t('common.error'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold text-gray-900 text-center mb-8">{t('auth.loginTitle')}</h1>
        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-md p-8 flex flex-col gap-5">
          {error && <p className="bg-red-50 text-red-700 px-4 py-3 rounded-lg text-lg">{error}</p>}
          <label className="flex flex-col gap-2 text-lg font-medium text-gray-700">
            {t('auth.email')}
            <input
              type="email" required autoComplete="email"
              value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="flex flex-col gap-2 text-lg font-medium text-gray-700">
            {t('auth.password')}
            <input
              type="password" required autoComplete="current-password"
              value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <Button type="submit" disabled={loading} className="w-full text-xl py-3 mt-2">
            {loading ? t('common.loading') : t('auth.loginBtn')}
          </Button>
          <p className="text-center text-lg text-gray-600">
            {t('auth.noAccount')}{' '}
            <Link to="/register" className="text-blue-700 font-semibold hover:underline">{t('nav.register')}</Link>
          </p>
        </form>
      </div>
    </div>
  );
}
