% SmithCase_Chapter16.m

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

% create social security accounts
  iSocialSecurity = iSocialSecurity_create( );
  iSocialSecurity.state1Incomes = [Inf    30000];
  iSocialSecurity.state2Incomes = [Inf    30000];
  iSocialSecurity.state3Incomes = [44000];
% process social security accounts
  client = iSocialSecurity_process(iSocialSecurity, client, market);

% create and process AMDnLockboxes
   AMDnLockboxes = AMDnLockboxes_create( );
   AMDnLockboxes.cumRmDistributionYear = 2;
   AMDnLockboxes.showProportions = 'y';
   AMDnLockboxes = AMDnLockboxes_process(AMDnLockboxes, market, client);

% create iLBAnnuity
  iLBAnnuity = iLBAnnuity_create;
% set iLBAnnuity cost
  iLBAnnuity.cost = 1000000;
% set annuity lockbox proportions  
  iLBAnnuity.proportions =  AMDnLockboxes.proportions;
% process LBAnnuity
  client = iLBAnnuity_process(iLBAnnuity, client, market);

% create analysis
   analysis = analysis_create( );  
   
% reset analysis parameters
   analysis.animationDelays = [0.5 .5];
   analysis.animationShadowShade = .2;
   
 
   analysis.figuresCloseWhenDone = 'n';
   analysis.stackFigures = 'n';
   analysis.figureDelay = 0;

   analysis.plotIncomeDistributions = 'y';
   analysis.plotIncomeDistributionsTypes = {'rc'};     
   analysis.plotIncomeDistributionsStates = {[3]  [1 2]};
   analysis.plotIncomeDistributionsProportionShown = 0.999;


   analysis.plotYOYIncomes = 'y';
   analysis.plotYOYIncomesTypes = {'r'};
   analysis.plotYOYIncomesStates = {[3] [1 2]};

  
   analysis.plotScenarios = 'y';
   analysis.plotScenariosTypes = {'ri'};
   analysis.plotScenariosNumber = 20;
  
   analysis.plotRecipientPVs = 'y';

   analysis.plotIncomeMaps = 'y';
   analysis.plotIncomeMapsTypes = {'r'};
   analysis.plotIncomeMapsStates = {[3] [1 2]};
 

 
   analysis.plotPPCSandIncomes = 'y';
   analysis.plotPPCSandIncomesSemilog = 'n';
   analysis.plotPPCSandIncomesStates = {[3] [1 2] };
 
   
   analysis.plotYearlyPVs = 'y';
   analysis.plotYearlyPVsStates = {[3] [1 2]};
  
   

% produce analysis
  analysis_process(analysis, client, market);
 
   