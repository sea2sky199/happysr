import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import api from '../utils/api';
import Card from '../components/common/Card';
import Button from '../components/common/Button';

const COLORS = ['#2563eb', '#16a34a', '#dc2626', '#d97706', '#7c3aed', '#0891b2', '#db2777', '#65a30d'];

export default function Reports() {
  const { t } = useTranslation();
  const [data, setData] = useState([]);
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (from) params.set('from', from);
      if (to) params.set('to', to);
      const res = await api.get(`/reports/expenses?${params}`);
      setData(res.data.data);
    } catch {} finally { setLoading(false); }
  };

  useEffect(() => { fetchData(); }, []);

  const byCategory = data.reduce((acc, row) => {
    const existing = acc.find((r) => r.category === row.category);
    if (existing) { existing.total += parseFloat(row.total); }
    else { acc.push({ category: row.category || 'other', total: parseFloat(row.total) }); }
    return acc;
  }, []);

  const byMonth = data.reduce((acc, row) => {
    const existing = acc.find((r) => r.month === row.month);
    if (existing) { existing.total += parseFloat(row.total); }
    else { acc.push({ month: row.month, total: parseFloat(row.total) }); }
    return acc;
  }, []).sort((a, b) => a.month.localeCompare(b.month));

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">{t('reports.title')}</h1>

      <Card className="mb-6">
        <div className="flex flex-wrap gap-4 items-end">
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('reports.from')}
            <input type="date" value={from} onChange={(e) => setFrom(e.target.value)}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
            {t('reports.to')}
            <input type="date" value={to} onChange={(e) => setTo(e.target.value)}
              className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </label>
          <Button onClick={fetchData} disabled={loading}>{loading ? t('common.loading') : t('reports.filter')}</Button>
        </div>
      </Card>

      {data.length === 0 ? (
        <Card><p className="text-gray-500 text-xl">{t('reports.noData')}</p></Card>
      ) : (
        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <h2 className="text-xl font-bold text-gray-800 mb-4">Expenses by Category</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={byCategory} dataKey="total" nameKey="category" cx="50%" cy="50%" outerRadius={100} label={({ category, percent }) => `${category} ${(percent * 100).toFixed(0)}%`}>
                  {byCategory.map((_, idx) => <Cell key={idx} fill={COLORS[idx % COLORS.length]} />)}
                </Pie>
                <Tooltip formatter={(v) => `$${v.toFixed(2)}`} />
              </PieChart>
            </ResponsiveContainer>
          </Card>

          <Card>
            <h2 className="text-xl font-bold text-gray-800 mb-4">Monthly Spending</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={byMonth}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis tickFormatter={(v) => `$${v}`} />
                <Tooltip formatter={(v) => `$${v.toFixed(2)}`} />
                <Bar dataKey="total" fill="#2563eb" name="Total" />
              </BarChart>
            </ResponsiveContainer>
          </Card>

          <Card className="md:col-span-2">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Summary by Category</h2>
            <table className="w-full text-lg">
              <thead>
                <tr className="border-b border-gray-200 text-gray-600">
                  <th className="text-left py-3 pr-6">{t('reports.category')}</th>
                  <th className="text-right py-3">{t('reports.total')}</th>
                </tr>
              </thead>
              <tbody>
                {byCategory.sort((a, b) => b.total - a.total).map((row) => (
                  <tr key={row.category} className="border-b border-gray-100">
                    <td className="py-3 pr-6 text-gray-700 capitalize">{row.category}</td>
                    <td className="py-3 text-right font-semibold text-gray-900">${row.total.toFixed(2)}</td>
                  </tr>
                ))}
                <tr className="font-bold text-gray-900">
                  <td className="py-3 pr-6">Grand Total</td>
                  <td className="py-3 text-right">${byCategory.reduce((s, r) => s + r.total, 0).toFixed(2)}</td>
                </tr>
              </tbody>
            </table>
          </Card>
        </div>
      )}
    </div>
  );
}
