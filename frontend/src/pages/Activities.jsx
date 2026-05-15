import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import api from '../utils/api';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Modal from '../components/common/Modal';

const CATEGORIES = ['Dancing', 'Exercise', 'Arts & Crafts', 'Social', 'Education', 'Games', 'Outdoors', 'Other'];

const emptyForm = { title: '', description: '', location: '', event_date: '', category: '' };

export default function Activities() {
  const { t } = useTranslation();
  const { isAdmin } = useAuth();
  const [activities, setActivities] = useState([]);
  const [filter, setFilter] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [loading, setLoading] = useState(false);

  const fetchAll = () => api.get('/activities').then((r) => setActivities(r.data.data)).catch(() => {});

  useEffect(() => { fetchAll(); }, []);

  const filtered = filter ? activities.filter((a) => a.category === filter) : activities;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/activities', form);
      setShowModal(false);
      setForm(emptyForm);
      fetchAll();
    } catch {} finally { setLoading(false); }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this activity?')) return;
    await api.delete(`/activities/${id}`);
    fetchAll();
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{t('activities.title')}</h1>
        {isAdmin && <Button onClick={() => setShowModal(true)}>{t('activities.add')}</Button>}
      </div>

      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => setFilter('')}
          className={`px-4 py-2 rounded-full text-lg font-medium transition-colors ${!filter ? 'bg-blue-700 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
        >
          {t('activities.all')}
        </button>
        {CATEGORIES.map((c) => (
          <button
            key={c} onClick={() => setFilter(c)}
            className={`px-4 py-2 rounded-full text-lg font-medium transition-colors ${filter === c ? 'bg-blue-700 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
          >
            {c}
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <Card><p className="text-gray-500 text-xl">{t('activities.noEvents')}</p></Card>
      ) : (
        <div className="grid md:grid-cols-2 gap-4">
          {filtered.map((a) => (
            <Card key={a.id}>
              <div className="flex justify-between items-start gap-2">
                <div className="flex-1">
                  <p className="text-blue-600 font-medium text-sm mb-1">
                    {new Date(a.event_date).toLocaleDateString('en-US', { weekday: 'short', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </p>
                  <h3 className="text-xl font-bold text-gray-900">{a.title}</h3>
                  {a.location && <p className="text-gray-600 mt-1">📍 {a.location}</p>}
                  {a.description && <p className="text-gray-600 mt-2 text-lg leading-relaxed">{a.description}</p>}
                  {a.category && <span className="inline-block mt-3 text-sm bg-blue-50 text-blue-700 px-3 py-1 rounded-full">{a.category}</span>}
                </div>
                {isAdmin && (
                  <button onClick={() => handleDelete(a.id)} className="text-red-500 hover:text-red-700 text-sm font-medium flex-shrink-0" aria-label="Delete">✕</button>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}

      {showModal && (
        <Modal title={t('activities.add')} onClose={() => setShowModal(false)}>
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            {[
              { key: 'title', label: 'Title', type: 'text', required: true },
              { key: 'location', label: t('activities.location'), type: 'text' },
              { key: 'event_date', label: t('activities.date'), type: 'datetime-local', required: true },
            ].map(({ key, label, type, required }) => (
              <label key={key} className="flex flex-col gap-1 text-lg font-medium text-gray-700">
                {label}
                <input type={type} required={required} value={form[key]}
                  onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                  className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </label>
            ))}
            <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
              Category
              <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}
                className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">—</option>
                {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
              </select>
            </label>
            <label className="flex flex-col gap-1 text-lg font-medium text-gray-700">
              Description
              <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })}
                rows={3} className="border border-gray-300 rounded-lg px-4 py-2.5 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </label>
            <Button type="submit" disabled={loading}>{loading ? t('common.loading') : t('common.save')}</Button>
          </form>
        </Modal>
      )}
    </div>
  );
}
