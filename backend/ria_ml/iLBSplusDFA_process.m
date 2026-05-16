function [client, iLBSplusDFA]  = iLBSplusDFA_process(client,iLBSplusDFA, market );   
  % process lockbox spending plus deferred fixed annuity 
  
  % create deferred fixed annuity with cost equal to 50% of total 
       iFixedAnnuity = iFixedAnnuity_create();
    % set deferral period  
       nLByrs = iLBSplusDFA.numberOfLockboxYears;
       iFixedAnnuity.guaranteedIncomes = zeros(1,nLByrs);
    % set relative incomes equal for personal states 1,2 and 3 
       iFixedAnnuity.pStateIncomes = [0 1 1 1 0]; 
    % set incomes constant 
       iFixedAnnuity.graduationRatio = 1.00;
    % set type of income to real;   
       iFixedAnnuity.realOrNominal = 'r';
    % set ratio of value to initial cost
       iFixedAnnuity.valueOverCost = iLBSplusDFA.annuityValueOverCost;
    % cost 
       iFixedAnnuity.cost = 0.50*iLBSplusDFA.amountInvested;
    % create a temporary client with zero incomes
       clientTemp = client;
       [nscen nyrs] = size(clientTemp.incomesM);
       clientTemp.incomesM = zeros(nscen,nyrs);
    % process deferred fixed annuity with temporary client 
       clientTemp = iFixedAnnuity_process(iFixedAnnuity, clientTemp, market);
    % find annuity real income per dollar invested   
       annuityIncomePerDollar = max(max(clientTemp.incomesM))/iFixedAnnuity.cost;
       
  % create lockbox spending with cost equal to 50% of total
     iLockboxSpending =  iLockboxSpending_create( ); 
     % set lockbox proportions for selected number of years 
       props = iLBSplusDFA.lockboxProportions(:,1:nLByrs);
       iLockboxSpending.lockboxProportions = props;
     % set initial investment 
       iLockboxSpending.investedAmount = 0.50*iLBSplusDFA.amountInvested;
     % bequest utility ratio
       iLockboxSpending.bequestUtilityRatio=iLBSplusDFA.bequestUtilityRatio;
     % show lockbox amounts (y or n)
       iLockboxSpending.showLockboxAmounts = 'n';  
     % create a new temporary client with zero incomes
       clientTemp = client;  
       [nscen nyrs] = size(clientTemp.incomesM);
       clientTemp.incomesM = zeros(nscen,nyrs);
     % process lockbox spending with temporary client 
       [clientTemp,iLockboxSpending] = iLockboxSpending_process(iLockboxSpending, clientTemp, market);
     % find incomes in final year per dollar invested
        pstates = clientTemp.pStatesM(:,nLByrs);
        ii = find((pstates>0) & (pstates<4));
        incs =    clientTemp.incomesM(ii,nLByrs);
        incs = sort(incs,'descend');
        incsPerDollar = incs/iLockboxSpending.investedAmount;
        numIncsPerDollar = length(incsPerDollar);
     % find percentile of income in final year per dollar invested 
        pctl = iLBSplusDFA.percentileOfLastLockboxYear;
        incNum = round(.01*pctl*numIncsPerDollar);
        if incNum<1; incNum = 1; end;
        if incNum>numIncsPerDollar; incNum = numIncsPerDollar; end;
        LBIncomePerDollar = incsPerDollar(incNum);
    
  % find amounts to invest in lockbox and deferred annuity   
     r = annuityIncomePerDollar/(LBIncomePerDollar+annuityIncomePerDollar);
     LBInvestment  =  r*iLBSplusDFA.amountInvested;
     DFAInvestment =  iLBSplusDFA.amountInvested - LBInvestment;
       
  % create incomes from deferred fixed annuity
     clientTemp = client;  
     [nscen nyrs] = size(clientTemp.incomesM);
     iFixedAnnuity.cost = DFAInvestment;
     clientTemp = iFixedAnnuity_process(iFixedAnnuity, clientTemp, market);
     DFAincsM = clientTemp.incomesM;
     feesM = clientTemp.feesM;
            
  % create incomes from lockbox spending   
     clientTemp = client;  
     [nscen nyrs] = size(clientTemp.incomesM);
     clientTemp.incomesM = zeros(nscen,nyrs);
     iLockboxSpending.investedAmount= LBInvestment;
     [clientTemp,iLockboxSpending] = iLockboxSpending_process(iLockboxSpending, clientTemp, market);
     LBincsM = clientTemp.incomesM;
     
  % add amounts invested to iLBSplusDFA data structure
     iLBSplusDFA.DFAInvestment = DFAInvestment;
     iLBSplusDFA.LBInvestment =  LBInvestment;
     
  % add incomes to client income matrix
     client.incomesM = client.incomesM + DFAincsM + LBincsM;
     client.feesM = client.feesM + feesM;
       
end
