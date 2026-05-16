function iLBAnnuity = iLBAnnuity_create( );
   % create a Lockbox Annuity data structure 
   % uses only TIPS and market holdings
   
   % relative payments from lockboxes (2* client number of years)
   %   row 1: tips
   %   row 2: market portfolio 
       iLBAnnuity.proportions = [ ];
   
   % first income year
       iLBAnnuity.firstIncomeYear = 1;
   % relative incomes for personal states 1,2,3 and 4
       iLBAnnuity.pStateRelativeIncomes = [0.5 0.5 1.0 0]; 
   % graduation ratio of each real income distribution relative to the prior
   % distribution
       iLBAnnuity.graduationRatio = 1.00;
   % retention ratio for investment returns for tips and market portfolio
   %   = 1 - expense ratio
   %   e.g. expense ratio = 0.10% per year,retentionRatio = 0.999
       iLBAnnuity.retentionRatios = [0.999 0.999];
   % ratio of value invested in lockboxes to initial cost
        iLBAnnuity.valueOverCost = 0.90;
   % cost 
       iLBAnnuity.cost = 100000;
end