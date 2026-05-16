% SmithCase_Chapter19.m

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
   
   
% create a new GLWB structure
   iGLWB = iGLWB_create( );
% process the GLWB data structure    
   [client iGLWB] = iGLWB_process(client, market, iGLWB);

   
% create analysis 
   analysis = analysis_create; 
   analysis.animationDelays = [1 0.5];

% scenarios   
   analysis.plotScenarios = 'y';
   analysis.plotScenariosTypes = {'ri'};
   analysis.plotScenariosNumber = 20;
   
   

   analysis.plotIncomeDistributions = 'y';
   analysis.plotIncomeDistributionsTypes = {'rc'};     
   analysis.plotIncomeDistributionsStates = { [3 1 2] };
   analysis.plotIncomeDistributionsMinPctScenarios =0.5;
   analysis.plotIncomeDistributionsPctMaxIncome = 50;
 
   analysis.plotYOYIncomes = 'n';
   analysis.plotYOYIncomesTypes = {'r'};
   analysis.plotYOYIncomesStates = {[3 1 2]};

  

   analysis.plotRecipientPVs = 'y';
  
   analysis.plotIncomeMaps = 'y';
   analysis.plotIncomeMapsTypes = {'rc'};
   analysis.plotIncomeMapsStates = {[3 1 2]};
   analysis.plotIncomeMapsMinPctScenarios = .5;
   analysis.plotIncomeMapsPctMaxIncome = 25;
      
      
   analysis.plotPPCSandIncomes = 'y';
   analysis.plotPPCSandIncomesSemilog = 'y';
   analysis.plotPPCSandIncomesStates = {[3 1 2] };
      
   analysis.plotYearlyPVs = 'y';
   analysis.plotYearlyPVsStates = {[3 1 2]};
   
   analysis.plotEfficientIncomes = 'n';
   analysis.plotEfficientIncomesStates = {[3 1 2]};
   analysis.plotEfficientIncomesTypes = {'pcl'}; 
   
      
% process analysis  
   analysis_process(analysis, client, market)

   

   

  