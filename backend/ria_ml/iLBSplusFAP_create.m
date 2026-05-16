function iLBSplusFAP = iLBSplusFAP_create( )
  % creates a data structure for a combination of lockbox spending
  %   and future purchase of an annuity
  
  % lockbox proportions (matrix with TIPS in top row, market in bottom row
     iLBSplusFAP.lockboxProportions = [ ];
     
  % lockbox spending bequest utility ratio for spending
      iLBSplusFAP.bequestUtilityRatio = 0.50;
  
  % year in which annuity is to be purchased
      iLBSplusFAP.annuitizationYear = 20;
      
   % set initial proportion in TIPS for lockbox to be used to purchase annuity   
     iLBSplusFAP.FAPlockboxProportionInTIPS = 0.50;
      
   % annuity ratio of value to initial cost
     iLBSplusFAP.annuityValueOverCost = 0.90;
  
   % percentile of income distribution to match for FAP and last 
   %   spending lockbox (0 to 100)
      iLBSplusFAP.incomePercentileToMatch = 75;
  
  % total amount invested
     iLBSplusFAP.amountInvested = 100000;
  
end
