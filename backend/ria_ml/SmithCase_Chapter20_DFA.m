% SmithCase_Chapter20_DFA.m
% lockbox spending plus deferred fixed annuity

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
   
% create AMD2 lockboxes   
  AMDnLockboxes = AMDnLockboxes_create( );
  AMDnLockboxes.showProportions = 'y';
  AMDnLockboxes = AMDnLockboxes_process(AMDnLockboxes, market, client);

% create iLockboxSpending plus deferred fixed annuity
  iLBSplusDFA = iLBSplusDFA_create( );
  iLBSplusDFA.numberOfLockboxYears = 20;
  iLBSplusDFA.bequestUtilityRatio = 0.50;
  iLBSplusDFA.percentileOfLastLockboxYear = 50;
  iLBSplusDFA.annuityValueOverCost = 0.90;
  iLBSplusDFA.amountInvested = 1000000;
% set lockbox proportions  
  iLBSplusDFA.lockboxProportions = AMDnLockboxes.proportions;
  

% process LockboxSpending  
  [client, iLBSplusDFA]  = iLBSplusDFA_process(client,iLBSplusDFA, market );   

 % create analysis 
   analysis = analysis_create; 

   analysis.plotScenarios = 'y';
   analysis.plotScenariosTypes = {'ri'};
   analysis.plotScenariosNumber = 20;

   analysis.plotIncomeDistributions = 'y';
   analysis.plotIncomeDistributionsTypes = {'rc'};     
   analysis.plotIncomeDistributionsStates = { [3 1 2] };
   analysis.plotIncomeDistributionsMinPctScenarios =0.5;
   analysis.plotIncomeDistributionsPctMaxIncome = 50;
 
   analysis.plotRecipientPVs = 'n';
  
   analysis.plotYearlyPVs = 'y';
   analysis.plotYearlyPVsStates = {[3 1 2]};
   
   analysis.plotRecipientPVs = 'y';
     
% process analysis  
   analysis_process(analysis, client, market)
   

  
