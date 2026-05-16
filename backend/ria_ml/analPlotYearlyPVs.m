function analPlotYearlyPVs(analysis, client, market, states);
   % plot Yearly PVs for states
   % called by analysis_process function

% add labels  
     set(gcf,'name','YearlyPVs ');
     set(gcf,'Position', analysis.figPosition); 
 
     grid on;
     xlabel('Year   ');
     ylabel('Present Value    ');
     hold on;
  
  % set colors for states 0,1,2,3,and 4 
     % orange; red; blue; green; orange; black  
       cmap = [1 .5 0 ; 1 0 0; 0 0 1; 0 .8 0; 1 .5 0];
  % set efficient PV color based on states
       clrmat = [];
       for s = 1:length(states)
          clrmat = [clrmat; cmap(states(s)+1,:)];  
       end;     
       clrPV = mean(clrmat,1);
  % set inefficiency color
       clrIneff = [0 0 0]; 
       colormap([clrPV ; clrIneff]);
       
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
    minprop = analysis.plotYearlyPVsMinPctScenarios;
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
 
  % set up valuation vectors
    totalpvs = [];
    effpvs = [];
  % get present values  
    for yr = 1:lastyear
        rows = find(cells(:,yr) > 0); 
        pvs = market.pvsM(rows,yr);
        incs = client.incomesM(rows,yr);
        totalpv = pvs' * incs;
        effpv = sort(pvs,'ascend')' * sort(incs,'descend');
        totalpvs = [totalpvs totalpv];
        effpvs = [effpvs effpv];
    end;
    
  % compute total efficiency  
    totaleff =100*(sum(effpvs) / sum(totalpvs));
    
  % title  
     ttl1 = ['Yearly Present Values, States = ' num2str(states) '  '];
     ttl2 =['Overall Efficiency = ' num2str(.1*round(10*totaleff)) '%  '];
     title({ttl1 ttl2}, 'color' , 'b');
  
  % scale axes
     axis([0 lastyear+1 0 max(totalpvs)]);
     grid;

  % plot pvs
     diffs = totalpvs - effpvs;  
     bar([effpvs; diffs]', 'stacked'); grid;
     legend('Efficient PV ','Inefficient PV ' );
  
   
end % plotYearlyPVs(analysis, client,market, states);  

