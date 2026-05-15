import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../utils/api';
import Card from '../components/common/Card';
import Button from '../components/common/Button';

const CATEGORIES = ['food', 'medical', 'utilities', 'transportation', 'entertainment', 'other'];
const today = new Date().toISOString().split('T')[0];
const emptyForm = { amount: '', category: 'other', description: '', expense_date: today };

export default function Expenses() {
  const { t } = useTranslation();
  const [expenses, setExpenses] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchAll = () => api.get('/expenses').then((r) => setExpenses(r.data.data)).catch(() => {});
  useEffect(() => { fetchAll(); }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await api.post('/expenses', form);
      setForm(emptyForm);
      fetchAll();
    } catch (err) {
      setError(err.response?.data?.error || t('common.error'));
    } finally { setLoading(false); }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this expense?')) return;
    await api.delete(`/expenses/${id}`);
    fetchAll();
  };

  const total = expenses.reduce((s, e) => s + parseFloat(e.amount), 0);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">{t('expenses.title')}</h1>

      <Card className="mb-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">{t('expenses.add')}</h2>
        {error && <p className="bg-red-50 text-red-700 px-4 py-2 rounded-lg text-lg mb-3">{error}</p>}
        <form onSubmit={handleAdd} className="grid md:grid-cols-2 gap-4">
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('expenses.amount')}
            <input type="number" step="0.01" min="0.01" required value={form.amount}
              onChange={(e) => setForm({ ...form, amount: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('expenses.category')}
            <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
              {CATEGORIES.map((c) => <option key={c} value={c}>{t(`expenses.categories.${c}`)}</option>)}
            </select>
          </label>
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('expenses.description')}
            <input type="text" value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('expenses.date')}
            <input type="date" required value={form.expense_date}
              onChange={(e) => setForm({ ...form, expense_date: e.target.value })}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <div className="md:col-span-2">
            <Button type="submit" disabled={loading}>{loading ? t('common.loading') : t('expenses.add')}</Button>
          </div>
        </form>
      </Card>

      <Card>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-800">All Expenses</h2>
          <span className="text-2xl font-bold text-red-600">Total: ${total.toFixed(2)}</span>
        </div>
        {expenses.length === 0 ? (
          <p className="text-gray-500 text-lg">No expenses yet. Add your first one above.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-lg">
              <thead>
                <tr className="border-b border-gray-200 text-gray-600">
                  <th className="text-left py-3 pr-4">{t('expenses.date')}</th>
                  <th className="text-left py-3 pr-4">{t('expenses.category')}</th>
                  <th className="text-left py-3 pr-4">{t('expenses.description')}</th>
                  <th className="text-right py-3 pr-4">{t('expenses.amount')}</th>
                  <th className="py-3"></th>
                </tr>
              </thead>
              <tbody>
                {expenses.map((e) => (
                  <tr key={e.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 pr-4 text-gray-700">{e.expense_date?.split('T')[0]}</td>
                    <td className="py-3 pr-4">
                      <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full text-sm">{t(`expenses.categories.${e.category}`) || e.category}</span>
                    </td>
                    <td className="py-3 pr-4 text-gray-700">{e.description}</td>
                    <td className="py-3 pr-4 text-right font-semibold text-gray-900">${parseFloat(e.amount).toFixed(2)}</td>
                    <td className="py-3">
                      <button onClick={() => handleDelete(e.id)} className="text-red-500 hover:text-red-700 font-medium" aria-label="Delete">✕</button>
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
