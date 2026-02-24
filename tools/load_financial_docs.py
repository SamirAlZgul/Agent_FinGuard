# load_financial_docs.py
import os
import sys
from rag_knowledge_base import rag_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_sample_documents():
    """Создает примеры финансовых документов для тестирования с выдуманными компаниями"""
    docs_folder = "./financial_docs"
    os.makedirs(docs_folder, exist_ok=True)

    document_count = 0

    # ============================================
    # 1. ТЕХНОЛОГИЧЕСКИЕ КОМПАНИИ (квартальные отчеты)
    # ============================================

    # TechNova Inc. (квартальные отчеты)
    with open(os.path.join(docs_folder, "technova_q1_2023.txt"), "w") as f:
        f.write("""
TECHNOVA INC. (TNVA)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended January 1, 2023

COMPANY OVERVIEW
TechNova Inc. is a leading provider of cloud infrastructure, enterprise software, and digital transformation solutions. The company serves over 50,000 customers across 120 countries.

FINANCIAL HIGHLIGHTS
Total revenue: $24.3 billion
Cloud revenue: $12.8 billion
Software revenue: $8.5 billion
Services revenue: $3.0 billion
Gross margin: 72.4%
Operating income: $9.2 billion
Net income: $7.8 billion
Earnings per share: $1.95

SEGMENT RESULTS
Cloud Infrastructure: $12.8 billion (up 28% YoY)
Enterprise Software: $8.5 billion (up 12% YoY)
Professional Services: $3.0 billion (up 8% YoY)

AI INITIATIVES
TechNova continues to invest heavily in artificial intelligence. Our AI platform now serves over 15,000 developers, with revenue growing 65% year-over-year. We recently launched TechNova AI Studio, a suite of tools for building and deploying machine learning models.

MANAGEMENT DISCUSSION
"We are pleased with our strong start to fiscal 2023," said Jane Smith, CEO. "Our cloud business continues to gain share, and our AI investments are beginning to pay off. We remain confident in our long-term growth trajectory."
""")
    document_count += 1

    with open(os.path.join(docs_folder, "technova_q2_2023.txt"), "w") as f:
        f.write("""
TECHNOVA INC. (TNVA)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended April 1, 2023

FINANCIAL HIGHLIGHTS
Total revenue: $25.8 billion
Cloud revenue: $13.9 billion
Software revenue: $8.9 billion
Services revenue: $3.0 billion
Gross margin: 73.1%
Operating income: $10.1 billion
Net income: $8.6 billion
Earnings per share: $2.15

SEGMENT RESULTS
Cloud Infrastructure: $13.9 billion (up 32% YoY)
Enterprise Software: $8.9 billion (up 15% YoY)
Professional Services: $3.0 billion (up 5% YoY)

AI INITIATIVES
TechNova AI platform revenue grew 72% year-over-year. We now have over 20,000 active developers using our AI tools. Major customers include financial institutions, healthcare providers, and retail companies using AI for personalization and automation.

GEOGRAPHIC EXPANSION
International revenue now represents 45% of total revenue, up from 42% last year. We continue to invest in Europe and Asia-Pacific markets, with double-digit growth in both regions.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "technova_q3_2023.txt"), "w") as f:
        f.write("""
TECHNOVA INC. (TNVA)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended July 1, 2023

FINANCIAL HIGHLIGHTS
Total revenue: $26.9 billion
Cloud revenue: $14.8 billion
Software revenue: $9.2 billion
Services revenue: $2.9 billion
Gross margin: 73.5%
Operating income: $10.8 billion
Net income: $9.2 billion
Earnings per share: $2.30

SEGMENT RESULTS
Cloud Infrastructure: $14.8 billion (up 34% YoY)
Enterprise Software: $9.2 billion (up 16% YoY)
Professional Services: $2.9 billion (up 2% YoY)

NEW PRODUCTS
TechNova launched AI-powered analytics platform for enterprise customers. The platform combines data integration, machine learning, and visualization capabilities. Early customer feedback is positive, with 500 customers signed up in the first month.

COMPETITIVE LANDSCAPE
We continue to gain share against competitors. Our differentiated AI capabilities and strong partner ecosystem give us advantages in enterprise accounts. We are winning deals against both established players and emerging startups.
""")
    document_count += 1

    # QuantumLeap Technologies (квартальные отчеты)
    with open(os.path.join(docs_folder, "quantumleap_q1_2023.txt"), "w") as f:
        f.write("""
QUANTUMLEAP TECHNOLOGIES (QLEAP)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended January 1, 2023

COMPANY OVERVIEW
QuantumLeap Technologies develops advanced computing solutions including quantum processors, specialized AI chips, and high-performance computing systems.

FINANCIAL HIGHLIGHTS
Total revenue: $8.7 billion
AI Chip revenue: $5.2 billion
Quantum Computing revenue: $1.8 billion
HPC Systems revenue: $1.7 billion
Gross margin: 62.3%
Operating income: $2.4 billion
Net income: $2.0 billion
Earnings per share: $0.85

AI CHIP BUSINESS
Our next-generation AI accelerator, the QL-9000, is now shipping to major cloud providers. The chip delivers 3x performance improvement over previous generation. We have secured design wins with four of the top five cloud providers.

RESEARCH AND DEVELOPMENT
R&D spending was $1.8 billion, or 21% of revenue. We continue to invest in quantum computing research, with a goal of achieving quantum advantage within three years.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "quantumleap_q2_2023.txt"), "w") as f:
        f.write("""
QUANTUMLEAP TECHNOLOGIES (QLEAP)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended April 1, 2023

FINANCIAL HIGHLIGHTS
Total revenue: $9.4 billion
AI Chip revenue: $5.8 billion
Quantum Computing revenue: $1.9 billion
HPC Systems revenue: $1.7 billion
Gross margin: 63.1%
Operating income: $2.7 billion
Net income: $2.3 billion
Earnings per share: $0.96

AI CHIP BUSINESS
QL-9000 shipments exceeded expectations, with revenue up 45% year-over-year. We are expanding manufacturing capacity to meet strong demand. New customers include automotive companies using our chips for autonomous driving development.

QUANTUM COMPUTING
We achieved a major milestone: our quantum processor successfully solved a complex optimization problem that would take classical supercomputers years to complete. We are now working with select enterprise customers on pilot programs.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "quantumleap_q3_2023.txt"), "w") as f:
        f.write("""
QUANTUMLEAP TECHNOLOGIES (QLEAP)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended July 1, 2023

FINANCIAL HIGHLIGHTS
Total revenue: $10.2 billion
AI Chip revenue: $6.4 billion
Quantum Computing revenue: $2.1 billion
HPC Systems revenue: $1.7 billion
Gross margin: 63.8%
Operating income: $3.1 billion
Net income: $2.6 billion
Earnings per share: $1.08

AI CHIP PIPELINE
We announced the QL-10000, our next-generation AI chip scheduled for release in 2024. The chip will feature new architecture optimized for large language models and generative AI workloads.

QUANTUM COMPUTING
We expanded our quantum cloud service to include access to our quantum processors via API. Early customers include financial services firms using quantum algorithms for portfolio optimization.
""")
    document_count += 1

    # ============================================
    # 2. ФИНАНСОВЫЕ И БАНКОВСКИЕ КОМПАНИИ
    # ============================================

    # CapitalGuard Bank (годовые отчеты)
    with open(os.path.join(docs_folder, "capitalguard_annual_2022.txt"), "w") as f:
        f.write("""
CAPITALGUARD BANK (CGUARD)
FORM 10-K (ANNUAL REPORT)
For the fiscal year ended December 31, 2022

COMPANY OVERVIEW
CapitalGuard is a diversified financial services company with operations in retail banking, commercial lending, wealth management, and investment banking.

FINANCIAL SUMMARY
Total revenue: $42.6 billion
Net interest income: $28.3 billion
Non-interest income: $14.3 billion
Net income: $12.1 billion
Earnings per share: $8.45
Return on equity: 14.2%
Return on assets: 1.2%

SEGMENT RESULTS
Retail Banking: $18.5 billion revenue
Commercial Banking: $14.2 billion revenue
Wealth Management: $5.8 billion revenue
Investment Banking: $4.1 billion revenue

BALANCE SHEET
Total assets: $980 billion
Total loans: $620 billion
Total deposits: $720 billion
Total equity: $85 billion
Tier 1 capital ratio: 12.5%

DIGITAL TRANSFORMATION
CapitalGuard invested $1.2 billion in digital initiatives during 2022. Mobile banking users grew 22% to 15 million. Digital transactions now represent 65% of all customer interactions.

AI APPLICATIONS
We are using AI across the organization:
- Fraud detection: ML models reduced fraud losses by 35%
- Credit underwriting: AI models improved approval accuracy by 25%
- Customer service: AI chatbots handle 40% of routine inquiries
- Investment research: NLP analyzes news and reports for trading signals

RISK FACTORS
Our business is subject to credit risk, market risk, operational risk, and regulatory risk. Economic uncertainty could impact loan performance and customer activity.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "capitalguard_q1_2023.txt"), "w") as f:
        f.write("""
CAPITALGUARD BANK (CGUARD)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended March 31, 2023

FINANCIAL HIGHLIGHTS
Total revenue: $11.2 billion
Net interest income: $7.5 billion
Non-interest income: $3.7 billion
Net income: $3.3 billion
Earnings per share: $2.28

LOAN PORTFOLIO
Commercial loans: $245 billion
Consumer loans: $185 billion
Mortgage loans: $160 billion
Total loans: $590 billion
Non-performing loans: 0.8% of total

DEPOSITS
Consumer deposits: $380 billion
Commercial deposits: $310 billion
Total deposits: $690 billion

AI INITIATIVES
We expanded our AI-powered investment advisory service, CapitalGuard AI Advisor. The service now has 250,000 users and $15 billion in assets under management. Early data shows AI-driven portfolios outperforming traditional ones by 120 basis points.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "capitalguard_q2_2023.txt"), "w") as f:
        f.write("""
CAPITALGUARD BANK (CGUARD)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended June 30, 2023

FINANCIAL HIGHLIGHTS
Total revenue: $11.5 billion
Net interest income: $7.7 billion
Non-interest income: $3.8 billion
Net income: $3.4 billion
Earnings per share: $2.35

WEALTH MANAGEMENT
Assets under management reached $425 billion, up 8% year-to-date. Strong performance in equity markets and net inflows contributed to growth. Our AI-powered advisory service now has 300,000 users.

TECHNOLOGY INVESTMENT
We announced a $500 million partnership with TechNova to develop AI solutions for banking. The partnership will focus on fraud detection, credit underwriting, and personalized customer experiences.
""")
    document_count += 1

    # Apex Investment Partners (инвестиционная компания)
    with open(os.path.join(docs_folder, "apex_investment_annual_2022.txt"), "w") as f:
        f.write("""
APEX INVESTMENT PARTNERS (APEX)
FORM 10-K (ANNUAL REPORT)
For the fiscal year ended December 31, 2022

COMPANY OVERVIEW
Apex Investment Partners is a global investment management firm offering mutual funds, ETFs, and separately managed accounts to institutional and retail investors.

FINANCIAL SUMMARY
Total revenue: $8.2 billion
Management fees: $6.5 billion
Performance fees: $1.2 billion
Other income: $0.5 billion
Operating income: $3.8 billion
Net income: $3.1 billion
Earnings per share: $5.20

ASSETS UNDER MANAGEMENT
Total AUM: $1.2 trillion
Equity strategies: $650 billion
Fixed income: $350 billion
Alternative investments: $120 billion
Money market: $80 billion

INVESTMENT PERFORMANCE
85% of our mutual funds outperformed their benchmarks over the 5-year period. Our flagship Apex Growth Fund has generated 14.2% annualized returns over the past decade.

AI IN INVESTING
We have integrated AI across our investment process:
- Quantitative models identify market inefficiencies
- NLP analyzes earnings calls and news sentiment
- Machine learning optimizes portfolio construction
- AI assists in risk management and scenario analysis

OUTLOOK
We see opportunities in AI-related companies, healthcare innovation, and sustainable investing. Our research suggests companies with strong AI capabilities will outperform over the next decade.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "apex_investment_q1_2023.txt"), "w") as f:
        f.write("""
APEX INVESTMENT PARTNERS (APEX)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended March 31, 2023

FINANCIAL HIGHLIGHTS
Revenue: $2.2 billion
Operating income: $1.1 billion
Net income: $0.9 billion
Earnings per share: $1.45

ASSETS UNDER MANAGEMENT
Total AUM: $1.25 trillion
Net inflows: $25 billion
Market appreciation: $25 billion

INVESTMENT STRATEGY
We increased exposure to technology and AI-related companies during the quarter. Top holdings include TechNova, QuantumLeap, and DataStream AI. We believe AI represents a multi-year investment opportunity.

NEW PRODUCTS
We launched the Apex AI Innovation ETF, which invests in companies developing or benefiting from artificial intelligence. The fund has attracted $500 million in assets since its February launch.
""")
    document_count += 1

    # ============================================
    # 3. ФАРМАЦЕВТИЧЕСКИЕ И БИОТЕХ КОМПАНИИ
    # ============================================

    # BioVita Pharmaceuticals
    with open(os.path.join(docs_folder, "biovita_annual_2022.txt"), "w") as f:
        f.write("""
BIOVITA PHARMACEUTICALS (BVITA)
FORM 10-K (ANNUAL REPORT)
For the fiscal year ended December 31, 2022

COMPANY OVERVIEW
BioVita is a global pharmaceutical company focused on developing and commercializing innovative medicines for cancer, autoimmune diseases, and rare disorders.

FINANCIAL SUMMARY
Total revenue: $28.5 billion
Product sales: $24.2 billion
Royalty revenue: $3.1 billion
Collaboration revenue: $1.2 billion
Gross margin: 78.5%
R&D expense: $6.8 billion (24% of revenue)
Net income: $5.9 billion
Earnings per share: $4.85

KEY PRODUCTS
Oncology portfolio: $12.5 billion
Immunology portfolio: $8.2 billion
Rare diseases: $4.5 billion
Other products: $3.3 billion

PIPELINE
Phase 3 programs: 8
Phase 2 programs: 15
Phase 1 programs: 22
NDA submissions planned 2023: 4

AI IN DRUG DISCOVERY
BioVita has invested $500 million in AI-powered drug discovery. Our AI platform has identified 15 novel drug candidates, with 3 advancing to clinical trials. AI has reduced early-stage discovery time by 40%.

RECENT DEVELOPMENTS
FDA approved our new cancer therapy, OncoVita, for lung cancer treatment. Peak sales potential estimated at $3 billion annually.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "biovita_q1_2023.txt"), "w") as f:
        f.write("""
BIOVITA PHARMACEUTICALS (BVITA)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended March 31, 2023

FINANCIAL HIGHLIGHTS
Revenue: $7.4 billion
Product sales: $6.3 billion
R&D expense: $1.8 billion
Net income: $1.5 billion
Earnings per share: $1.22

PRODUCT PERFORMANCE
OncoVita (launched January): $450 million sales
ImmunoVita (autoimmune): $2.1 billion sales
CardioVita: $1.2 billion sales
Other products: $2.5 billion sales

PIPELINE UPDATE
Positive Phase 3 results for NeuroVita in Alzheimer's disease. We plan to submit NDA in Q4 2023. Analyst estimates peak sales of $4 billion.

AI PARTNERSHIP
Expanded collaboration with QuantumLeap Technologies to apply quantum computing to protein folding problems. Initial results show 30% improvement in prediction accuracy.
""")
    document_count += 1

    # GenoMedix (биотех)
    with open(os.path.join(docs_folder, "genomedix_annual_2022.txt"), "w") as f:
        f.write("""
GENOMEDIX INC. (GMDX)
FORM 10-K (ANNUAL REPORT)
For the fiscal year ended December 31, 2022

COMPANY OVERVIEW
GenoMedix is a biotechnology company focused on gene therapies and precision medicine for rare genetic disorders.

FINANCIAL SUMMARY
Revenue: $1.2 billion
Collaboration revenue: $850 million
Grant revenue: $350 million
R&D expense: $680 million
Net loss: -$220 million
Cash and investments: $1.5 billion

PIPELINE
Gene therapy programs: 12
Lead program: GMDX-101 for cystic fibrosis (Phase 3)
GMDX-201 for muscular dystrophy (Phase 2)
GMDX-301 for Huntington's disease (Phase 1/2)

TECHNOLOGY PLATFORM
Our proprietary AAV vector platform enables targeted delivery of therapeutic genes. We have exclusive licenses to key patents covering AAV manufacturing and delivery.

AI APPLICATIONS
GenoMedix uses AI for:
- AAV capsid engineering and optimization
- Patient stratification for clinical trials
- Biomarker discovery
- Manufacturing process optimization

RECENT DEVELOPMENTS
Positive interim data from GMDX-101 Phase 3 trial showed 45% improvement in lung function. We expect to complete enrollment by Q3 2023 and file BLA in 2024.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "genomedix_q1_2023.txt"), "w") as f:
        f.write("""
GENOMEDIX INC. (GMDX)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended March 31, 2023

FINANCIAL HIGHLIGHTS
Revenue: $310 million
R&D expense: $185 million
Net loss: -$65 million
Cash position: $1.4 billion

CLINICAL UPDATE
GMDX-101 (cystic fibrosis): Enrollment complete with 120 patients. Top-line data expected Q4 2023.
GMDX-201 (muscular dystrophy): Phase 2 enrollment ongoing, 45 patients enrolled.
GMDX-301 (Huntington's): Phase 1/2 initiated, first patient dosed.

MANUFACTURING
Completed construction of commercial-scale manufacturing facility. Capacity sufficient to support initial product launches.

STRATEGIC PARTNERSHIP
Announced collaboration with TechNova to develop AI models for predicting AAV vector immunogenicity. Partnership includes $50 million upfront and potential milestones.
""")
    document_count += 1

    # ============================================
    # 4. ЭНЕРГЕТИЧЕСКИЕ КОМПАНИИ
    # ============================================

    # NovaStar Energy
    with open(os.path.join(docs_folder, "novastar_annual_2022.txt"), "w") as f:
        f.write("""
NOVASTAR ENERGY (NOVA)
FORM 10-K (ANNUAL REPORT)
For the fiscal year ended December 31, 2022

COMPANY OVERVIEW
NovaStar Energy is an integrated energy company with operations in renewable energy, natural gas, and electricity generation.

FINANCIAL SUMMARY
Total revenue: $18.3 billion
Renewable energy: $7.2 billion
Natural gas: $6.5 billion
Electricity generation: $4.6 billion
Operating income: $3.8 billion
Net income: $2.9 billion
Earnings per share: $2.45

RENEWABLE PORTFOLIO
Solar capacity: 3.5 GW
Wind capacity: 2.8 GW
Battery storage: 1.2 GW
Under construction: 4.0 GW

SUSTAINABILITY
Carbon emissions reduced 35% since 2018. Target of net zero by 2040. 65% of capital spending directed to renewable projects.

AI APPLICATIONS
NovaStar uses AI for:
- Wind farm optimization (increased output by 8%)
- Solar forecasting (improved accuracy by 25%)
- Grid management and load balancing
- Predictive maintenance (reduced downtime by 30%)

STRATEGIC INITIATIVES
Investing $2 billion in green hydrogen production. First facility expected online in 2025. Partnership with automotive companies for hydrogen fueling infrastructure.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "novastar_q1_2023.txt"), "w") as f:
        f.write("""
NOVASTAR ENERGY (NOVA)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended March 31, 2023

FINANCIAL HIGHLIGHTS
Revenue: $5.1 billion
Renewable energy: $2.2 billion
Natural gas: $1.8 billion
Electricity: $1.1 billion
Operating income: $1.1 billion
Net income: $0.9 billion

RENEWABLE PROJECTS
Completed 500 MW solar project in Texas. Began construction on 750 MW wind farm in Oklahoma. Added 300 MW of battery storage capacity.

AI INVESTMENT
Launched NovaAI, a subsidiary focused on AI applications for energy management. Initial products include grid optimization software and renewable forecasting tools.
""")
    document_count += 1

    # GreenFuture Renewables
    with open(os.path.join(docs_folder, "greenfuture_annual_2022.txt"), "w") as f:
        f.write("""
GREENFUTURE RENEWABLES (GFR)
FORM 10-K (ANNUAL REPORT)
For the fiscal year ended December 31, 2022

COMPANY OVERVIEW
GreenFuture Renewables develops, owns, and operates utility-scale solar and wind projects across North America and Europe.

FINANCIAL SUMMARY
Revenue: $2.8 billion
Operating income: $850 million
Net income: $620 million
EBITDA: $1.4 billion

OPERATING PORTFOLIO
Solar projects: 2.8 GW
Wind projects: 1.9 GW
Total capacity: 4.7 GW
Capacity factor: 28%
Production: 11.5 TWh

DEVELOPMENT PIPELINE
Solar: 5.2 GW
Wind: 3.1 GW
Battery storage: 1.5 GW
Total pipeline: 9.8 GW

TECHNOLOGY PARTNERSHIPS
Collaborating with QuantumLeap on AI-powered solar tracking systems. Early results show 12% increase in energy yield.

FINANCING
Secured $1.5 billion in green bonds for project development. Weighted average cost of debt: 4.2%.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "greenfuture_q1_2023.txt"), "w") as f:
        f.write("""
GREENFUTURE RENEWABLES (GFR)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended March 31, 2023

FINANCIAL HIGHLIGHTS
Revenue: $780 million
Operating income: $240 million
Net income: $175 million
EBITDA: $390 million

NEW PROJECTS
Acquired 600 MW solar portfolio in Spain. Began construction on 400 MW wind farm in Texas. Completed 200 MW battery storage facility in California.

AI IMPLEMENTATION
Deployed AI-based predictive maintenance across all operating assets. Early data shows 15% reduction in unplanned downtime and 8% increase in energy production.
""")
    document_count += 1

    # ============================================
    # 5. ПОТРЕБИТЕЛЬСКИЕ КОМПАНИИ
    # ============================================

    # OmniConsumer Products
    with open(os.path.join(docs_folder, "omniconsumer_annual_2022.txt"), "w") as f:
        f.write("""
OMNICONSUMER PRODUCTS (OMNI)
FORM 10-K (ANNUAL REPORT)
For the fiscal year ended December 31, 2022

COMPANY OVERVIEW
OmniConsumer is a global leader in consumer packaged goods, with brands in food, beverage, personal care, and household products.

FINANCIAL SUMMARY
Revenue: $45.2 billion
North America: $22.8 billion
Europe: $12.5 billion
Asia-Pacific: $7.2 billion
Latin America: $2.7 billion
Gross margin: 48.5%
Operating income: $8.4 billion
Net income: $6.3 billion
Earnings per share: $4.20

BRAND PORTFOLIO
Food and beverage: $24.5 billion
Personal care: $12.8 billion
Household products: $7.9 billion

E-COMMERCE
Online sales grew 22% to $8.5 billion, representing 19% of total revenue. Direct-to-consumer channels grew 35%.

AI APPLICATIONS
- Demand forecasting: AI models improved forecast accuracy by 30%
- Supply chain optimization: Reduced inventory costs by 15%
- Personalized marketing: Increased conversion rates by 25%
- Product development: AI identifies consumer trends and preferences

SUSTAINABILITY
Reduced plastic packaging by 18% since 2020. Goal of 100% recyclable packaging by 2025. Invested $500 million in sustainable sourcing initiatives.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "omniconsumer_q1_2023.txt"), "w") as f:
        f.write("""
OMNICONSUMER PRODUCTS (OMNI)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended March 31, 2023

FINANCIAL HIGHLIGHTS
Revenue: $11.8 billion
Gross margin: 49.2%
Operating income: $2.3 billion
Net income: $1.7 billion
Earnings per share: $1.12

SEGMENT PERFORMANCE
Food and beverage: $6.4 billion
Personal care: $3.3 billion
Household: $2.1 billion

E-COMMERCE
Online sales: $2.3 billion (up 18% YoY)
Direct-to-consumer: $850 million (up 28% YoY)

AI INITIATIVES
Launched AI-powered personalization engine for e-commerce sites. Early results show 15% increase in average order value and 20% improvement in customer retention.

NEW PRODUCTS
Introduced OmniSmart home products line with AI capabilities. Includes smart kitchen appliances and personal care devices. Initial reception exceeds expectations.
""")
    document_count += 1

    # LuxeRetail Group
    with open(os.path.join(docs_folder, "luxeretail_annual_2022.txt"), "w") as f:
        f.write("""
LUXERETAIL GROUP (LUXE)
FORM 10-K (ANNUAL REPORT)
For the fiscal year ended December 31, 2022

COMPANY OVERVIEW
LuxeRetail is a premier luxury goods company with brands in fashion, accessories, jewelry, and cosmetics.

FINANCIAL SUMMARY
Revenue: $15.6 billion
Fashion and accessories: $8.2 billion
Jewelry and watches: $4.5 billion
Cosmetics and fragrances: $2.9 billion
Gross margin: 72.5%
Operating income: $4.2 billion
Net income: $3.1 billion
Earnings per share: $6.80

GEOGRAPHIC REVENUE
Europe: $6.2 billion
Americas: $5.1 billion
Asia-Pacific: $3.8 billion
Middle East: $0.5 billion

DIGITAL TRANSFORMATION
E-commerce revenue: $3.2 billion (21% of total)
Mobile app users: 5 million
Digital engagement up 45% year-over-year

AI APPLICATIONS
- Personalized recommendations: Increased conversion by 35%
- Inventory optimization: Reduced stockouts by 40%
- Pricing optimization: Improved margins by 250 basis points
- Customer service: AI chatbots handle 50% of inquiries

BRAND ACQUISITIONS
Acquired heritage jewelry brand for $850 million. Integration progressing well with cross-selling opportunities identified.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "luxeretail_q1_2023.txt"), "w") as f:
        f.write("""
LUXERETAIL GROUP (LUXE)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended March 31, 2023

FINANCIAL HIGHLIGHTS
Revenue: $4.1 billion
Gross margin: 73.2%
Operating income: $1.1 billion
Net income: $0.8 billion
Earnings per share: $1.75

SEGMENT PERFORMANCE
Fashion: $2.2 billion
Jewelry: $1.2 billion
Cosmetics: $0.7 billion

DIGITAL
E-commerce: $920 million (22% of revenue)
Mobile app downloads: +35% YoY

AI LAUNCH
Introduced LuxeAI Stylist, an AI-powered personal shopping assistant. The tool analyzes customer preferences and provides personalized fashion recommendations. Early user engagement is strong with 40% returning weekly.

STORE EXPANSION
Opened flagship stores in Shanghai and Dubai. Renovated Paris flagship with enhanced digital experience. Store productivity up 12% year-over-year.
""")
    document_count += 1

    # ============================================
    # 6. ПРОМЫШЛЕННЫЕ КОМПАНИИ
    # ============================================

    # Industrial Dynamics Corp
    with open(os.path.join(docs_folder, "industrial_dynamics_annual_2022.txt"), "w") as f:
        f.write("""
INDUSTRIAL DYNAMICS CORP (IDYN)
FORM 10-K (ANNUAL REPORT)
For the fiscal year ended December 31, 2022

COMPANY OVERVIEW
Industrial Dynamics manufactures industrial automation equipment, robotics, and factory automation systems.

FINANCIAL SUMMARY
Revenue: $12.8 billion
Robotics: $5.2 billion
Automation systems: $4.5 billion
Industrial components: $3.1 billion
Gross margin: 38.5%
Operating income: $2.1 billion
Net income: $1.6 billion
Earnings per share: $3.25

GEOGRAPHIC REVENUE
North America: $5.8 billion
Europe: $3.9 billion
Asia: $2.8 billion
Rest of world: $0.3 billion

PRODUCT LINES
Industrial robots: 25,000 units shipped
Collaborative robots (cobots): 12,000 units shipped
Automation software: $850 million revenue
Vision systems: $620 million revenue

AI INTEGRATION
All new robots feature AI-powered vision and control systems. Machine learning enables robots to adapt to new tasks without reprogramming. Customers report 30% productivity improvements.

RESEARCH AND DEVELOPMENT
R&D spending: $980 million (7.7% of revenue)
AI research center opened in Boston
150 PhDs working on next-generation robotics

OUTLOOK
Strong demand from automotive, electronics, and logistics industries. Order backlog of $3.5 billion, up 25% year-over-year.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "industrial_dynamics_q1_2023.txt"), "w") as f:
        f.write("""
INDUSTRIAL DYNAMICS CORP (IDYN)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended March 31, 2023

FINANCIAL HIGHLIGHTS
Revenue: $3.5 billion
Robotics: $1.5 billion
Automation: $1.2 billion
Components: $0.8 billion
Operating income: $620 million
Net income: $480 million
Earnings per share: $0.95

NEW PRODUCTS
Launched ID-7 collaborative robot with advanced AI capabilities. Features include natural language programming and autonomous task planning. Pre-orders exceed 2,000 units.

AI PARTNERSHIP
Collaborating with QuantumLeap on next-generation AI chips for robotics. Custom chip expected to deliver 5x performance improvement for vision and control systems.

FACTORY EXPANSION
Breaking ground on new manufacturing facility in Texas. Capacity will increase by 40% when completed in 2024.
""")
    document_count += 1

    # AeroSpace Technologies
    with open(os.path.join(docs_folder, "aerospace_tech_annual_2022.txt"), "w") as f:
        f.write("""
AEROSPACE TECHNOLOGIES (AERO)
FORM 10-K (ANNUAL REPORT)
For the fiscal year ended December 31, 2022

COMPANY OVERVIEW
AeroSpace Technologies designs and manufactures commercial aircraft, defense systems, and space exploration vehicles.

FINANCIAL SUMMARY
Revenue: $32.5 billion
Commercial aviation: $18.2 billion
Defense systems: $10.5 billion
Space systems: $3.8 billion
Gross margin: 16.5%
Operating income: $2.8 billion
Net income: $2.1 billion
Earnings per share: $4.15

BACKLOG
Total backlog: $95 billion
Commercial: $52 billion
Defense: $35 billion
Space: $8 billion

MAJOR PROGRAMS
A-350 commercial aircraft: 450 deliveries
F-35 component manufacturing: $2.5 billion revenue
Satellite systems: 25 satellites delivered
Space launch vehicles: 12 launches

AI APPLICATIONS
- Autonomous flight systems for unmanned aircraft
- Predictive maintenance using sensor data
- Manufacturing quality control with computer vision
- Supply chain optimization and risk management

SUSTAINABILITY
Developing hydrogen-powered aircraft with target entry into service 2035. Reduced manufacturing emissions by 25% since 2020.
""")
    document_count += 1

    with open(os.path.join(docs_folder, "aerospace_tech_q1_2023.txt"), "w") as f:
        f.write("""
AEROSPACE TECHNOLOGIES (AERO)
FORM 10-Q (QUARTERLY REPORT)
For the quarterly period ended March 31, 2023

FINANCIAL HIGHLIGHTS
Revenue: $8.7 billion
Commercial: $4.9 billion
Defense: $2.8 billion
Space: $1.0 billion
Operating income: $820 million
Net income: $610 million

DELIVERIES
Commercial aircraft: 115 units
Defense systems: $680 million
Satellites: 8 units

AI MILESTONE
Successfully demonstrated fully autonomous flight of unmanned aircraft using AI pilot system. System handled emergency situations and air traffic integration without human intervention.

NEW CONTRACT
Awarded $2.5 billion contract for military surveillance aircraft. Program will span 5 years with options for additional systems.
""")
    document_count += 1

    # ============================================
    # 7. АНАЛИТИЧЕСКИЕ ОТЧЕТЫ ПО СЕКТОРАМ
    # ============================================

    # AI in Healthcare Report
    with open(os.path.join(docs_folder, "ai_healthcare_report.txt"), "w") as f:
        f.write("""
ARTIFICIAL INTELLIGENCE IN HEALTHCARE
Market Analysis Report 2023
HealthTech Insights

EXECUTIVE SUMMARY
The global AI in healthcare market reached $25 billion in 2022 and is projected to grow at 38% CAGR to $188 billion by 2030. Key applications include drug discovery, diagnostics, personalized medicine, and administrative automation.

KEY SEGMENTS

Drug Discovery (35% market share)
AI reduces drug discovery time by 40-50% and costs by 30-40%. Major players include BioVita, GenoMedix, and PharmaAI. Over 150 AI-discovered compounds are in clinical trials.

Medical Imaging (25% market share)
AI-powered diagnostics achieve accuracy comparable to specialist physicians. Applications include radiology, pathology, and ophthalmology. Market leaders include MediScan AI, RadioLogix, and VisionMed.

Personalized Medicine (20% market share)
AI analyzes genomic data to identify optimal treatments. Growing adoption in oncology and rare diseases. Key players include GeneCounsel, OncoAI, and PrecisionHealth.

Administrative Applications (15% market share)
AI automates scheduling, billing, and prior authorization. Reduces administrative costs by 20-30%. Leaders include HealthFlow, MediBilling AI, and CareAdmin.

Wearables and Remote Monitoring (5% market share)
AI analyzes data from wearables for early disease detection. Rapidly growing segment with entrants from consumer tech companies.

REGULATORY LANDSCAPE
FDA has approved over 200 AI-enabled medical devices. New regulatory pathways being developed for adaptive AI algorithms that learn from real-world data.

INVESTMENT TRENDS
VC investment in healthcare AI reached $12 billion in 2022. Top deals included BioVita's $500 million AI partnership and GenoMedix's $300 million Series C.

FUTURE OUTLOOK
Generative AI will transform healthcare with applications in clinical documentation, patient communication, and treatment planning. Companies investing in AI capabilities will gain competitive advantage.
""")
    document_count += 1

    # Autonomous Vehicles Report
    with open(os.path.join(docs_folder, "autonomous_vehicles_report.txt"), "w") as f:
        f.write("""
AUTONOMOUS VEHICLES MARKET REPORT 2023
AutoTech Research

MARKET OVERVIEW
The autonomous vehicle market reached $45 billion in 2022 and is projected to reach $350 billion by 2030 at 28% CAGR. Levels of autonomy:
- Level 2 (partial automation): 35% of new vehicles
- Level 3 (conditional automation): 5% of new vehicles
- Level 4 (high automation): Limited deployment in robotaxis
- Level 5 (full automation): Expected post-2030

KEY PLAYERS

AutoDrive Technologies: Leader in Level 2/3 systems with 25% market share. Partnerships with 12 major automakers.

SensorVision: Leading provider of LiDAR and sensor fusion. Customers include 8 of top 10 automakers.

MapMind: High-definition mapping for autonomous vehicles. Covers 5 million miles of road.

CloudNav: AI-powered navigation and path planning. Used by multiple robotaxi operators.

TECHNOLOGY TRENDS
- Sensor costs declining: LiDAR down 80% since 2018
- Compute requirements: 100+ TOPS for Level 3, 1000+ TOPS for Level 4
- AI training: Billions of miles simulated
- V2X communication: Growing deployment for safety

REGULATORY ENVIRONMENT
15 states have passed autonomous vehicle legislation. Federal guidelines being developed for interstate commerce. Insurance frameworks evolving for autonomous operation.

INVESTMENT IMPLICATIONS
Companies with vertical integration (hardware + software) best positioned. Partnerships with automakers critical for scale. Robotaxi operators represent high-risk/high-reward opportunity.
""")
    document_count += 1

    # Clean Energy Transition Report
    with open(os.path.join(docs_folder, "clean_energy_transition.txt"), "w") as f:
        f.write("""
CLEAN ENERGY TRANSITION REPORT 2023
GreenTech Analytics

MARKET SIZE
Global clean energy investment reached $1.1 trillion in 2022, up 25% from 2021. Sectors include:
- Renewable energy: $500 billion
- Energy storage: $150 billion
- Electric vehicles: $350 billion
- Hydrogen: $50 billion
- Carbon capture: $50 billion

RENEWABLE ENERGY
Solar installations: 250 GW in 2022, cumulative 1.2 TW
Wind installations: 100 GW in 2022, cumulative 900 GW
Levelized cost of energy (LCOE):
- Solar: $30-50/MWh
- Wind: $40-60/MWh
- Gas: $60-80/MWh
- Coal: $70-100/MWh

ENERGY STORAGE
Battery installations: 50 GWh in 2022
Lithium-ion costs: $150/kWh (down 80% since 2010)
Grid-scale projects: 25 GW in development
Duration requirements increasing for renewable integration

ELECTRIC VEHICLES
EV sales: 10 million units (14% market share)
Battery capacity: 450 GWh
Charging infrastructure: 2.7 million public chargers
EV battery costs: $140/kWh (cell), $160/kWh (pack)

COMPANY SPOTLIGHT
NovaStar Energy: Leading renewable developer with 6.5 GW operating
GreenFuture Renewables: 4.7 GW operating, 9.8 GW pipeline
QuantumLeap: AI chips for grid optimization
Industrial Dynamics: Automation for battery manufacturing

INVESTMENT THESIS
Clean energy transition requires $4 trillion annual investment by 2030. Opportunities in renewable development, storage manufacturing, grid modernization, and enabling technologies like AI and automation.
""")
    document_count += 1

    # ============================================
    # 8. МАКРОЭКОНОМИЧЕСКИЕ ОТЧЕТЫ
    # ============================================

    # Global Economic Outlook
    with open(os.path.join(docs_folder, "global_economic_outlook.txt"), "w") as f:
        f.write("""
GLOBAL ECONOMIC OUTLOOK 2023-2025
International Finance Institute

GDP GROWTH FORECASTS
2023: 2.8% (down from 3.4% in 2022)
2024: 3.1%
2025: 3.3%

Regional breakdown 2023:
United States: 1.8%
Eurozone: 0.7%
China: 5.2%
Japan: 1.2%
India: 6.1%
Brazil: 1.5%
Russia: -0.8%

INFLATION OUTLOOK
Global inflation expected to moderate from 7.5% in 2022 to 4.5% in 2023 and 3.2% in 2024. Core inflation remains sticky due to services and wage pressures.

INTEREST RATES
Major central banks nearing peak rates:
Federal Reserve: 5.25-5.50%
ECB: 3.75%
BOE: 4.50%
BOJ: -0.10% (unchanged)

LABOR MARKETS
Unemployment near historic lows in major economies. Labor force participation recovering but still below pre-pandemic levels. Wage growth averaging 4-5% in developed economies.

TRADE AND GLOBALIZATION
Trade growth slowing to 2.5% in 2023 from 5.0% in 2022. Supply chains diversifying with "China+1" strategies. Near-shoring trends in North America and Europe.

GEOPOLITICAL RISKS
- Russia-Ukraine conflict continues
- US-China tensions over technology
- Middle East regional instability
- Climate change impacts on agriculture

INVESTMENT IMPLICATIONS
Defensive sectors preferred in near term. Technology and AI remain long-term growth areas. Emerging markets offer value but with higher risk.
""")
    document_count += 1

    # Technology Investment Outlook
    with open(os.path.join(docs_folder, "technology_investment_outlook.txt"), "w") as f:
        f.write("""
TECHNOLOGY INVESTMENT OUTLOOK 2023
TechVest Research

SECTOR PERFORMANCE 2022
Software: -25% return
Semiconductors: -35% return
Hardware: -20% return
Internet: -40% return
Relative to S&P 500: -18% underperformance

2023 OUTLOOK BY SEGMENT

AI and Machine Learning
Revenue growth: 30-35%
Key beneficiaries: TechNova, QuantumLeap, DataStream AI
Investment theme: Generative AI monetization

Cloud Computing
Revenue growth: 20-25%
Key beneficiaries: TechNova, CloudScale, DataCore
Investment theme: Enterprise optimization

Cybersecurity
Revenue growth: 15-20%
Key beneficiaries: SecureNet, CyberGuard, FireWall Inc.
Investment theme: Zero trust architecture

Semiconductors
Revenue growth: 5-10%
Key beneficiaries: QuantumLeap, ChipWorks, Silicon Dynamics
Investment theme: AI accelerators and automotive chips

Digital Payments
Revenue growth: 12-15%
Key beneficiaries: PayFlow, DigitalWallet, Transact Global
Investment theme: Embedded finance

TOP PICKS FOR 2023

TechNova (TNVA)
- Leader in cloud and AI
- Strong competitive position
- Valuation: 25x forward earnings
- Price target: $180 (25% upside)

QuantumLeap (QLEAP)
- Dominant in AI chips
- Quantum computing optionality
- Valuation: 30x forward earnings
- Price target: $95 (30% upside)

SecureNet (SNET)
- Best-in-class cybersecurity
- Recurring revenue model
- Valuation: 35x forward earnings
- Price target: $220 (20% upside)

RISKS
- Valuation multiples compressed by higher rates
- Slowing enterprise IT spending
- Regulatory scrutiny of large tech
- Geopolitical tensions affecting supply chains
""")
    document_count += 1

    logger.info(f"✅ Создано {document_count} примеров документов в папке {docs_folder}")
    return docs_folder


def main():
    """Основная функция для загрузки документов в RAG"""
    logger.info("=" * 60)
    logger.info("FinGuard AI - Загрузка документов в базу знаний RAG")
    logger.info("=" * 60)

    # ВСЕГДА создаем новые документы (удаляем старую папку если есть)
    docs_folder = "./financial_docs"

    # Опционально: спросить пользователя
    if os.path.exists(docs_folder):
        logger.info("📝 Папка с документами существует. Создаю новые документы...")
        import shutil
        shutil.rmtree(docs_folder)  # Удаляем старую папку

    logger.info("📝 Создание примеров финансовых документов...")
    docs_folder = create_sample_documents()

    # Загружаем документы
    logger.info(f"📂 Загрузка документов из {docs_folder}...")
    num_chunks = rag_db.load_documents_from_folder(docs_folder)

    if num_chunks > 0:
        logger.info(f"✅ Успешно загружено {num_chunks} чанков в базу знаний!")

        # Показываем статистику
        stats = rag_db.get_stats()
        logger.info(f"📊 Статистика базы знаний: {stats}")

        # Тестовый поиск
        logger.info("\n🔍 Тестовый поиск по запросу 'AI strategy'...")
        results = rag_db.search("AI strategy", k=2)
        for i, result in enumerate(results, 1):
            logger.info(f"\nРезультат {i}:\n{result[:300]}...")
    else:
        logger.error("❌ Не удалось загрузить документы")

if __name__ == "__main__":
    main()