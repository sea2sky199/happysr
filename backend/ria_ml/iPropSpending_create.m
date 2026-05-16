function iPropSpending = iPropSpending_create( )
  % create a proportional spending income data structure

  % amount invested
       iPropSpending.investedAmount = 100000;   

      
  % use IRS Required Minimum Distributions (RMD) Life Expectancies (y or n)
       iPropSpending.useRMDlifeExpectancies = 'y';
  % if RMD not used, vector of life expectancies and age for first value
       iPropSpending.nonRMDlifeExpectancies = [ ];
       iPropSpending.nonRMDfirstLEAge = 70;
   
  % current age of portfolio owner
       iPropSpending.portfolioOwnerCurrentAge = 65;
        
  % show proportions spent (y or n)
       iPropSpending.showProportionsSpent = 'n';
       
  % show Lockbox equivalent initial investment values
       iPropSpending.showLockboxEquivalentValues = 'n';
       
        
  % matrix of points on portfolio market proportion glide path graph
  % top row is y: market proportions (between 0.0 and 1.0 inclusive)
  %   bottom row is x: years (first must be 1 or greater)
  % first proportion applies to years up to and at first year
  % last proportion applies to years at and after last year
  % proportions between two years are interpolated linearly 
      iPropSpending.glidePath = [1.0 ; 1 ];
       
  % show portfolio glide path (y or n)
       iPropSpending.showGlidePath = 'n';
       
  % retention ratio for portfolio investment returns 
  %   = 1 - expense ratio
  %   e.g. expense ratio = 0.10% per year,retentionRatio = 0.999
       iPropSpending.retentionRatio = 0.999;
   
end 