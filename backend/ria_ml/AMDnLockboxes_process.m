function AMDnLockboxes = AMDnLockboxes_process(AMDnLockboxes, market, client);

  % get number of years of returns 
     [nscen nyrs] = size(market.cumRmsM);
  % get n
     n = AMDnLockboxes.cumRmDistributionYear;
     if n < 2 ; n = 2; end;
     if n > nyrs; n = nyrs; end; 
 
  % set lockbox proportions for initial years to investment in the market
  % portfolio
     xfs = zeros(1,n-1);
     xms = ones (1,n-1); 
  % create matrix of proportions
     xs = [xfs; xms];
     
  % do regressions to compute contents of remaining lockboxes
     for yr = n:nyrs
        % sort cumulative returns
           x = sort(market.cumRmsM(:,yr),'ascend');
           y = sort(market.cumRmsM(:,n),'ascend');
        % regress y values on x values
        %     y = b(1) + b(2)*x
           xvals = [ ones(length(x), 1) x ];
           b = xvals \ y;
        % compute lockbox contents
           xf =  b(1)/mean(market.cumRfsM(:,yr));
           xm =  b(2);
        % add to xs matrix
           xs = [xs [xf;xm]];
     end % for yr = n:nyrs  
     
  % add lockbox holdings to AMDnLockboxes
     AMDnLockboxes.proportions = xs;
  
  % plot contents if requested
     if lower(AMDnLockboxes.showProportions) == 'y'
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
        t = ['Lockbox Contents for Approximating Market Distribution in year ' num2str(n)];
        title(t,'Fontsize',40,'Color','b');
        beep; pause;
     end; %if lower(AMDnLockboxes.showContents) = 'y'    
     
end % function 
