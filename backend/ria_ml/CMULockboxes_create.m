function CMULockboxes = CMULockboxes_create( );
  % creates a CMU lockboxes data structure
  
    % initial lockbox market proportion: 0 to 1.0 inclusive
       CMULockboxes.initialMarketProportion = 1.0;
       
    % lockbox proportions (computed by CMULockboxes_process)
       CMULockboxes.proportions = [ ];   
       
    % show lockbox contents (y or n)
       CMULockboxes.showProportions = 'n';
       
end        