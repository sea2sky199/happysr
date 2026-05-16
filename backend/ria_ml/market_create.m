function market = market_create()
  % create a market data structure with default values
  % cost of living 
    market.eC      = 1.02;   % expected cost of living ratio
    market.sdC     = 0.01;   % standard deviation of cost of living ratios
  % risk-free real investments   
    market.rf      = 1.01;   % risk-free real return rate
  % market portfolio returns
    market.exRm    = 1.0425; % market portfolio expected return over risk-free rate
    market.sdRm    = 0.125;  % market portfolio standard deviation of return
 end
