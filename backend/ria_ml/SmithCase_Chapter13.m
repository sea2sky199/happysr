% SmithCase_Chapter13.m

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

% plot recipient present values -- y (yes) or n (no)
   analysis.plotRecipientPVs  =  'y';   

   
% plot PPCs and Incomes -- y/n
   analysis.plotPPCSandIncomes = 'y';
% plot PPC and Incomes --  semilog or loglog
   analysis.plotPPCSandIncomesSemilog = 'y';
% plot PPCs and Incomes -- sets of states (one set per graph)
   analysis.plotPPCSandIncomesStates = { [3] };
% plot PPCs and Incomes: minimum percent of scenarios
   analysis.plotPPCSandIncomesMinPctScenarios = 0.5;
 
   
 % plot yearly present values -- y (yes) or n (no)
    analysis.plotYearlyPVs = 'y';
 % plot yearly present values-- sets of states (one set per graph)
    analysis.plotYearlyPVsStates = {[3] [1 2]};
 % plot yearly present values: minimum percent of scenarios
    analysis.plotYearlyPVsMinPctScenarios = 0.5;

 % plot efficient incomes -- y (yes) or n (no)
   analysis.plotEfficientIncomes = 'y';
 % plot efficient incomes -- sets of states (one set per graph)
   analysis.plotEfficientIncomesStates = {[3]};
 % plot points (actual) curves (efficient) and/or 
 %   lines (two-asset market-based strategies
 %   combinations of (p,c,l) -- one graph per type
   analysis.plotEfficientIncomesTypes = {'pcl'}; 
 % plot efficient incomes: minimum percent of scenarios
   analysis.plotEfficientIncomesMinPctScenarios = 0.5;
   

% process analysis  
   analysis_process(analysis, client, market);

   
 

  