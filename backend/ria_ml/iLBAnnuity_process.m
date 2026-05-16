
function client = iLBAnnuity_process(iLBAnnuity, client, market);
  % creates LB annuity income matrix and fees matrix
  % then adds values to client incomes matrix and fees matrices
  
  % the lockbox proportions matrix can be computed by AMDnLockboxes_process
  %   or in some other manner. The first row is TIPS proportions, the second is Market
  %   proportions, and there is a column for each year in the client matrix

  % get number of scenarios and years
     [nscen nyrs] = size(client.pStatesM);
  % set initial lockbox proportions
      proportions = iLBAnnuity.proportions;
   
  % reset proportions to adjust for graduation and retention ratios   
      gr =  iLBAnnuity.graduationRatio;
      rrs = iLBAnnuity.retentionRatios;
      for row = 1:2
        factors = (gr/rrs(row)).^(0:nyrs-1);
        proportions(row,:) = factors.*proportions(row,:);
      end;
   
  % set lockbox proportions to zero for any excluded years
      firstyear = iLBAnnuity.firstIncomeYear;
      if firstyear > 1
         proportions(:,1:firstyear-1) = zeros(2, firstyear-1);
      end;

   % create matrices of returns net of expenses
     NrfsM = iLBAnnuity.retentionRatios(1)*market.rfsM;
     NrmsM = iLBAnnuity.retentionRatios(2)*market.rmsM;
  % create cumulative returns net of expenses
     m = cumprod(NrfsM,2);
     cumNrfsM = [ones(nscen,1) m(:,1:nyrs-1)];
     m = cumprod(NrmsM,2);
     cumNrmsM = [ones(nscen,1) m(:,1:nyrs-1)];
     
     
  % create matrices with proportions in market and rf in each row
     xfm = ones(nscen,1)*proportions(1,:);
     xmm = ones(nscen,1)*proportions(2,:);
  % compute net incomes for lockbox relative proportions   
     boxIncsM  = xfm.*cumNrfsM + xmm.*cumNrmsM;
  % compute  incomes if there were no expenses
     gboxIncsM = xfm.*market.cumRfsM + xmm.*market.cumRmsM;
  % set fees to differences
     feesM = gboxIncsM - boxIncsM;
  
  % set up relative incomes matrix and relative fees matrix 
      psRelIncs = iLBAnnuity.pStateRelativeIncomes;
      psRelIncs = psRelIncs / max(psRelIncs);
      relIncsM = zeros(nscen,nyrs);
      relFeesM = zeros(nscen,nyrs);
      for ps = 1:4
         relInc =  psRelIncs(ps); 
         psmat =   (client.pStatesM == ps);
         psIncsM = relInc*(psmat.*boxIncsM);
         relIncsM = relIncsM + psIncsM; 
         psFeesM = relInc*(psmat.*feesM);
         relFeesM = relFeesM + psFeesM;
      end; % for ps = 1:4
      
              
   % convert relative incomes to dollar incomes
      pvbase = sum(sum( (relIncsM + relFeesM).*market.pvsM));
      totval = iLBAnnuity.cost * iLBAnnuity.valueOverCost;
      incsM =  relIncsM * (totval / pvbase);
      feesM =  relFeesM * (totval / pvbase);
 
   % add incomes and fees to client incomes and fees matrices   
      client.incomesM = client.incomesM + incsM;
      client.feesM    = client.feesM    + feesM;
         
   % add insurance fee to fee matrix
      insFee = iLBAnnuity.cost * (1 - iLBAnnuity.valueOverCost);  
      client.feesM(:,1) = client.feesM(:,1) + insFee; 
    
end 
         
 