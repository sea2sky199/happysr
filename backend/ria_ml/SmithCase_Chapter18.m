% SmithCase_Chapter18.m

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

% create proportional spending account  
   iPropSpending = iPropSpending_create( );
   iPropSpending.investedAmount = 1000000;
   iPropSpending.glidePath = [1  0 ; 0 30];
   iPropSpending.showGlidePath = 'y';
   iPropSpending.retentionRatio = 0.999;
% proces proportional spending account
   client = iPropSpending_process(iPropSpending, client, market);
   

% create analysis
   analysis = analysis_create( ); 
   
% change selected analysis settings 
   analysis.animationDelays = [.2 .2];
   
   analysis.plotIncomeDistributions = 'y';
   analysis.plotIncomeDistributionsTypes = {'rc'};     
   analysis.plotIncomeDistributionsStates = { [1 2 3] };
   analysis.plotIncomeDistributionsMinPctScenarios = 0.5;
 
   analysis.plotYOYIncomes = 'y';
   analysis.plotYOYIncomesTypes = {'r'};
   analysis.plotYOYIncomesStates = {[3 1 2]};

   analysis.plotScenarios = 'y';
   analysis.plotScenariosTypes = {'ri'};
   analysis.plotScenariosNumber = 20;
 
   analysis.plotRecipientPVs = 'y';
  
   analysis.plotIncomeMaps = 'y';
   analysis.plotIncomeMapsTypes = {'ru' 'rc'};
   analysis.plotIncomeMapsStates = {[3 1 2]};
   analysis.plotIncomeMapsMinPctScenarios = 0.5;
      
   analysis.plotPPCSandIncomes = 'y';
   analysis.plotPPCSandIncomesSemilog = 'y';
   analysis.plotPPCSandIncomesStates = {[3 1 2] };
      
   analysis.plotYearlyPVs = 'y';
   analysis.plotYearlyPVsStates = {[3 1 2]};
   
% process analysis
   analysis_process(analysis, client, market)

   
 

  