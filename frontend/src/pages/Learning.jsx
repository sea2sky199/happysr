import { useTranslation } from 'react-i18next';
import Card from '../components/common/Card';

const sections = [
  {
    title: 'Free Online Courses',
    icon: '🎓',
    items: [
      { name: 'Coursera for Seniors', desc: 'Thousands of free courses from top universities on topics from history to data science. Audit any course for free.', url: 'https://www.coursera.org' },
      { name: 'edX Free Courses', desc: 'University-level courses from MIT, Harvard, and more. Free audit track available on most courses.', url: 'https://www.edx.org' },
      { name: 'Khan Academy', desc: 'Completely free learning in math, science, history, grammar, and more at your own pace.', url: 'https://www.khanacademy.org' },
    ],
  },
  {
    title: 'Libraries & Reading',
    icon: '📚',
    items: [
      { name: 'OverDrive / Libby', desc: 'Borrow free e-books and audiobooks from your local library on any device — no cost, no late fees.', url: 'https://libbyapp.com' },
      { name: 'Project Gutenberg', desc: 'Over 70,000 free e-books — classic literature, history, and reference works in the public domain.', url: 'https://www.gutenberg.org' },
      { name: 'National Library Service (NLS)', desc: 'Free talking books and braille materials for people with print disabilities, from the Library of Congress.', url: 'https://www.loc.gov/nls' },
    ],
  },
  {
    title: 'Senior-Focused Programs',
    icon: '👴',
    items: [
      { name: 'Road Scholar', desc: 'Educational travel and online learning programs designed exclusively for adults 50 and older.', url: 'https://www.roadscholar.org' },
      { name: 'Osher Lifelong Learning (OLLI)', desc: 'University-based learning programs for adults 50+ at campuses nationwide — classes, lectures, and trips.', url: 'https://sagelearning.org/olli-directory' },
      { name: 'Senior Planet', desc: 'AARP-supported tech and wellness courses specifically designed for adults 60+. Free online classes.', url: 'https://seniorplanet.org' },
    ],
  },
  {
    title: 'Languages & Arts',
    icon: '🎨',
    items: [
      { name: 'Duolingo', desc: 'Learn a new language for free — Spanish, French, Mandarin, and 40+ others. Just 5 minutes a day.', url: 'https://www.duolingo.com' },
      { name: 'Skillshare Free Classes', desc: 'Creative classes on painting, photography, writing, and more. Many free lessons available.', url: 'https://www.skillshare.com' },
      { name: 'YouTube Learning', desc: 'Millions of free tutorial videos on every topic — cooking, crafts, history, music, and more.', url: 'https://www.youtube.com/learning' },
    ],
  },
];

export default function Learning() {
  const { t } = useTranslation();
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">{t('learning.title')}</h1>
        <p className="text-xl text-gray-600 mt-2">{t('learning.subtitle')}</p>
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
