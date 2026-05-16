 function client = iPropSpending_process(iPropSpending, client, market);
 
   % get matrix dimensions
      [nscen nyrs] = size(market.rmsM);
   % get glidepath   
      path =  iPropSpending.glidePath;
   
   % get points from glidepath 
     ys =  path(1,:);
     xs =  path(2,:);
   % insure no years prior to 1
     xs = max(xs,1);
   % insure no market proportions greater than 1 or less than 0
     ys =  min(ys,1);
     ys =  max(ys,0);
   % sort points in increasing order of x values
     [xs ii] = sort(xs);
     ys = ys(ii);
   % add values for year 1 and/or last year if needed
     if xs(1) > 1; xs = [1 xs]; ys = [ys(1) ys]; end;
     if xs(length(xs))< nyrs
        xs = [xs nyrs]; ys = [ys ys(length(ys))];
     end;  
 
   % create vectors for all years
     pathxs = []; pathys = [];
     for i = 1:length(xs)-1  
       xlft = xs(i); xrt =  xs(i+1);
       ylft = ys(i); yrt =  ys(i+1);  
       pathxs = [pathxs xlft];
       pathys = [pathys ylft];
       if xlft ~= xrt
         slope = (yrt - ylft)/(xrt - xlft);
         for x = xlft+1:xrt-1
            pathxs = [pathxs x];
            yy = ylft + slope * (x - xlft);
            pathys = [pathys yy];
         end; %  for x = xlft+1:xrt-1
       end; % if xlft ~= xrt
     end; % for i = 1:length(xs)-1  
     pathxs =[pathxs xs(length(xs))];
     pathys =[pathys ys(length(ys))];
    
   % show glide path if desired
     if lower(iPropSpending.showGlidePath) == 'y'
        fig = figure;
        set(gca,'FontSize',30);
        ss = client.figurePosition;
        set(gcf,'Position',ss);
        set(gcf,'Color',[1 1 1]);
        xlabel('Year ','fontsize',30);
        ylabel('Proportion in Market Portfolio   ','fontsize',30);
        plot(path(2,:),path(1,:),'*b','Linewidth',4);
        hold on;
        plot(xs,ys,'-r','Linewidth',2);
        legend('Input ','All ');
        ax = axis; ax(1) = 0; ax(2) = nyrs+1; ax(3) = 0; ax(4) = 1; axis(ax);
        t = ['Glide Path: Market Proportions by Year  '];
        title(t,'Fontsize',40,'Color','b');
        plot(xs,ys,'-r','Linewidth',2);
        grid;
        hold off;
        xlabel('Year ','fontsize',30);
        ylabel('Proportion in Market Portfolio   ','fontsize',30);
        beep; pause;
        % create blank screen
          figblank = figure; set(gcf,'Position',ss);
          set(gcf,'Color',[1 1 1]);
     end; %  if lower(iPropSpending.showGlidePath) == 'y'
     
   % create matrix of gross returns for investment strategy 
     retsM = zeros(nscen,nyrs);
     for yr = 1: nyrs-1
        rets = pathys(yr) * market.rmsM(:,yr);
        rets = rets + (1-pathys(yr)) * market.rfsM(:,yr);
        retsM(:,yr) = rets;
     end;
     
   % get retention ratio
      rr = iPropSpending.retentionRatio;
      
   % get life expectancies 
    if lower(iPropSpending.useRMDlifeExpectancies) == 'y'
      LEs = [27.4 26.5 25.6 24.7 23.8 22.9 22.0 21.2 20.3 19.5 18.7 17.9 17.1 ...
          16.3 15.5 14.8 14.1 13.4 12.7 12.0 11.4 10.8 10.2 9.6 9.1 8.6    ...
          8.1 7.6 7.1 6.7 6.3 5.9 5.5 5.2 4.9 4.5 4.2 3.9 3.7 3.4 3.1  ...
          2.9 2.6 2.4 2.1 1.9 ];
      firstLEAge = 70;
    else
       % if RMD not used, vector of life expectancies and age for first value
       LEs = iPropSpending.nonRMDlifeExpectancies;
       firstAge = iPropSpending.nonRMDfirstLEAge;
    end; %  if lower(iPropSpending.useRMDlifeExpectancies) == 'y'  
    
   % expand LE vector 
   % assume no mortality before first age 
      firstLE = LEs(1);
      initLEs = firstLE + (firstLEAge-1:-1:1);
   % assume life expectancy constant after last age   
      LEs = [initLEs LEs];
      LEs = [LEs LEs(length(LEs))*ones(1,120)];
   % set life expectancies for years based on owners current age
     currAge = iPropSpending.portfolioOwnerCurrentAge;
     LEs = LEs(currAge:length(LEs));
     LEs = LEs(1:nyrs);
     
  % find spending proportions and insure they are between 0 and 1 inclusive
     spendProps = 1./LEs;
     spendProps = max(spendProps,0);
     spendProps = min(spendProps,1);
     
  % if desired, show proportions spent
     if lower(iPropSpending.showProportionsSpent) == 'y'
        fig2 = figure;
        set(gca,'FontSize',30);
        ss = client.figurePosition;
        set(gcf,'Position',ss);
        set(gcf,'Color',[1 1 1]);
        xs = 1:1:nyrs;
        ys = spendProps;
        plot(xs,ys,'-*r','Linewidth',2);
        t = ['Proportions of Portfolio Spent   '];
        title(t,'Fontsize',40,'Color','b');
        xlabel('Year ', 'fontsize',30);
        ylabel('Proportion of Portfolio Value Spent   ','fontsize',30);
        grid;
        beep; pause;
     end; %if lower(iPropSpending.showProportionsSpent) == 'y'
         
  % if desired, show Lockbox Equivalent Values
     if lower(iPropSpending.showLockboxEquivalentValues) == 'y'
        % find lockbox equivalent values  
          facs = 1 - spendProps;
          facs = [1 facs];
          facs = facs(1:length(facs)-1);
          lbVals = cumprod(facs).*spendProps;
          lbVals = lbVals* iPropSpending.investedAmount;
          fig3 = figure;
          set(gca,'FontSize',30);
          ss =client.figurePosition;
          set(gcf,'Position',ss);
          set(gcf,'Color',[1 1 1]);
          bar(lbVals,'r','Linewidth',2);
       %   ax = axis; ax(4) = 1; axis(ax);
          t = ['Lockbox Equivalent Initial Values  '];
          title(t,'Fontsize',40,'Color','b');
          xlabel('Year ', 'fontsize',30);
          ylabel('Lockbox Equivalent Initial Value   ','fontsize',30);
          grid;
          beep; pause;
        % create blank screen
          figblank = figure; set(gcf,'Position',ss);
          set(gcf,'Color',[1 1 1]);
     end; %if lower(iPropSpending.showLockboxEquivalentValues) == 'y'
          
     
  % create vector of initial portfolio values 
      portvals = ones(nscen,1)*iPropSpending.investedAmount;
 
  % initialize desired spending matrix   
      desiredSpendingM = zeros(nscen,nyrs);
    % initialize incomes and fees matrices
      incsM = zeros(nscen,nyrs);
      feesM = zeros(nscen,nyrs);
   % compute incomes paid at the beginning of year 1
      incsM(:,1) =  portvals*spendProps(1);
   % compute portfolio values after income payments
      portvals =  portvals - incsM(:,1);
      
   % compute incomes and fees paid at beginning of each subsequent year  
     for yr = 2: nyrs
       % compute portfolio values before deductions
          portvals = portvals.*retsM(:,yr-1);
       % compute and deduct fees paid at beginning of year
          feesV = (1 - rr)*portvals;
          feesM(:,yr) = feesM(:,yr) + feesV;
          portvals = portvals - feesV;        
       % compute incomes paid out at beginning of year in states 1,2 or 3
          v = (client.pStatesM(:,yr) > 0) & (client.pStatesM(:,yr) < 4);
          incsM(:,yr) =  v .* (portvals*spendProps(yr));
       % pay entire value if state 4
          v = (client.pStatesM(:,yr) == 4);
          incsM(:,yr) = incsM(:,yr) + v.*portvals;
       % deduct incomes paid from portfolio values
          portvals = portvals - incsM(:,yr);
     end;    
     
   % add incomes and fees to client matrices
      client.incomesM = client.incomesM + incsM;
      client.feesM = client.feesM + feesM;
 end