function analPlotYOYIncomes( analysis, client, market, plottype, states)
  % plots income images using personal states in vector states
  
  % initialize graph
     set(gcf,'name',['YOYIncomes ' plottype] );
     set(gcf,'Position', analysis.figPosition); 
     grid on;
  % make plottype lower case
     plottype = lower(plottype);
     
  % set real or nominal text
     if findstr('n',plottype) > 0
          rntext = 'Nominal '; 
       else
          rntext = 'Real '; 
     end;
     
  % set states text
     statestext = ['States: ' num2str(states) ]; 
     
  % convert client incomes  to nominal values if required
     if findstr('n',plottype) > 0
         client.incomesM = market.cumCsM .* client.incomesM;
     end;  
     
  % set labels
    xlabel(['Year t ' rntext 'Income ' ]);
    ylabel(['Year t+1 ' rntext 'Income ']);
    ttl = ['Year over Year ' rntext 'Incomes: ' statestext ', Year t: '];
    
  % create matrix with 1 for each personal state to be included
     cells = zeros(size(client.pStatesM));
     for s = 1:length(states)
        cells = cells + (client.pStatesM == states(s)); 
     end;
  
  % find last year with income for personal states
     nyrs =  max(find(sum(cells) > 0));
  % modify matrices   
     incs = client.incomesM(:,1:nyrs); 
     cells = cells(:,1:nyrs);
    
     
  % set axes   
    ii = find(cells > 0);
    maxval = max(incs(ii));
    minval = min(incs(ii));
    if analysis.plotYOYIncomesWithZero == 'y'
        minval = 0;
    end;
    axis([minval maxval minval maxval]);
    
  % initialize plot  
    grid on;
    hold on;
    
  % set colors for states 0,1,2,3 and 4 
  % orange; red; blue; green; orange; 
    cmap = [1 .5 0 ; 1 0 0; 0 0 1; 0 .8 0; 1 .5 0]; 
  % set full color based on states
    clrmat = [];
       for s = 1:length(states)
          clrmat = [clrmat; cmap(states(s)+1, :)];
       end;     
    clrFull = mean(clrmat,1);
  % set shade color
    shade = analysis.animationShadowShade;
    clrShade = shade * clrFull + (1-shade)*[1 1 1]; 
    
  % set delay change parameter
    delays = analysis.animationDelays;
    delayChange = (delays(2)-delays(1))/(nyrs -1);
  % set initial delay   
    delay = delays(1);
    
  % plot 45 degree line
     plot([minval maxval], [minval maxval],'Linewidth',1,'color','k');
 
  % plot incomes   
     for col = 2:nyrs
        ttl1 = [ttl num2str(col-1) '  '];
        title(ttl1,'Fontsize',40,'color','b');
        col1 = col - 1;
        col2 = col;
        cellmat = cells(:,col-1:col);
        ii = find(sum(cellmat,2) >= 2);
        plot(incs(ii,col-1),incs(ii,col),'.','color', clrFull,'Linewidth',2);
        plot([minval maxval], [minval maxval],'Linewidth',2,'color','k');
        pause(delay);
        delay = delay + delayChange;
        plot(incs(ii,col-1),incs(ii,col),'.','color', clrShade, 'Linewidth',2);
     end;

end
