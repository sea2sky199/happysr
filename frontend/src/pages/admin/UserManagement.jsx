import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../../utils/api';
import Card from '../../components/common/Card';

export default function UserManagement() {
  const { t } = useTranslation();
  const [users, setUsers] = useState([]);
  const [saving, setSaving] = useState(null);

  const fetchUsers = () => api.get('/users/admin/users').then((r) => setUsers(r.data.data)).catch(() => {});
  useEffect(() => { fetchUsers(); }, []);

  const handleRoleChange = async (id, role) => {
    setSaving(id);
    try {
      await api.put(`/users/admin/users/${id}/role`, { role });
      setUsers((prev) => prev.map((u) => (u.id === id ? { ...u, role } : u)));
    } finally { setSaving(null); }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">{t('admin.title')}</h1>
      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-lg">
            <thead>
              <tr className="border-b border-gray-200 text-gray-600">
                <th className="text-left py-3 pr-4">{t('admin.name')}</th>
                <th className="text-left py-3 pr-4">{t('admin.email')}</th>
                <th className="text-left py-3 pr-4">{t('admin.age')}</th>
                <th className="text-left py-3 pr-4">{t('admin.joined')}</th>
                <th className="text-left py-3">{t('admin.role')}</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 pr-4 font-medium text-gray-900">{user.name || '—'}</td>
                  <td className="py-3 pr-4 text-gray-700">{user.email}</td>
                  <td className="py-3 pr-4 text-gray-600">{user.age || '—'}</td>
                  <td className="py-3 pr-4 text-gray-600">{new Date(user.created_at).toLocaleDateString()}</td>
                  <td className="py-3">
                    <select
                      value={user.role}
                      disabled={saving === user.id}
                      onChange={(e) => handleRoleChange(user.id, e.target.value)}
                      className="border border-gray-300 rounded-lg px-3 py-1.5 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                    >
                      <option value="user">User</option>
                      <option value="admin">Admin</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-4 text-gray-500 text-base">{users.length} user(s) registered</p>
      </Card>
    </div>
  );
}
