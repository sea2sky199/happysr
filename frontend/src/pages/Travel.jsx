import { useTranslation } from 'react-i18next';
import Card from '../components/common/Card';

const sections = [
  {
    title: 'Senior Discounts & Programs',
    icon: '🏷️',
    items: [
      { name: 'AARP Travel Center', desc: 'Exclusive travel deals for AARP members including hotels, rental cars, and vacation packages.', url: 'https://www.aarp.org/travel' },
      { name: 'Senior Corps Volunteer Travel', desc: 'Volunteer travel opportunities and programs for adults 55+.', url: 'https://www.nationalservice.gov/programs/senior-corps' },
      { name: 'National Park Senior Pass', desc: 'The America the Beautiful Senior Pass grants lifetime access to national parks for $80.', url: 'https://www.nps.gov/subjects/npscelebration/senior-pass.htm' },
    ],
  },
  {
    title: 'Cruise Travel for Seniors',
    icon: '🚢',
    items: [
      { name: 'Cruise Critic Senior Deals', desc: 'Comprehensive cruise reviews, senior deals, and travel advice from experienced cruisers.', url: 'https://www.cruisecritic.com' },
      { name: 'Royal Caribbean', desc: 'Senior and AAA discounts available on sailings worldwide.', url: 'https://www.royalcaribbean.com' },
      { name: 'Holland America', desc: 'Known for relaxed pacing and itineraries popular with senior travelers.', url: 'https://www.hollandamerica.com' },
    ],
  },
  {
    title: 'Travel Safety & Health',
    icon: '🏥',
    items: [
      { name: 'CDC Traveler Health', desc: 'Health notices, vaccine recommendations, and travel health guidance by destination.', url: 'https://wwwnc.cdc.gov/travel' },
      { name: 'Travel Insurance for Seniors', desc: 'InsureMyTrip compares senior travel insurance plans including medical evacuation coverage.', url: 'https://www.insuremytrip.com' },
    ],
  },
  {
    title: 'Trip Planning Resources',
    icon: '🗺️',
    items: [
      { name: 'Road Scholar', desc: 'Educational travel programs designed specifically for adults 50 and older.', url: 'https://www.roadscholar.org' },
      { name: 'Overseas Adventure Travel', desc: 'Small-group tours with itineraries crafted for travelers 50+.', url: 'https://www.oattravel.com' },
    ],
  },
];

export default function Travel() {
  const { t } = useTranslation();
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">{t('travel.title')}</h1>
        <p className="text-xl text-gray-600 mt-2">{t('travel.subtitle')}</p>
      </div>
      <div className="flex flex-col gap-8">
        {sections.map((section) => (
          <div key={section.title}>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">{section.icon} {section.title}</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {section.items.map((item) => (
                <Card key={item.name} className="flex flex-col gap-3">
                  <h3 className="text-xl font-semibold text-gray-900">{item.name}</h3>
                  <p className="text-gray-600 text-lg flex-1 leading-relaxed">{item.desc}</p>
                  <a href={item.url} target="_blank" rel="noopener noreferrer"
                    className="text-blue-700 font-semibold text-lg hover:underline">
                    Learn More →
                  </a>
                </Card>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
