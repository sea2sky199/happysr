% SmithCase_Chapter20_LBS.m
% lockbox spending

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
  AMDnLockboxes.showProportions = 'n';
  AMDnLockboxes = AMDnLockboxes_process(AMDnLockboxes, market, client);

% create iLockboxSpending
  iLockboxSpending = iLockboxSpending_create();
  iLockboxSpending.lockboxProportions = AMDnLockboxes.proportions;
  iLockboxSpending.bequestUtilityRatio = 0.5;
  LockboxSpending.showLockboxAmounts = 'y';

% process LockboxSpending  
   [client iLockboxSpending] = iLockboxSpending_process(iLockboxSpending, client, market);

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
