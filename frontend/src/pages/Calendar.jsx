import { useEffect, useState, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import ReactCalendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import api from '../utils/api';
import Card from '../components/common/Card';

const SOURCE_COLORS = {
  activity: 'bg-blue-100 text-blue-800 border-blue-200',
  event:    'bg-purple-100 text-purple-800 border-purple-200',
};

const SOURCE_DOT = {
  activity: 'bg-blue-500',
  event:    'bg-purple-500',
};

function toDateStr(d) {
  return d instanceof Date
    ? d.toISOString().split('T')[0]
    : String(d).split('T')[0];
}

export default function Calendar() {
  const { t } = useTranslation();
  const [events, setEvents] = useState([]);
  const [selected, setSelected] = useState(new Date());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/calendar')
      .then((r) => setEvents(r.data.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  // Map date string → events on that day
  const eventsByDate = useMemo(() => {
    const map = {};
    events.forEach((ev) => {
      const key = toDateStr(ev.event_date);
      if (!map[key]) map[key] = [];
      map[key].push(ev);
    });
    return map;
  }, [events]);

  const selectedStr = toDateStr(selected);
  const dayEvents = eventsByDate[selectedStr] || [];

  // Next 30 days of upcoming events
  const upcoming = useMemo(() => {
    const today = toDateStr(new Date());
    return events.filter((ev) => toDateStr(ev.event_date) >= today).slice(0, 10);
  }, [events]);

  const tileContent = ({ date, view }) => {
    if (view !== 'month') return null;
    const key = toDateStr(date);
    const dayEvs = eventsByDate[key];
    if (!dayEvs) return null;
    return (
      <div className="flex justify-center gap-0.5 mt-0.5 flex-wrap">
        {dayEvs.slice(0, 3).map((ev, i) => (
          <span key={i} className={`inline-block w-1.5 h-1.5 rounded-full ${SOURCE_DOT[ev.source]}`} />
        ))}
      </div>
    );
  };

  const tileClassName = ({ date, view }) => {
    if (view !== 'month') return '';
    const key = toDateStr(date);
    return eventsByDate[key] ? 'has-events' : '';
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{t('calendar.title')}</h1>
        <p className="text-xl text-gray-600 mt-1">{t('calendar.subtitle')}</p>
      </div>

      {/* Legend */}
      <div className="flex gap-4 mb-5 flex-wrap">
        <span className="flex items-center gap-2 text-lg text-gray-600">
          <span className="w-3 h-3 rounded-full bg-blue-500 inline-block" />
          {t('calendar.activityLegend')}
        </span>
        <span className="flex items-center gap-2 text-lg text-gray-600">
          <span className="w-3 h-3 rounded-full bg-purple-500 inline-block" />
          {t('calendar.eventLegend')}
        </span>
      </div>

      <div className="grid lg:grid-cols-[auto_1fr] gap-6">
        {/* Calendar widget */}
        <div>
          <Card className="p-2">
            <style>{`
              .react-calendar { border: none; font-size: 1.05rem; width: 100%; }
              .react-calendar__tile { padding: 0.6em 0.4em; min-height: 52px; }
              .react-calendar__tile--active { background: #1d4ed8 !important; border-radius: 8px; }
              .react-calendar__tile--now { background: #dbeafe; border-radius: 8px; }
              .react-calendar__tile.has-events { font-weight: 600; }
              .react-calendar__navigation button { font-size: 1rem; font-weight: 600; }
            `}</style>
            <ReactCalendar
              value={selected}
              onChange={setSelected}
              tileContent={tileContent}
              tileClassName={tileClassName}
            />
          </Card>

          {/* Selected day events */}
          <Card className="mt-4">
            <h2 className="text-xl font-bold text-gray-800 mb-3">
              {selected.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
            </h2>
            {loading ? (
              <p className="text-gray-500">{t('common.loading')}</p>
            ) : dayEvents.length === 0 ? (
              <p className="text-gray-500 text-lg">{t('calendar.noEvents')}</p>
            ) : (
              <ul className="flex flex-col gap-3">
                {dayEvents.map((ev, i) => (
                  <li key={i} className={`border rounded-lg px-4 py-3 ${SOURCE_COLORS[ev.source]}`}>
                    <p className="font-semibold text-lg">{ev.title}</p>
                    {ev.location && <p className="text-sm mt-0.5">📍 {ev.location}</p>}
                    {ev.description && <p className="text-sm mt-1 opacity-80">{ev.description}</p>}
                    {ev.category && (
                      <span className="inline-block mt-2 text-xs bg-white/60 px-2 py-0.5 rounded-full">{ev.category}</span>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </div>

        {/* Upcoming list */}
        <div>
          <Card>
            <h2 className="text-xl font-bold text-gray-800 mb-4">{t('calendar.upcoming')}</h2>
            {loading ? (
              <p className="text-gray-500">{t('common.loading')}</p>
            ) : upcoming.length === 0 ? (
              <p className="text-gray-500 text-lg">{t('calendar.noUpcoming')}</p>
            ) : (
              <ul className="divide-y divide-gray-100">
                {upcoming.map((ev, i) => {
                  const dateStr = toDateStr(ev.event_date);
                  const isSelected = dateStr === selectedStr;
                  return (
                    <li
                      key={i}
                      onClick={() => setSelected(new Date(dateStr + 'T12:00:00'))}
                      className={`py-4 px-2 cursor-pointer rounded-lg transition-colors hover:bg-gray-50 ${isSelected ? 'bg-blue-50' : ''}`}
                    >
                      <div className="flex gap-4 items-start">
                        {/* Date badge */}
                        <div className="flex-shrink-0 text-center bg-blue-700 text-white rounded-xl px-3 py-2 min-w-[56px]">
                          <p className="text-xs font-medium uppercase leading-tight">
                            {new Date(dateStr + 'T12:00:00').toLocaleDateString('en-US', { month: 'short' })}
                          </p>
                          <p className="text-2xl font-bold leading-tight">
                            {new Date(dateStr + 'T12:00:00').getDate()}
                          </p>
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${SOURCE_COLORS[ev.source]}`}>
                              {ev.source === 'activity' ? t('calendar.activityLegend') : t('calendar.eventLegend')}
                            </span>
                            {ev.category && (
                              <span className="text-xs text-gray-500">{ev.category}</span>
                            )}
                          </div>
                          <p className="font-semibold text-lg text-gray-900 mt-1">{ev.title}</p>
                          {ev.location && <p className="text-gray-500 text-sm">📍 {ev.location}</p>}
                          {ev.description && (
                            <p className="text-gray-600 text-sm mt-1 line-clamp-2">{ev.description}</p>
                          )}
                        </div>
                      </div>
                    </li>
                  );
                })}
              </ul>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
