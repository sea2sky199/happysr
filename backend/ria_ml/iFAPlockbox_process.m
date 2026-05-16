function client  = iFAPlockbox_process(client, iFAPlockbox, market );   
  % processes an iFAPlockbox data structure
  % creating a future real annuity with constant payments as long as
  %   anyone is alive
  
  % compute annual real income per dollar depending on personal state
  %   when annuity is purchased
  % find mortality rates in future year (if alive)
     FAPyear = iFAPlockbox.yearOfAnnuityPurchase;
     mortP1 = client.mortP1;
     mortP1 = mortP1(FAPyear+1:length(mortP1));
     mortP2 = client.mortP2;
     mortP2 = mortP2(FAPyear+1:length(mortP2));
  % compute probabilities of payment for each initial personal state
    % probability of payment each year if only 1 is alive at outset
      probP1Alive = cumprod(1-mortP1);
    % probability of payment each year if only 2 is alive at outset
      probP2Alive = cumprod(1-mortP2);
    % probability of payment if both alive at outset and payment is made
    %   when either or both are alive
      probBothDead =(1-probP1Alive).*(1-probP2Alive);
      probPayment1 = probP1Alive;
      probPayment2 = probP2Alive;
      probPayment3 = 1 - probBothDead;
  %  add an initial payment of $1 at the beginning of first year
      probPayment1 = [1 probPayment1];
      probPayment2 = [1 probPayment2];
      probPayment3 = [1 probPayment3];

  % find discounted sum of payments
      n = length(probPayment1);
      dfs = market.rf.^[0:n-1];
      pvs = 1./dfs;
      valuePerDollar1 = sum(probPayment1.*pvs);   
      valuePerDollar2 = sum(probPayment2.*pvs);   
      valuePerDollar3 = sum(probPayment3.*pvs); 
  % find costs of annuities for initial personal states   
      valOverCost = iFAPlockbox.annuityValueOverCost;
      costPerDollar1 = valuePerDollar1 / valOverCost;
      costPerDollar2 = valuePerDollar2 / valOverCost;
      costPerDollar3 = valuePerDollar3 / valOverCost;
 
  % create values available to purchase annuity
      tipsProp = iFAPlockbox.proportionInTIPS;
      if tipsProp > 1; tipsProp = 1; end;
      if tipsProp < 0; tipsProp = 0; end;
      tipsAmt = tipsProp * iFAPlockbox.investedAmount;
      mktAmt  = iFAPlockbox.investedAmount - tipsAmt;
      mktVals =  mktAmt * market.cumRmsM(:,FAPyear);
      tipsVals = tipsAmt* market.cumRfsM(:,FAPyear);
      totVals = mktVals + tipsVals; 
    
  % create annuity payments and fees vectors
    [nscen nyrs] = size(client.incomesM); 
    annPayments = zeros(nscen,1);
    feesV = zeros(nscen,1);
    ii = find(client.pStatesM(:,FAPyear) == 1);
      annPayments(ii) =  totVals(ii)./costPerDollar1;
      feesV(ii) = (1 - valOverCost)*totVals(ii); 
    ii = find(client.pStatesM(:,FAPyear) == 2);
      annPayments(ii) =  totVals(ii)./costPerDollar2;
      feesV(ii) = (1 - valOverCost)*totVals(ii);
    ii = find(client.pStatesM(:,FAPyear) == 3);
      annPayments(ii) =  totVals(ii)./costPerDollar3;
      feesV(ii) = (1 - valOverCost)*totVals(ii);
 
  % create incomes matrix 
    incsM = zeros(nscen,nyrs);
  % add payments in FAPyear
    incsM(:,FAPyear) = annPayments;
  % add payments for years after FAPyear  
    for yr = FAPyear+1:nyrs
       ps = client.pStatesM(:,yr); 
       v =  (ps>0) & (ps<4);
       incsM(:,yr) = v.*annPayments;
    end;      
 
  % create fees matrix  
    feesM = zeros(nscen,nyrs);
    feesM(:,FAPyear) = feesV;
    
  % find payments to estate before FAPyear
     marketValsM = mktAmt * market.cumRmsM;
     tipsValsM  =  tipsAmt * market.cumRfsM;
     totValsM = marketValsM + tipsValsM;
     totValsM(:,FAPyear+1:nyrs) = 0;
     estatePaidM =  client.pStatesM == 4;
     amtsPdM = totValsM .* estatePaidM;
  
  % add incomes and amounts paid to client incomes
     client.incomesM = client.incomesM + incsM + amtsPdM;
  % add fees to client fees
     client.feesM = client.feesM  + feesM;

end