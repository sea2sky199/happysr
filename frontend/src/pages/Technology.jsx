import { useTranslation } from 'react-i18next';
import Card from '../components/common/Card';

const sections = [
  {
    title: 'Getting Started',
    icon: '📱',
    items: [
      { name: 'GCFGlobal — Tech Basics', desc: 'Free, easy-to-follow lessons on computers, smartphones, email, and the internet — designed for beginners.', url: 'https://edu.gcfglobal.org/en/topics/technology' },
      { name: 'AARP Technology Tips', desc: 'Practical guides to help you get the most from your devices and apps.', url: 'https://www.aarp.org/home-family/personal-technology' },
      { name: 'Older Adults Technology Services (OATS)', desc: 'Training programs and resources from a nonprofit dedicated to senior tech education.', url: 'https://oats.org' },
    ],
  },
  {
    title: 'Staying Connected',
    icon: '📹',
    items: [
      { name: 'Video Calling Guide', desc: 'Step-by-step guides for Zoom, FaceTime, and Google Meet — stay in touch with family and friends.', url: 'https://edu.gcfglobal.org/en/zoom' },
      { name: 'Facebook for Seniors', desc: 'Learn how to connect with family, share photos, and join community groups on Facebook.', url: 'https://edu.gcfglobal.org/en/facebook-tips' },
      { name: 'Telehealth Guide', desc: 'How to use video appointments with your doctor — from the Health in Aging Foundation.', url: 'https://www.healthinaging.org/tools-and-tips/tip-sheet-telehealth-tips-older-adults' },
    ],
  },
  {
    title: 'Online Safety',
    icon: '🛡️',
    items: [
      { name: 'CISA Cybersecurity for Seniors', desc: 'Official government guidance on staying safe online, avoiding phishing, and protecting your accounts.', url: 'https://www.cisa.gov/resources-tools/resources/online-safety-resources-older-adults' },
      { name: 'Strong Passwords Guide', desc: 'How to create strong passwords and use a password manager to protect your accounts.', url: 'https://edu.gcfglobal.org/en/internetsafety/creating-strong-passwords/1' },
      { name: 'Recognizing Online Scams', desc: 'Learn to spot phishing emails, fake tech support calls, and other common senior-targeted scams.', url: 'https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams' },
    ],
  },
  {
    title: 'Useful Apps & Tools',
    icon: '🛠️',
    items: [
      { name: 'Google Maps Guide', desc: 'How to get turn-by-turn directions, find local businesses, and explore street view.', url: 'https://edu.gcfglobal.org/en/googlemaps' },
      { name: 'MyChart Patient Portal', desc: 'Access your medical records, test results, and communicate with your doctor online.', url: 'https://www.mychart.com' },
      { name: 'Accessibility Features', desc: 'Built-in tools on your phone or computer to make text larger, increase contrast, or use voice control.', url: 'https://www.aarp.org/home-family/personal-technology/info-2021/smartphone-accessibility-features.html' },
    ],
  },
];

export default function Technology() {
  const { t } = useTranslation();
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">{t('technology.title')}</h1>
        <p className="text-xl text-gray-600 mt-2">{t('technology.subtitle')}</p>
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
