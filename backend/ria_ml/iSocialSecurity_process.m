function client = iSocialSecurity_process(iSocialSecurity, client, market);
  % creates social security income matrix 
  % then adds values to client incomes matrix 
  
  % get number of scenarios and years
    [nscen nyrs] = size(client.pStatesM);
  % save personal states
    pStatesM = client.pStatesM;
  % create social security incomes matrix   
    incomesM = zeros(nscen,nyrs);
  
  % add incomes for personal state 3
    % extend input vector
       vec = iSocialSecurity.state3Incomes;
       if length(vec) > nyrs; vec = vec(1:nyrs); end;
       lastval = vec(length(vec));
       vec = [vec lastval*ones(1,nyrs-length(vec))];
    % create matrix with incomes for personal state 3 
       allIncomes = ones(nscen,1)*vec;
       states = (pStatesM == 3);
       stateIncomes = states.*allIncomes;
     % add to incomes matrix
       incomesM = incomesM + stateIncomes;
    
  % add incomes for personal states 1 and 2  
     for s =  1:2
        
      % get input matrix 
        if s==1
            m = iSocialSecurity.state1Incomes;  
          else
            m = iSocialSecurity.state2Incomes;
        end;     
     % extend input matrix
        [nrows ncols] = size(m);
        if ncols > nyrs; m = m(:,1:nyrs); ncols = nyrs; end;
        lastcol = m(:,ncols);
        numadd = nyrs - ncols;
        if numadd >0; m = [m lastcol*ones(1,numadd)]; end;
     % process all but last row 
       for i = 1: nrows-1
         % get row from matrix 
            incrow = m(i,:);
         % find column for last 3
            last3col = sum(incrow == Inf);
         % replace Inf with zero in incrow
            for c = 1:last3col; incrow(c) = 0; end;
         % create vector with s in pStateM rows with desired sequence of 3 and s
            psrows = (pStatesM(:,last3col) == 3) & (pStatesM(:,last3col+1) == s);
         % make matrix with incrow in every eligible row 
            mm = psrows*incrow;
         % set all cells with state not equal to s to zero 
            mm =  mm.*(pStatesM == s);
         % add to incomes matrix
            incomesM = incomesM + mm;
       end; % for i = 1: nrows-1    
        
     % process last row
         % get row from matrix 
            incrow = m(nrows,:);
         % find column for last 3
            last3col = sum(incrow == Inf);
         % replace Inf with zero in incrow
            for c = 1:last3col; incrow(c) = 0; end;
         % create vector with 1 in pStateM rows with >= the number of 3s
            psrows = (pStatesM(:,last3col) == 3);
         % make matrix with incrow in every eligible row 
            mm = psrows*incrow;
         % set all cells with state not equal to s to zero 
            mm =  mm.*(pStatesM == s);
         % add to incomes matrix
            incomesM = incomesM + mm;
        
    end; % for s = 1:2
     
  % add incomes to client incomes
      client.incomesM = client.incomesM + incomesM;

 end 
         
 