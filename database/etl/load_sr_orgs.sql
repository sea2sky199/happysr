-- Data load script for sr_orgs
-- Organizations that provide services to seniors
-- Run: mysql -u root -p happysr < database/etl/load_sr_orgs.sql

USE happysr;

TRUNCATE TABLE sr_orgs;

INSERT INTO sr_orgs (name, category, description, website_url, phone, email, address, city, state, zipcode, is_active) VALUES

-- ─── Government & Entitlements ─────────────────────────────────────────────
('Social Security Administration', 'Government', 'Federal agency that administers retirement, disability, and survivor benefits.', 'https://www.ssa.gov', '1-800-772-1213', NULL, '6401 Security Blvd', 'Baltimore', 'MD', '21235', TRUE),

('Medicare', 'Government', 'Federal health insurance program for people 65 or older and certain younger people with disabilities.', 'https://www.medicare.gov', '1-800-633-4227', NULL, '7500 Security Blvd', 'Baltimore', 'MD', '21244', TRUE),

('Medicaid', 'Government', 'Joint federal and state program providing health coverage for eligible low-income seniors.', 'https://www.medicaid.gov', '1-877-267-2323', NULL, '7500 Security Blvd', 'Baltimore', 'MD', '21244', TRUE),

('U.S. Department of Veterans Affairs', 'Government', 'Provides benefits, healthcare, and services to eligible veterans and their families.', 'https://www.va.gov', '1-800-698-2411', NULL, '810 Vermont Ave NW', 'Washington', 'DC', '20420', TRUE),

('Administration for Community Living', 'Government', 'Federal agency supporting older adults and people with disabilities to live where they choose.', 'https://acl.gov', '1-202-401-4634', 'aclinfo@acl.hhs.gov', '330 C St SW', 'Washington', 'DC', '20201', TRUE),

-- ─── Advocacy & National Nonprofits ────────────────────────────────────────
('AARP', 'Advocacy', 'Nonprofit membership organization empowering people 50 and older with resources on health, finances, and lifestyle.', 'https://www.aarp.org', '1-888-687-2277', 'member@aarp.org', '601 E St NW', 'Washington', 'DC', '20049', TRUE),

('National Council on Aging', 'Advocacy', 'Nonprofit organization that champions healthy aging and economic security for older adults.', 'https://www.ncoa.org', '1-571-527-3900', 'info@ncoa.org', '251 18th St S Ste 500', 'Arlington', 'VA', '22202', TRUE),

('Eldercare Locator', 'Advocacy', 'Nationwide service connecting seniors and caregivers to local aging services and resources.', 'https://eldercare.acl.gov', '1-800-677-1116', 'eldercarelocator@n4a.org', '1730 Rhode Island Ave NW Ste 1200', 'Washington', 'DC', '20036', TRUE),

('National Alliance for Caregiving', 'Advocacy', 'Nonprofit coalition focused on improving the quality of life for family caregivers and those they care for.', 'https://www.caregiving.org', '1-202-918-1013', 'info@caregiving.org', '1730 Rhode Island Ave NW Ste 812', 'Washington', 'DC', '20036', TRUE),

-- ─── Health & Medical ──────────────────────────────────────────────────────
('Meals on Wheels America', 'Nutrition', 'National organization supporting community programs that deliver nutritious meals to seniors at home.', 'https://www.mealsonwheelsamerica.org', '1-888-998-6325', 'mow@mealsonwheelsamerica.org', '1550 Crystal Dr Ste 902', 'Arlington', 'VA', '22202', TRUE),

('National Institute on Aging', 'Health', 'Federal institute conducting and supporting research on the nature of aging and age-related conditions.', 'https://www.nia.nih.gov', '1-800-222-2225', 'niaic@nia.nih.gov', '31 Center Dr MSC 2292', 'Bethesda', 'MD', '20892', TRUE),

('Alzheimer\'s Association', 'Health', 'Voluntary health organization dedicated to Alzheimer\'s care, support, and research.', 'https://www.alz.org', '1-800-272-3900', NULL, '225 N Michigan Ave Fl 17', 'Chicago', 'IL', '60601', TRUE),

('American Heart Association', 'Health', 'Nonprofit focused on heart disease and stroke prevention, especially relevant for seniors.', 'https://www.heart.org', '1-800-242-8721', NULL, '7272 Greenville Ave', 'Dallas', 'TX', '75231', TRUE),

('American Cancer Society', 'Health', 'Nationwide voluntary health organization dedicated to eliminating cancer as a major health problem.', 'https://www.cancer.org', '1-800-227-2345', NULL, '250 Williams St NW', 'Atlanta', 'GA', '30303', TRUE),

('Mental Health America', 'Mental Health', 'Community-based nonprofit addressing mental health needs including depression and anxiety common in seniors.', 'https://www.mhanational.org', '1-703-684-7722', 'info@mhanational.org', '500 Montgomery St Ste 820', 'Alexandria', 'VA', '22314', TRUE),

-- ─── Housing & Independence ────────────────────────────────────────────────
('National Shared Housing Resource Center', 'Housing', 'Helps seniors find shared housing arrangements to reduce costs and combat isolation.', 'https://www.nationalsharedhousing.org', '1-206-956-0334', 'info@nationalsharedhousing.org', NULL, 'Seattle', 'WA', NULL, TRUE),

