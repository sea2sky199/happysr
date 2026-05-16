% SmithCase_Chapter14.m

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


% create social security 
   iSocialSecurity = iSocialSecurity_create( );
% incomes in state 1, last column repeated for subsequent years
   iSocialSecurity.state1Incomes = [Inf    30000];
% incomes in state 2, last column repeated for subsequent years
   iSocialSecurity.state2Incomes = [Inf    30000];                                   
% incomes for state 3, last column repeated for subsequent years
   iSocialSecurity.state3Incomes = [44000]; 
% process social security
   client = iSocialSecurity_process(iSocialSecurity, client, market); 
   
% create analysis
   analysis = analysis_create( );  
   analysis.plotRecipientPVs = 'y';
% process analysis   
   analysis_process(analysis, client, market);

   
 

  