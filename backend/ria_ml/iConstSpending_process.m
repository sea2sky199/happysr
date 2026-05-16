 function client = iConstSpending_process(iConstSpending, client, market);
 
   % get matrix dimensions
      [nscen nyrs] = size(market.rmsM);
   % get glidepath   
      path =  iConstSpending.glidePath;
   
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
     if lower(iConstSpending.showGlidePath) == 'y'
        fig = figure;
        set(gca,'FontSize',30);
        ss = get(0,'Screensize');
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
     end; %  if lower(iConstSpending.showGlidePath) == 'y'
     
   % create matrix of gross returns for investment strategy 
     retsM = zeros(nscen,nyrs);
     for yr = 1: nyrs-1
        rets = pathys(yr) * market.rmsM(:,yr);
        rets = rets + (1-pathys(yr)) * market.rfsM(:,yr);
        retsM(:,yr) = rets;
     end;
     
   % get retention ratio
      rr = iConstSpending.retentionRatio;
      
   % create vector of initial portfolio values 
      portvals = ones(nscen,1)*iConstSpending.investedAmount;
      
   % initialize desired spending matrix   
      desiredSpendingM = zeros(nscen,nyrs);
   % create matrix of desired real spending for highest personal state 
      prop = iConstSpending.initialProportionSpent;
      amt = prop *iConstSpending.investedAmount;
      gradRatio = iConstSpending.graduationRatio;
      factors =  gradRatio.^(0:1:nyrs-1);
   % create matrix of maximum desired spending   
      maxSpendingM = ones(nscen,1)* (amt*factors);
     
   % add amounts to desired spending matrix
      props = iConstSpending.pStateRelativeIncomes;
      props = props / max(props);
      props = max(props,0);
      for ps = 1:1:3
         s = maxSpendingM .* props(ps); 
         m = (client.pStatesM == ps) .* s;
         desiredSpendingM = desiredSpendingM + m;
      end;   
   
   % initialize incomes and fees matrices
      incsM = zeros(nscen,nyrs);
      feesM = zeros(nscen,nyrs);

   % compute incomes paid at the beginning of year 1
      incsM(:,1) =  min(desiredSpendingM(:,1),portvals(:));
   % compute portfolio values after income payments
      portvals =  portvals - incsM(:,1);
      
   % compute incomes and fees paid at beginning of each subsequent year  
     for yr = 2: nyrs
       % compute portfolio values before deductions
          portvals = portvals.*retsM(:,yr-1);
       % compute and deduct fees paid at beginning of year
          feesV = (1 - rr)*portvals;
          feesM(:,yr) = feesV;
          portvals = portvals - feesV;
       % compute incomes paid out at beginning of year in states 1,2 or 3
          v = (client.pStatesM(:,yr) > 0) & (client.pStatesM(:,yr) < 4);
          incsM(:,yr) = v .* min(desiredSpendingM(:,yr),portvals);
       % pay entire value if state 4
          v = (client.pStatesM(:,yr) == 4);
          incsM(:,yr) = incsM(:,yr) + v.*portvals;
       % deduct incomes paid from portfolio values
          portvals = portvals - incsM(:,yr);
     end;    
  
     
   % add incomes and fees to client matrices
      client.incomesM = client.incomesM + incsM;
      client.feesM  = client.feesM + feesM;

 end
 