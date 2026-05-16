% SmithCase_Chapter12.m

% clear all previous variables and close any figures
   clear all;
   close all;

% create a new client data structure
   client = client_create();
% process the client data structure
   client = client_process(client);

% create a new market data structure
   market = market_create( );
% process the client data structure
   market = market_process(market,client);

% create fixed nominal Annuity
   iFixedAnnuity = iFixedAnnuity_create;
   iFixedAnnuity.realOrNominal = 'n';
% process fixed annuity
   client  = iFixedAnnuity_process(iFixedAnnuity, client, market);

% create analysis
   analysis = analysis_create( );

% plot scenarios
   analysis.plotScenarios = 'n';
   analysis.plotScenariosTypes = {'rie'};
   analysis.plotScenariosNumber = 10;

% plot income distributions
   analysis.plotIncomeDistributions = 'y';
   analysis.plotIncomeDistributionsTypes = {'rc' 'ru' };
   analysis.plotIncomeDistributionsStates = { [3] };
   analysis.plotIncomeDistributionsMinPctScenarios = 0.5;

% plot income maps
   analysis.plotIncomeMaps = 'y';
   analysis.plotIncomeMapsTypes = {'ru' 'rc'};
   analysis.plotIncomeMapsStates = {[3]};
   analysis.plotIncomeMapsMinPctScenarios = 0.5;

% plot year-over-year incomes
   analysis.plotYOYIncomes = 'n';
   analysis.plotYOYIncomesTypes = {'r'};
   analysis.plotYOYIncomesStates = { [3] };

% process analysis
   analysis_process(analysis, client, market);





