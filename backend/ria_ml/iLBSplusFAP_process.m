function [client, iLBSplusFAP]  = iLBSplusFAP_process(client,iLBSplusFAP, market );   
  % process lockbox spending plus deferred fixed annuity 
  
  % create a temporary client
    clientTemp = client; 
  % process lockbox spending with 0.5 of the total amount invested
    iLockboxSpending = iLockboxSpending_create;
  % set lockbox proportions  
    iLockboxSpending.lockboxProportions = iLBSplusFAP.lockboxProportions;
  % use lockbox spending up to and including the year before annuity purchase
    lastSpendingYr = iLBSplusFAP.annuitizationYear - 1; 
    iLockboxSpending.lockboxProportions = iLockboxSpending.lockboxProportions(:,1:lastSpendingYr); 
  % set bequest utility ratio
    iLockboxSpending.bequestUtilityRatio = iLBSplusFAP.bequestUtilityRatio;
  % do not show lockbox proportions  
     iLockboxSpending.showLockboxAmounts = 'n'; 
  % amount invested for lockbox spending  
     iLockboxSpending.investedAmount = 0.50*iLBSplusFAP.amountInvested;
  % process lockbox spending
     clientTemp = client; 
     [nscen nyrs] = size(client.incomesM);
     clientTemp.incomesM = zeros(nscen,nyrs);
     clientTemp = iLockboxSpending_process(iLockboxSpending, clientTemp, market);
  % find percentile income in last lockbox spending year for matching states
     ps = clientTemp.pStatesM(:,lastSpendingYr);
     ii = find((ps>0) & (ps<4));
     incs = clientTemp.incomesM(ii,lastSpendingYr);
     sortincs = sort(incs,'descend');
     matchPctl = iLBSplusFAP.incomePercentileToMatch;
     matchPctl = matchPctl/100;
     if matchPctl>1; matchPctl = 1; end;
     if matchPctl<0; matchPctl = 0; end;
     n = matchPctl*length(sortincs);
     n = round(n);
     if n>length(sortincs); n = length(sortincs); end;
     if n<1; n = 1; end;
     pctlIncSpending = sortincs(n);

  % create lockbox for future annuity purchase  
    iFAPlockbox = iFAPlockbox_create( );
  % set year annuity is to be purchased  
    iFAPlockbox.yearOfAnnuityPurchase  = iLBSplusFAP.annuitizationYear;
  % set initial proportion in TIPS in the FAPlockbox
    propTIPS = iLBSplusFAP.FAPlockboxProportionInTIPS;
    iFAPlockbox.proportionInTIPS = propTIPS;
  % set initial amount ($) in the lockbox
    iFAPlockbox.investedAmount = 0.50*iLBSplusFAP.amountInvested;
  % process FAP lockbox with temporary client
    clientTemp = client; 
    [nscen nyrs] = size(client.incomesM);
    clientTemp.incomesM = zeros(nscen,nyrs);
    clientTemp  = iFAPlockbox_process(clientTemp, iFAPlockbox, market );  
  % find percentile amount spent in first annuity  year matching states
     ps = clientTemp.pStatesM(:,lastSpendingYr+1);
     incs = clientTemp.incomesM(ii,lastSpendingYr+1);
     sortincs =  sort(incs,'descend');
     n = matchPctl*length(sortincs);
     n = round(n);
     if n>length(sortincs); n = length(sortincs); end;
     if n<1; n = 1; end;
     pctlIncAnnuity = sortincs(n); 
     
  % compute revised amounts to be invested
   % find incomes per dollar
     incomePerDollarSpending = pctlIncSpending / iLockboxSpending.investedAmount; 
     incomePerDollarAnnuity  = pctlIncAnnuity / iFAPlockbox.investedAmount; 
   % find proportions of total investment
     sum =  incomePerDollarSpending + incomePerDollarAnnuity;
     propSpending  =  incomePerDollarAnnuity / sum;
     propAnnuity =  incomePerDollarSpending /sum; 
   % find total amount invested
     totAmountInvested = iLockboxSpending.investedAmount + iFAPlockbox.investedAmount;
     
  % put amounts to be invested in data structures
     iLockboxSpending.investedAmount = propSpending * totAmountInvested;
     iFAPlockbox.investedAmount =      propAnnuity  * totAmountInvested;
  % add to iLBSplusFAP data structure
     iLBSplusFAP.spendingAmountInvested =  iLockboxSpending.investedAmount;
     iLBSplusFAP.FAPAmountInvested =      iFAPlockbox.investedAmount;
     
  % create incomes from lockbox spending   
     clientTemp = client;  
     [nscen nyrs] = size(clientTemp.incomesM);
     clientTemp.incomesM = zeros(nscen,nyrs);
     [clientTemp,iLockboxSpending] = iLockboxSpending_process(iLockboxSpending, clientTemp, market);
     
  % add incomes and fees from FAP
     clientTemp  = iFAPlockbox_process(clientTemp, iFAPlockbox, market );   
     
  % add incomes to client income matrix
     client.incomesM = client.incomesM + clientTemp.incomesM;
  % add fees to client fee matrix   
     client.feesM = client.feesM + clientTemp.feesM;
       
end
