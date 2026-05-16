% SmithCase_Chapter17.m

% clear all previous variables and close any figures
   clear all;
   close all;
   tic;
   
% create a new client data structure
   client = client_create();
% process the client data structure 
   client = client_process(client);
 
% create a new market data structure
   market = market_create( );
% process the client data structure
   market = market_process(market,client); 

% create social security accounts
  iSocialSecurity = iSocialSecurity_create( );
  iSocialSecurity.state1Incomes = [Inf    30000];
  iSocialSecurity.state2Incomes = [Inf    30000];
  iSocialSecurity.state3Incomes = [44000];
% process social security accounts
  client = iSocialSecurity_process(iSocialSecurity, client, market);
   
% create constant spending data structure
   iConstSpending = iConstSpending_create( );
   iConstSpending.glidePath = [1 ; 1];
   iConstSpending.retentionRatio = 0.999;
   iConstSpending.initialProportionSpent = 0.040;
   iConstSpending.graduationRatio = 1.00;
   iConstSpending.pStateRelativeIncomes = [1 1 1 ]; 
   iConstSpending.investedAmount = 1000000;   
   iConstSpending.showGlidePath = 'y';
% process the constant spending data structure   
   client = iConstSpending_process(iConstSpending, client, market);
 
%  create analysis
   analysis = analysis_create( );  
   
% reset analysis parameters
   analysis.animationDelays = [0.5 .5];
   analysis.animationShadowShade = 1;
  
   analysis.figuresCloseWhenDone = 'n';
   analysis.stackFigures = 'y';
   analysis.figureDelay = 0;

   analysis.plotScenarios = 'y';
   analysis.plotScenariosTypes = {'ri'}; 
   analysis.plotScenariosNumber = 20;

   analysis.plotRecipientPVs = 'y';
  
   analysis.plotYearlyPVs = 'y';
   analysis.plotYearlyPVsStates = {[1 2] [3]};

 
% produce analysis
   analysis_process(analysis, client, market);

    
 