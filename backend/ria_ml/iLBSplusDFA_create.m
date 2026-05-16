function iLBSplusDFA = iLBSplusDFA_create( )
  % creates a data structure for a combination of lockbox spending
  %   and a deferred fixed annuity
  
  % lockbox proportions (matrix with TIPS in top row, market in bottom row
     iLBSplusDFA.lockboxProportions = [ ];
  
  % number of years of lockbox income
      iLBSplusDFA.numberOfLockboxYears = 20;
      
  % lockbox bequest utility ratio
      iLBSplusDFA.bequestUtilityRatio = 0.50;
  
  % percentile of last lockbox year income distribution for fixed annuity
  %  100=lowest income; 50=median income, 0=highest income
      iLBSplusDFA.percentileOfLastLockboxYear = 50;
      
  % fixed annuity ratio of value to initial cost
     iLBSplusDFA.annuityValueOverCost = 0.90;
  
  % total amount invested
     iLBSplusDFA.amountInvested = 100000;
  
end