('HUD Housing Counseling', 'Housing', 'HUD-approved counseling agencies offering free or low-cost housing advice to seniors facing foreclosure or rental issues.', 'https://www.hud.gov/housing/counseling', '1-800-569-4287', NULL, '451 7th St SW', 'Washington', 'DC', '20410', TRUE),

('Rebuilding Together', 'Housing', 'Nonprofit that rehabilitates homes for low-income seniors and people with disabilities free of charge.', 'https://rebuildingtogether.org', '1-800-473-4229', 'info@rebuildingtogether.org', '999 N Capitol St NE Ste 410', 'Washington', 'DC', '20002', TRUE),

-- ─── Financial Assistance ─────────────────────────────────────────────────
('BenefitsCheckUp (NCOA)', 'Financial', 'Free online tool that connects seniors to federal, state, and local benefit programs.', 'https://www.benefitscheckup.org', '1-571-527-3900', NULL, '251 18th St S Ste 500', 'Arlington', 'VA', '22202', TRUE),

('AARP Foundation', 'Financial', 'Provides legal, tax, and financial assistance to low-income seniors through programs like Tax-Aide.', 'https://www.aarpfoundation.org', '1-202-434-6200', 'aarpfoundation@aarp.org', '601 E St NW', 'Washington', 'DC', '20049', TRUE),

('Low Income Home Energy Assistance Program (LIHEAP)', 'Financial', 'Federal program helping low-income seniors with home heating and cooling energy costs.', 'https://www.acf.hhs.gov/ocs/programs/liheap', '1-202-401-9351', NULL, '330 C St SW', 'Washington', 'DC', '20201', TRUE),

-- ─── Transportation ───────────────────────────────────────────────────────
('ITNAmerica', 'Transportation', 'Nonprofit providing dignified, affordable transportation for seniors who no longer drive.', 'https://www.itnamerica.org', '1-207-857-9001', 'info@itnamerica.org', '1939 NE Broadway Ste 109', 'Portland', 'OR', '97232', TRUE),

('GoGoGrandparent', 'Transportation', 'Service that connects seniors to rideshare apps like Uber and Lyft via a simple phone call.', 'https://gogograndparent.com', '1-855-464-6872', 'support@gogograndparent.com', NULL, 'San Francisco', 'CA', NULL, TRUE),

-- ─── Legal Services ───────────────────────────────────────────────────────
('National Senior Citizens Law Center', 'Legal', 'Nonprofit advocating for the rights of low-income older adults on issues like elder abuse, housing, and benefits.', 'https://www.nsclc.org', '1-202-289-6976', 'nsclc@nsclc.org', '1444 I St NW Ste 1100', 'Washington', 'DC', '20005', TRUE),

('Legal Services Corporation', 'Legal', 'Independent nonprofit providing civil legal assistance to low-income Americans including seniors.', 'https://www.lsc.gov', '1-202-295-1500', NULL, '3333 K St NW', 'Washington', 'DC', '20007', TRUE),

-- ─── Social & Community ───────────────────────────────────────────────────
('YMCA Senior Programs', 'Social', 'Local YMCAs offer fitness classes, social activities, and wellness programs tailored to seniors.', 'https://www.ymca.org', '1-800-872-9622', NULL, '101 N Wacker Dr', 'Chicago', 'IL', '60606', TRUE),

('Senior Corps (AmeriCorps)', 'Social', 'Federal program connecting seniors 55+ with volunteer opportunities that enrich communities.', 'https://www.nationalservice.gov/programs/senior-corps', '1-800-942-2677', 'questions@cns.gov', '250 E St SW', 'Washington', 'DC', '20525', TRUE),

('SCORE', 'Education', 'Nonprofit offering free mentoring and education to seniors interested in starting or growing a small business.', 'https://www.score.org', '1-800-634-0245', NULL, '1175 Herndon Pkwy Ste 900', 'Herndon', 'VA', '20170', TRUE),

('Osher Lifelong Learning Institute (OLLI)', 'Education', 'Non-credit educational and social programs for adults 50+ offered through university partnerships nationwide.', 'https://scsep.dol.gov', '1-202-693-3911', NULL, '200 Constitution Ave NW', 'Washington', 'DC', '20210', TRUE),

-- ─── Technology & Digital Access ──────────────────────────────────────────
('Older Adults Technology Services (OATS)', 'Technology', 'Nonprofit helping seniors develop digital skills and stay connected through technology training.', 'https://oats.org', '1-212-356-0234', 'info@oats.org', '33 W 60th St Fl 4', 'New York', 'NY', '10023', TRUE),

('Senior Planet', 'Technology', 'Program of OATS offering free tech classes and online resources to help seniors use technology confidently.', 'https://seniorplanet.org', '1-888-713-3495', NULL, '33 W 60th St Fl 4', 'New York', 'NY', '10023', TRUE),

-- ─── Grief & End-of-Life ──────────────────────────────────────────────────
('Hospice Foundation of America', 'End-of-Life', 'Provides leadership in the development and application of hospice and its philosophy of care.', 'https://hospicefoundation.org', '1-800-854-3402', 'info@hospicefoundation.org', '1707 L St NW Ste 220', 'Washington', 'DC', '20036', TRUE),

('GriefShare', 'Mental Health', 'Support groups and resources for people grieving the death of a loved one, widely available for seniors.', 'https://www.griefshare.org', '1-919-562-2112', 'info@griefshare.org', '5905 Breckenridge Pkwy Ste F', 'Tampa', 'FL', '33610', TRUE);
