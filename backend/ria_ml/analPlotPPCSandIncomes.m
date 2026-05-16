function analPlotPPCSandIncomes(analysis, client, market, states);
   % plot PPCS and incomes for states
   % called by analysis_process function

% add labels  
     set(gcf,'name',['PPCs and Real Incomes ']);
     set(gcf,'Position', analysis.figPosition); 
 
     grid on;
     ylabel('log ( Price per Chance )  ');
     hold on;
  
  % set colors for states 0,1,2,3,and 4 
     % orange; red; blue; green; orange; black  
       cmap = [1 .5 0 ; 1 0 0; 0 0 1; 0 .8 0; 1 .5 0];
  % set full color based on states
       clrmat = [];
       for s = 1:length(states)
          clrmat = [clrmat; cmap(states(s)+1,:)];  
       end;     
       clrFull = mean(clrmat,1);
     % set shade color
       shade = analysis.animationShadowShade;
       clrShade = shade * clrFull + (1-shade)*[1 1 1]; 
       
  % get matrix size
     [nscen nyrs] = size(client.pStatesM);
     
  % set delay change parameter
     delays = analysis.animationDelays;
     delayChange = (delays(2)-delays(1))/(nyrs -1);
     
  % set initial delay  
     delay = delays(1);     
       
  % create matrix with 1 for each personal state to be included
     cells = zeros(size(client.pStatesM));
     for s = 1:length(states)
        cells = cells + (client.pStatesM == states(s)); 
     end;    
     
  % find last year with sufficient included states
    [nscen,nyrs] = size(cells);
    numstates = sum(cells > 0);
    minprop = analysis.plotPPCSandIncomesMinPctScenarios;
    minnum = (minprop/100)*nscen;
    lastyear = max((numstates > minnum).*(1:1:nyrs));
    if lastyear == 0
        title('Insufficient scenarios');
        return
    end;    
    
  % truncate matrices
    cellsM = cells(:,1:lastyear);
    incsM = client.incomesM(:,1:lastyear);
    ppcsM = market.ppcsM(:,1:lastyear);
     
  % find maximum and minimum incomes 
     ii = find(cellsM > 0);
     incsvec = incsM(ii);
     maxinc = max(incsvec);
     mininc= min(incsvec);
  % find maximum and minimum PPCs
     ppcsvec = ppcsM(ii);
     maxppc = max(ppcsvec);
     minppc = min(ppcsvec);
  % set delay change parameter
     delays = analysis.animationDelays;
     delayChange = (delays(2)-delays(1))/(nyrs -1);
  
  % set initial delay  
     delay = delays(1);  
 
  % if minimum income is zero, require semilog
    if mininc == 0
        analysis.plotPPCSandIncomesSemilog = 'y'
    end;    
      

 if analysis.plotPPCSandIncomesSemilog == 'y' 
     
  % set axes and label
     axis([0 maxinc log(minppc) log(maxppc)]);  
     xlabel('Real Income  ');
     
   for yr = 1:lastyear
       
     % get data  
       cellsv = cellsM(:,yr);
       ii = find(cellsv > 0);
       incs = incsM(ii,yr);
       ppcs = ppcsM(ii,yr);
  
     % title
       ttl1 = ['PPCs and Real Incomes, States =  '  num2str(states) '  '];
       ttl2 = ['Year: ' num2str(yr) '  '];
       title({ttl1 ttl2},'color','b');
       
     % plot points 
       plot(incs,log(ppcs),'*','color',clrFull,'Linewidth',.5);
       pause(delay);
     % shade points  
       delay = delay + delayChange;
       plot(incs,log(ppcs),'*','color',clrShade,'Linewidth',.5);
     
   end; 
   
 end; % if analysis.PlotPPCSandIncomesSemilog == 'y'  
    
     
 if analysis.plotPPCSandIncomesSemilog ~= 'y'  
     
  %  set axes and labels
     xlabel('log ( Real Income )  ');
     axis([log(mininc) log(maxinc) log(minppc) log(maxppc)]);  
     
   for yr = 1:lastyear
       
     % get data  
       cellsv = cellsM(:,yr);
       ii = find(cellsv > 0);
       incs = incsM(ii,yr);
       ppcs = ppcsM(ii,yr);
  
     % title
       ttl1 = ['PPCs and Real Incomes, States =  '  num2str(states) '  '];
       ttl2 = ['Year: ' num2str(yr) '  '];
       title({ttl1 ttl2},'color','b');
       
     % plot points 
       plot(log(incs),log(ppcs),'*','color',clrFull,'Linewidth',.5);
       pause(delay);
     % shade points  
       delay = delay + delayChange;
       plot(log(incs),log(ppcs),'*','color',clrShade,'Linewidth',.5);
     
   end;  
 
 end; % if analysis.PlotPPCSandIncomesSemilog ~= 'y'  
 
   
end % plotPPCSandIncomes(analysis, client,market, states);  

