function AMDnLockboxes = AMDnLockboxes_create( );
  % creates an AMDn lockboxes data structure
  
  % year of cumulative market return distribution to approximate (n)
  % note: n must be greater or equal to 2
     AMDnLockboxes.cumRmDistributionYear = 2;

  % lockbox proportions (computed by AMDnLockboxes_process)
     AMDnLockboxes.proportions = [ ];
     
  % show lockbox contents (y or n)
     AMDnLockboxes.showProportions = 'n';

end      