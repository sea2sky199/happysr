import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import api from '../utils/api';
import Card from '../components/common/Card';

const announcements = [
  { id: 1, title: 'New Medicare Part D changes for 2026', date: '2026-01-15', body: 'Important updates to prescription drug coverage are now in effect. Review your plan during open enrollment.' },
  { id: 2, title: 'Senior Wellness Fair — May 20', date: '2026-05-01', body: 'Join us for free health screenings, exercise demos, and resource booths at your local community center.' },
  { id: 3, title: 'AARP Tax Aide available through April', date: '2026-02-10', body: 'Free tax preparation assistance is available for seniors at select library branches.' },
];

export default function Home() {
  const { t } = useTranslation();
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    api.get('/activities').then((r) => setActivities(r.data.data.slice(0, 3))).catch(() => {});
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="bg-gradient-to-r from-blue-700 to-blue-500 text-white rounded-2xl p-10 mb-10 text-center shadow-lg">
        <h1 className="text-4xl md:text-5xl font-bold mb-3">{t('home.welcome')}</h1>
        <p className="text-xl md:text-2xl text-blue-100 mb-6">{t('home.subtitle')}</p>
        <div className="flex flex-wrap gap-4 justify-center">
          <Link to="/health" className="bg-white text-blue-700 font-semibold px-6 py-3 rounded-xl text-lg hover:bg-blue-50 transition-colors">❤️ Health Resources</Link>
          <Link to="/activities" className="bg-blue-600 text-white font-semibold px-6 py-3 rounded-xl text-lg hover:bg-blue-500 border border-white transition-colors">🎉 Activities</Link>
          <Link to="/travel" className="bg-blue-600 text-white font-semibold px-6 py-3 rounded-xl text-lg hover:bg-blue-500 border border-white transition-colors">✈️ Travel</Link>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">{t('home.latestNews')}</h2>
          <div className="flex flex-col gap-4">
            {announcements.map((a) => (
              <Card key={a.id}>
                <p className="text-sm text-blue-600 font-medium mb-1">{a.date}</p>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{a.title}</h3>
                <p className="text-gray-600 text-lg leading-relaxed">{a.body}</p>
              </Card>
            ))}
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">{t('home.upcomingEvents')}</h2>
          {activities.length === 0 ? (
            <Card>
              <p className="text-gray-500 text-lg">No upcoming events. Check back soon!</p>
            </Card>
          ) : (
            <div className="flex flex-col gap-4">
              {activities.map((a) => (
                <Card key={a.id}>
                  <p className="text-sm text-blue-600 font-medium mb-1">
                    {new Date(a.event_date).toLocaleDateString()} · {a.location}
                  </p>
                  <h3 className="text-xl font-semibold text-gray-900">{a.title}</h3>
                  {a.category && <span className="inline-block mt-2 text-sm bg-blue-50 text-blue-700 px-3 py-1 rounded-full">{a.category}</span>}
                </Card>
              ))}
              <Link to="/activities" className="text-blue-700 font-semibold text-lg hover:underline">
                View all activities →
              </Link>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
