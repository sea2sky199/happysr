
function client = iFixedAnnuity_process(iFixedAnnuity, client, market);
  % creates fixed annuity income matrix and fees matrix
  % then adds values to client incomes matrix and fees matricesco

  % get number of scenarios and years
     [nscen nyrs] = size(client.pStatesM);

  % make matrix of incomes for states 0,1,2,3 and 4
     psIncomesM = [ ];
     for pState = 0:4
        % guaranteed incomes
           if pState == 0
              guarIncomes = zeros(1,length(iFixedAnnuity.guaranteedIncomes));
           end;
           if (pState > 0) & (pState <4)
             guarIncomes = iFixedAnnuity.guaranteedIncomes;
           end;
           if pState == 4
              guarIncomes = fliplr(cumsum(iFixedAnnuity.guaranteedIncomes));
           end;
        % annuity incomes
           nAnnYrs =  nyrs - length(iFixedAnnuity.guaranteedIncomes);
           gradRatios = iFixedAnnuity.graduationRatio.^(0:1:nAnnYrs - 1);
           annIncomes = iFixedAnnuity.pStateIncomes(pState+1)*gradRatios;
        % guaranteed and annuity incomes
           psIncomes = [guarIncomes annIncomes];
        % add to matrix
           psIncomesM = [psIncomesM ; psIncomes];
     end; % for pState = 0:4
     client.psIncomesM = psIncomesM;

  % create matrix of relative incomes for all scenarios
     incomesM = zeros(nscen,nyrs);
     for pState = 0:4
        % make matrix of incomes for personal state
          mat = ones(nscen,1)*psIncomesM(pState+1,:);
        % find cells in client personal state matrix for this state
          ii = find(client.pStatesM == pState);
        % put selected incomes in incomes Matrix
          incomesM(ii) = mat(ii);
     end;
     client.relIncomesM = incomesM;
  % if values are nominal, change to real
     if lower(iFixedAnnuity.realOrNominal) == 'n'
         incomesM = incomesM ./ market.cumCsM;
     end; % if lower(iFixedAnnuity.realOrNominal) == 'n'

  % compute present value of all relative incomes
    pvIncomes = sum(sum(incomesM.*market.pvsM));

  % create fee matrix
    feesM = zeros(nscen,nyrs);
  % compute value of annuity purchased
    annVal = iFixedAnnuity.valueOverCost * iFixedAnnuity.cost;
  % add fee to matrix in column 1
    feesM(:,1) = iFixedAnnuity.cost - annVal;

  % scale incomes so pv = amount invested - fee
    factor = annVal/pvIncomes;
    incomesM = incomesM * factor;

  % add incomes and fees to client matrices
    client.incomesM = client.incomesM + incomesM;
    client.feesM = client.feesM + feesM;
  % subtract cost from client budget
    client.budget = client.budget - iFixedAnnuity.cost;
    client.incomeMSum = sum(sum(client.incomesM));
    client.pvIncomes = pvIncomes;

end


