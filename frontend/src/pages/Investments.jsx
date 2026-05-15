import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../utils/api';
import Card from '../components/common/Card';
import Button from '../components/common/Button';

const TYPES = ['Stocks', 'Bonds', 'Mutual Funds', 'ETF', 'CD', 'Savings', 'Real Estate', 'Other'];
const today = new Date().toISOString().split('T')[0];
const emptyForm = { type: 'Savings', institution: '', amount: '', notes: '', as_of_date: today };

export default function Investments() {
  const { t } = useTranslation();
  const [investments, setInvestments] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [loading, setLoading] = useState(false);

  const fetchAll = () => api.get('/investments').then((r) => setInvestments(r.data.data)).catch(() => {});
  useEffect(() => { fetchAll(); }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    setLoading(true);
    try { await api.post('/investments', form); setForm(emptyForm); fetchAll(); }
    finally { setLoading(false); }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this investment?')) return;
    await api.delete(`/investments/${id}`);
    fetchAll();
  };

  const total = investments.reduce((s, i) => s + parseFloat(i.amount || 0), 0);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">{t('investments.title')}</h1>

      <Card className="mb-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">{t('investments.add')}</h2>
        <form onSubmit={handleAdd} className="grid md:grid-cols-2 gap-4">
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('investments.type')}
            <select value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
              {TYPES.map((tp) => <option key={tp} value={tp}>{tp}</option>)}
            </select>
          </label>
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('investments.institution')}
            <input type="text" value={form.institution}
              onChange={(e) => setForm({ ...form, institution: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('investments.amount')}
            <input type="number" step="0.01" min="0" required value={form.amount}
              onChange={(e) => setForm({ ...form, amount: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('investments.asOfDate')}
            <input type="date" required value={form.as_of_date}
              onChange={(e) => setForm({ ...form, as_of_date: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="md:col-span-2 flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('investments.notes')}
            <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })}
              rows={2} className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </label>
          <div className="md:col-span-2">
            <Button type="submit" disabled={loading}>{loading ? t('common.loading') : t('investments.add')}</Button>
          </div>
        </form>
      </Card>

      <Card>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-800">Portfolio</h2>
          <span className="text-2xl font-bold text-green-600">Total: ${total.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
        </div>
        {investments.length === 0 ? (
          <p className="text-gray-500 text-lg">No investments tracked yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-lg">
              <thead>
                <tr className="border-b border-gray-200 text-gray-600">
                  <th className="text-left py-3 pr-4">{t('investments.type')}</th>
                  <th className="text-left py-3 pr-4">{t('investments.institution')}</th>
                  <th className="text-right py-3 pr-4">{t('investments.amount')}</th>
                  <th className="text-left py-3 pr-4">{t('investments.asOfDate')}</th>
                  <th className="py-3"></th>
                </tr>
              </thead>
              <tbody>
                {investments.map((inv) => (
                  <tr key={inv.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 pr-4">
                      <span className="bg-green-50 text-green-700 px-2 py-0.5 rounded-full text-sm">{inv.type}</span>
                    </td>
                    <td className="py-3 pr-4 text-gray-700">{inv.institution}</td>
                    <td className="py-3 pr-4 text-right font-semibold text-gray-900">${parseFloat(inv.amount).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                    <td className="py-3 pr-4 text-gray-600">{inv.as_of_date?.split('T')[0]}</td>
                    <td className="py-3">
                      <button onClick={() => handleDelete(inv.id)} className="text-red-500 hover:text-red-700" aria-label="Delete">✕</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
