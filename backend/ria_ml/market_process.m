function market = market_process(market,client)
  % get size for all matrices from client.pStatesM
     [nrows, ncols] = size(client.pStatesM);
     
  % compute cost of living (inflation) matrix
       u = market.eC; 
       v = market.sdC^2;
       b = sqrt(log((v/(u^2)) + 1)); 
       a = 0.5 *log((u^2)/exp(b^2));
       market.csM = exp(a + b*randn(nrows,ncols));
  % compute cumulative cost of living (inflation) matrix
       m = cumprod(market.csM,2);
       market.cumCsM = [ones(nrows,1) m(:,1:ncols-1)];
       
  % compute risk-free real returns matrix
       market.rfsM = market.rf*ones(nrows,ncols);
  % compute cumulative risk-free real returns matrix at ends of each year
       m = cumprod(market.rfsM,2);
       market.cumRfsM = [ones(nrows,1) m(:,1:ncols-1)];
       
  % compute market returns matrix   
       u = market.exRm + (market.rf - 1); % get total market expected return
       v = market.sdRm^2;
       b = sqrt(log((v/(u^2)) + 1)); 
       a = 0.5 *log((u^2)/exp(b^2));
       market.rmsM = exp(a + b*randn(nrows,ncols));
  % compute market cumulative returns matrix
       m = cumprod(market.rmsM,2);
       market.cumRmsM = [ones(nrows,1) m(:,1:ncols-1)];

  % compute ppcs and present values matrix   
       b = log(u/market.rf)/log(1 + (market.sdRm^2)/(u^2));
       a = sqrt(u*market.rf)^(b-1);
       as = ones(nrows,1)*(a.^(0:ncols-1));
       market.ppcsM = as.*(market.cumRmsM.^-b);
       market.pvsM = market.ppcsM/nrows;
   % temporary
       market.avec = as(1,:);
       market.b = b;
       
 end              