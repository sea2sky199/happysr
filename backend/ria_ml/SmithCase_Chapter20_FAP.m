% SmithCase_Chapter20_FAP.m
% Lockbox Spending plus future annuity purchase

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

% create iLBSplusFAP
  iLBSplusFAP = iLBSplusFAP_create;
  iLBSplusFAP.lockboxProportions = AMDnLockboxes.proportions;
  
% set proportions in FAP lockbox to those in the last spending lockbox  
  yr = iLBSplusFAP.annuitizationYear;  
  props = iLBSplusFAP.lockboxProportions(:,yr-1);  
  iLBSplusFAP.FAPlockboxProportionInTIPS = props(1)/(props(1)+props(2));
% process iLBSplusFAP  
   [client, iLBSplusFAP]  = iLBSplusFAP_process(client,iLBSplusFAP, market );  

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
 
   analysis.plotYearlyPVs = 'y';
   analysis.plotYearlyPVsStates = {[3 1 2]};
   
   analysis.plotRecipientPVs = 'y';
     
% process analysis  
   analysis_process(analysis, client, market)
   

  
