function combinedLockboxes = combinedLockboxes_create( );
  % creates a lockbox by combining other lockboxes
  
     % lockboxes to be combined (data structures) 
       combinedLockboxes.componentLockboxes = {     };
      
     % proportions of lockboxes being combined
     %   one value for each lockbox; values greater than or equal to 0
     %   values will be normalized to sum to 1.0
       combinedLockboxes.componentWeights = [ ];
       
     % title of combined lockboxes
       combinedLockboxes.title = 'Combined Lockboxes';
       
     % combined lockboxes proportions produced by combinedLockboxes_process
       combinedLockboxes.proportions = [ ];
       
     % show combined lockbox contents (y or n)
       combinedLockboxes.showCombinedProportions = 'n';
       
end     