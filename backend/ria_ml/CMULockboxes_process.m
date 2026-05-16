function CMULockboxes = CMULockboxes_process(CMULockboxes, market, client );
  % computes lockbox proportions for an CMULockbox strategy
  
  % get number of years
     [nscen nyrs] = size(market.cumRmsM);
     
  % set proportions for year 1
     mktprop = CMULockboxes.initialMarketProportion;
     if mktprop > 1; mktprop = 1; end;
     if mktprop < 0; mktprop = 0; end;
     tipsprop =  1 - mktprop;
     
  % find ratio of market proportion each year to that for the prior year
     a = market.avec(2);
     b = market.b;
     logk = ( -log(1/a) ) / b;
     k = exp(logk);
  % compute market proportions for all years  
     mktprops = mktprop* ( (1/k).^(0:1:nyrs-1) );
     
  % compute TIPS proportions for all years   
     tipsprops = tipsprop * ( (1/market.rf).^(0:1:nyrs-1) );
     
  % compute lockbox proportions;
      CMULockboxes.proportions = [ tipsprops; mktprops ];

  % plot contents if requested
     if lower(CMULockboxes.showProportions) == 'y'
        xs =  CMULockboxes.proportions; 
        fig = figure;
        x = 1:1:size(xs,2);
        bar(x,xs','stacked'); grid;
        set(gca,'FontSize',30);
        ss = client.figurePosition;
        set(gcf,'Position',ss);
        set(gcf,'Color',[1 1 1]);
        xlabel('Lockbox Maturity Year ','fontsize',30);
        ylabel('Amount Invested at Inception   ','fontsize',30);
        legend('TIPS ','Market ');
        ax = axis; ax(1) = 0; ax(2) = nyrs+1; ax(3) = 0; ax(4) = 1; axis(ax);
        t = ['Lockbox Proportions for Constant Marginal Utility '];
        title(t,'Fontsize',40,'Color','b');
        beep; pause;
     end; %if lower(CMULockboxes.showContents) = 'y'    
     
end % function 

