function [client iGLWB]  = iGLWB_process (client, market, iGLWB)
 
  % set parameters 
      initialValue = iGLWB.initialValue;
      expPropTWB =  iGLWB.expenseRatioOfTWB;
      expPropFund = iGLWB.expenseRatioOfFund;
      
  % find proportion of TWB to withdraw    
      minAge = min(client.p1Age, client.p2Age);
      if lower(iGLWB.singleOrJoint) == 'j';
         tbl = iGLWB.jointLifeWithdrawalRates;
      else
         tbl = iGLWB.singleLifeWithdrawalRates; 
      end; % if find(lower(iGLWB.singleOrJoint),'j') >0;
      rows = (minAge >= tbl(:,1)) & (minAge <= tbl(:,2));
      withdrawPropTWB = sum(rows.*tbl(:,3));
      
  % create matrix of nominal market returns
     nrmsM =  market.rmsM .* market.csM;
  
  % get matrix dimensions   
     [nscen nyrs] = size(client.incomesM);   
    
  % set initial portfolio value vector
     portvalV =  initialValue*ones(nscen,1);   
  % set vector of total withdrawal bases
     twbV = portvalV;  
     
  % create nominal incomes and nominal fees matrices
     incsM = zeros(nscen,nyrs);
     feesFundM = zeros(nscen,nyrs);
     feesRiderM = zeros(nscen,nyrs);
  
  % set initial year payouts
     incsM(:,1) =  withdrawPropTWB * twbV; 
  % adjust portfolio values
     portvalV = portvalV - incsM(:,1);
  % set initial year fees to zero 
     feesFundM(:,1)  =  zeros(nscen,1);
     feesRiderM(:,1) =  zeros(nscen,1);
    
  % do remaining years
     for yr = 2:nyrs
         
       % find scenarios in which one or two are alive
         ii = find((client.pStatesM(:,yr)>0) & (client.pStatesM(:,yr)<4));
         if length(ii)>0
            % increment nominal values of portolio 
              portvalV(ii) =  portvalV(ii).* nrmsM(ii,yr-1);
            % compute fees for fund and subtract from portfolio value
              feesFundM(ii,yr)  = expPropFund * portvalV(ii);
              portvalV(ii) = portvalV(ii) - feesFundM(ii,yr);
            % compute guaranteed withdrawals and add to incomes   
              incsM(ii,yr) = withdrawPropTWB * twbV(ii);
            % subtract withdrawals from portfolio values
              portvalV(ii) =  portvalV(ii) - incsM(ii,yr);
            % compute rider fees
              feesRiderM(ii,yr) = expPropTWB * twbV(ii);
            % subtract rider fees from portfolio values
              portvalV(ii) = portvalV(ii) - feesRiderM(ii,yr);
            % for negative portfolio values, adjust rider fees
              negvalV = zeros(nscen,1);
              negvalV(ii) = min(portvalV(ii),0);
              feesRiderM(ii,yr) = feesRiderM(ii,yr) + negvalV(ii);
              portvalV(ii) = portvalV(ii) - negvalV(ii);
            % set TWB values to max of portfolio values and prior TWB
              twbV(ii) =  max(portvalV(ii),twbV(ii));
         end % if length(ii) > 0   
 
       % scenarios in which estate is paid  
          ii = find(client.pStatesM(:,yr) == 4);
          if length(ii)>0
            % increment nominal values of portolio 
              portvalV(ii) =  portvalV(ii).* nrmsM(ii,yr-1);
            % compute fees for fund and subtract from portfolio value
              feesFundM(ii,yr)  = expPropFund * portvalV(ii);
              portvalV(ii) = portvalV(ii) - feesFundM(ii,yr);
           % pay remaining portfolio value to estate
              incsM(ii,yr) = portvalV(ii);
              portvalV(ii) = portvalV(ii) - incsM(ii);
          end % if length(ii) > 0 
   
     end; % for yr = 2:nyrs  
     
   % convert nominal incomes matrix to real
      rincsM = incsM ./ market.cumCsM;
   % convert nominal fees matrices to real fees 
      rfeesRiderM = feesRiderM ./ market.cumCsM;
      rfeesFundM =  feesFundM  ./ market.cumCsM;  
   % add results to client income and fee matrices
      client.incomesM = client.incomesM + rincsM;
      client.feesM  =   client.feesM  + rfeesRiderM + rfeesFundM;
      
   % if desired add matrices of fees to iGLWB data structure
      if lower(iGLWB.saveFeeMatrices) == 'y'
        iGLWB.feesRiderM = rfeesRiderM; 
        iGLWB.feesFundM  = rfeesFundM;
      end;  
      
   
end % iGLWB_process