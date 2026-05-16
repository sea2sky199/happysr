function iConstSpending = iConstSpending_create( )
  % create a constant spending income data structure

  % amount invested
     iConstSpending.investedAmount = 100000;   

  % proportion of initial investment spent in first year
       iConstSpending.initialProportionSpent = 0.040;
     
   % relative incomes for personal states 1,2 and 3 
   %   (any remaining value is paid in personal state 4)
       iConstSpending.pStateRelativeIncomes = [0.5 0.5 1.0 ]; 
       
              
   % graduation ratio of each real income relative to the prior income
   % distribution
       iConstSpending.graduationRatio = 1.00;
          
     
  % matrix of points on market proportion glide path graph
  % top row is y: market proportions (between 0.0 and 1.0 inclusive)
  %   bottom row is x: years (first must be 1 or greater)
  % first proportion applies to years up to and at first year
  % last proportion applies to years at and after last year
  % proportions between two years are interpolated linearly 
      iConstSpending.glidePath = [1.0 ; 1 ];
       
   % show glide path (y or n)
       iConstSpending.showGlidePath = 'n';
       
   % retention ratio for investment returns for portfolio
   %   = 1 - expense ratio
   %   e.g. expense ratio = 0.10% per year,retentionRatio = 0.999
       iConstSpending.retentionRatio = 0.999;
       
       
end
