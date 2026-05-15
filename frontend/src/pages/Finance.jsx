import { useTranslation } from 'react-i18next';
import Card from '../components/common/Card';

const sections = [
  {
    title: 'Social Security',
    icon: '🏛️',
    items: [
      { name: 'SSA My Account', desc: 'Check your Social Security statement, estimate future benefits, and manage your account online.', url: 'https://www.ssa.gov/myaccount' },
      { name: 'When to Claim Benefits', desc: 'Learn how claiming age (62–70) affects your monthly Social Security payment.', url: 'https://www.ssa.gov/benefits/retirement/planner/agereduction.html' },
      { name: 'Medicare & Social Security', desc: 'Understand how Medicare premiums are deducted from Social Security payments.', url: 'https://www.ssa.gov/benefits/medicare' },
    ],
  },
  {
    title: 'Retirement Planning',
    icon: '📈',
    items: [
      { name: 'AARP Retirement Calculator', desc: 'Estimate how much you need to save and when you can retire comfortably.', url: 'https://www.aarp.org/retirement/retirement-calculator' },
      { name: 'IRS Retirement Plans', desc: 'Official IRS guidance on IRAs, 401(k)s, required minimum distributions (RMDs), and more.', url: 'https://www.irs.gov/retirement-plans' },
      { name: 'MyMoney.gov', desc: 'Federal resource for financial literacy and retirement planning tools.', url: 'https://www.mymoney.gov' },
    ],
  },
  {
    title: 'Benefits & Assistance',
    icon: '🤝',
    items: [
      { name: 'BenefitsCheckUp', desc: 'Find federal, state, and local benefit programs you may qualify for — from the National Council on Aging.', url: 'https://www.benefitscheckup.org' },
      { name: 'LIHEAP Energy Assistance', desc: 'Low-income home energy assistance program to help with heating and cooling costs.', url: 'https://www.acf.hhs.gov/ocs/programs/liheap' },
      { name: 'Extra Help (LIS)', desc: 'Medicare Extra Help program covers most prescription drug plan costs for qualifying seniors.', url: 'https://www.ssa.gov/medicare/part-d-extra-help' },
    ],
  },
  {
    title: 'Fraud Protection',
    icon: '🔒',
    items: [
      { name: 'CFPB Senior Financial Protection', desc: 'Consumer Financial Protection Bureau resources to protect against financial exploitation and scams.', url: 'https://www.consumerfinance.gov/consumer-tools/fraud' },
      { name: 'FTC Scam Alerts', desc: "Federal Trade Commission scam alerts and advice on what to do if you're targeted.", url: 'https://consumer.ftc.gov/scams' },
      { name: 'AARP Fraud Watch Network', desc: 'Free fraud prevention tools, scam alerts, and a helpline (877-908-3360) for seniors.', url: 'https://www.aarp.org/money/scams-fraud' },
    ],
  },
];

export default function Finance() {
  const { t } = useTranslation();
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">{t('finance.title')}</h1>
        <p className="text-xl text-gray-600 mt-2">{t('finance.subtitle')}</p>
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
