import { useTranslation } from 'react-i18next';
import Card from '../components/common/Card';

const resources = [
  {
    category: 'Federal Programs',
    icon: '🏛️',
    items: [
      { name: 'Medicare', desc: 'Federal health insurance for people 65 or older. Learn about Parts A, B, C, and D.', url: 'https://www.medicare.gov' },
      { name: 'Medicaid', desc: 'Joint federal/state program for low-income individuals. Find your state plan.', url: 'https://www.medicaid.gov' },
      { name: 'Medicare Part D', desc: 'Prescription drug coverage. Compare plans during open enrollment.', url: 'https://www.medicare.gov/drug-coverage-part-d' },
    ],
  },
  {
    category: 'Health Information',
    icon: '📋',
    items: [
      { name: 'MedlinePlus', desc: 'Trusted health information from the National Library of Medicine.', url: 'https://medlineplus.gov' },
      { name: 'Healthfinder.gov', desc: 'Health resources and tools from the U.S. Department of Health.', url: 'https://health.gov/myhealthfinder' },
      { name: 'CDC Healthy Aging', desc: 'Tips for staying healthy and preventing disease as you age.', url: 'https://www.cdc.gov/aging' },
    ],
  },
  {
    category: 'Dental & Vision',
    icon: '🦷',
    items: [
      { name: 'NIDCR Senior Dental', desc: 'Dental information and resources from the National Institute of Dental Research.', url: 'https://www.nidcr.nih.gov/health-info/seniors' },
      { name: 'NEI Eye Health', desc: 'Eye health tips and vision resources for older adults from the National Eye Institute.', url: 'https://www.nei.nih.gov/learn-about-eye-health/outreach-campaigns-and-resources/older-adults' },
    ],
  },
  {
    category: 'Mental Health',
    icon: '🧠',
    items: [
      { name: 'NIMH Older Adults', desc: 'Mental health resources for older adults, including depression and anxiety information.', url: 'https://www.nimh.nih.gov/health/topics/older-adults-and-mental-health' },
      { name: 'SAMHSA Helpline', desc: 'Free, confidential mental health and substance use disorder information. 1-800-662-4357', url: 'https://www.samhsa.gov/find-help/national-helpline' },
    ],
  },
];

export default function Health() {
  const { t } = useTranslation();
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">{t('health.title')}</h1>
        <p className="text-xl text-gray-600 mt-2">{t('health.subtitle')}</p>
      </div>
      <div className="flex flex-col gap-8">
        {resources.map((section) => (
          <div key={section.category}>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              {section.icon} {section.category}
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {section.items.map((item) => (
                <Card key={item.name} className="flex flex-col gap-3">
                  <h3 className="text-xl font-semibold text-gray-900">{item.name}</h3>
                  <p className="text-gray-600 text-lg flex-1 leading-relaxed">{item.desc}</p>
                  <a
                    href={item.url} target="_blank" rel="noopener noreferrer"
                    className="text-blue-700 font-semibold text-lg hover:underline inline-flex items-center gap-1"
                  >
                    Visit Website →
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
