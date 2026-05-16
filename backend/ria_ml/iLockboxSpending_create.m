function iLockboxSpending =  iLockboxSpending_create( );
  % create a lockbox spending data structure
  
  % amount invested
     iLockboxSpending.investedAmount = 100000;   

  % relative payments from lockboxes: size(2,client number of years)
  %   row 1: tips
  %   row 2: market portfolio 
  % may be provided by AMDnLockboxes.proportions, CMULockboxes.proportions,
  %    combinedLickboxes.proportions or otherwise   
  % note: lockboxes are to be spent for personal states 1,2,3 or 4
     iLockboxSpending.lockboxProportions = [];
     
  % bequest utility ratio
  %  ratio of utility per dollar for bequest versus spending
  %  note: this applies equally for personal states 1,2 and 3
     iLockboxSpending.bequestUtilityRatio = 0.50;
     
  % show lockbox amounts (y or n)
     iLockboxSpending.showLockboxAmounts = 'y';
     
end

