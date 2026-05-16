function combinedLockboxes = combinedLockboxes_process(combinedLockboxes,client);
  
  % combines componentLockboxes in combinedLockboxes to create a new lockbox
    n = length(combinedLockboxes.componentLockboxes);
    wts = combinedLockboxes.componentWeights;
    wts =  max(wts, 0);
    wts = wts / sum(wts);
    
    boxprops = combinedLockboxes.componentLockboxes{1}.proportions;
    combprops  = wts(1) * boxprops;
    for i = 2:length(combinedLockboxes.componentLockboxes)
        boxprops = combinedLockboxes.componentLockboxes{i}.proportions;
        combprops  = combprops + ( wts(i) * boxprops);
    end; 
    combinedLockboxes.proportions =  combprops; 
    
  % plot contents if requested
     xs =  combinedLockboxes.proportions;
     nyrs = size(xs,2);
     if lower(combinedLockboxes.showCombinedProportions) == 'y'
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
        t = ['Lockbox Proportions for ' combinedLockboxes.title];
        title(t,'Fontsize',40,'Color','b');
        beep; pause;
     end; %if lower(combinedLockboxes.showContents) = 'y'    
     
end % function 
