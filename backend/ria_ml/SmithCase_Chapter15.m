% SmithCase_Chapter15.m

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

% create and process AMDnLockboxes
   AMDnLockboxes = AMDnLockboxes_create( );
   AMDnLockboxes.showProportions = 'y';
   AMDnLockboxes = AMDnLockboxes_process(AMDnLockboxes, market, client);
     
% create and process CMULockboxes
   CMULockboxes = CMULockboxes_create( );
   CMULockboxes.showProportions = 'y';
   CMULockboxes = CMULockboxes_process(CMULockboxes, market, client);
  

% create and process combined lockboxes
   combinedLockboxes = combinedLockboxes_create( );
   combinedLockboxes.componentLockboxes = {AMDnLockboxes CMULockboxes};
   combinedLockboxes.componentWeights = [0.5 0.5];
   combinedLockboxes.showCombinedProportions = 'y';
   combinedLockboxes = combinedLockboxes_process(combinedLockboxes, client); 
   
