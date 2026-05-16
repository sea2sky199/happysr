function analPlotEfficientIncomes(analysis, client, market, type, states);
   % plot efficient incomes for states
   % called by analysis_process function

% add labels  
     set(gcf,'name','Efficient Real Incomes ');
     set(gcf,'Position', analysis.figPosition); 
 
     grid on;
     xlabel('Cumulative Market Real Return   ');
     ylabel('Real Income     ');
     hold on;
  
  % set colors for points for states 0,1,2,3,and 4 
     % orange; red; blue; green; orange; black  
       cmap = [1 .5 0 ; 1 0 0; 0 0 1; 0 .8 0; 1 .5 0];
  % set point color based on states
       clrmat = [];
       for s = 1:length(states)
          clrmat = [clrmat; cmap(states(s)+1,:)];  
       end;     
       clrPoints = mean(clrmat,1);
       
  % set point shadow shade color
       shade = analysis.animationShadowShade;
       clrPointsShade = shade*clrPoints + (1-shade)*[1 1 1];
       
  % set curve color and shade color
       clrCurve = [0 0 0];
       clrCurveShade = shade*clrCurve + (1-shade)*[1 1 1];
       
  % set line color and shade color  
       clrLine = [1 0.5 0];
       clrLineShade = shade*clrLine + (1-shade)*[1 1 1];
       
       
  % create matrix with 1 for each personal state to be included
     cells = zeros(size(client.pStatesM));
     for s = 1:length(states)
        cells = cells + (client.pStatesM == states(s)); 
     end;    
     
  % find last year with sufficient included states
    [nscen,nyrs] = size(cells);
    numstates = sum(cells > 0);
    minprop = analysis.plotEfficientIncomesMinPctScenarios;
    minnum = (minprop/100)*nscen;
    lastyear = max((numstates > minnum).*(1:1:nyrs));
    if lastyear == 0
        title('Insufficient scenarios');
        return
    end;  
    
  % set initial delay and change parameter
     delays = analysis.animationDelays;
     delay = delays(1);     
     delayChange = (delays(2)-delays(1))/(lastyear -1);
     delay = delays(1);     
      
  % truncate matrices
    cellsM = cells(:,1:lastyear);
    incsM = client.incomesM(:,1:lastyear);
    cumretsM = market.cumRmsM(:,1:lastyear);
    pvsM = market.pvsM(:,1:lastyear);
    
  % find maximum incomes
    maxincs =  max(max(incsM.*cellsM));
    
  % find maximum cumulative market return for x axis
  %   includes 99.9% of possible values
    cumretm = cumretsM.*cellsM;
    cumretv = sort(cumretm(:),'ascend');
    maxcumrets = cumretv(0.999*length(cumretv));
    
  % scale axes
    axis([0 maxcumrets 0 maxincs]);
    grid on;
    
  % plot results  
    for yr = 1:lastyear
        
      % get data for year  
        rows = find(cells(:,yr) > 0); 
        pvs = pvsM(rows,yr);
        incs = incsM(rows,yr);
        cumrets = cumretsM(rows,yr);
        
      % sort data  
        cumretsS = sort(cumrets,'ascend');
        incsS = sort(incs,'ascend');
        pvsS  = sort(pvs,'descend');
        
      % plot points if desired  
        if length(findstr('p',type)) >0
          plot(cumrets, incs,'*','color',clrPoints);
        end;  
        
      % fit line for regression of sorted incomes and cumrets
      %   incomeS = b(1) + b(2)*cumretS
        xvals =  [ones(length(cumretsS),1) cumretsS];
        b = xvals \ incsS;
   
      % compute fitted incomes using regression equation
        incsFitted = b(1) + b(2)* cumretsS;  
      % compute present value of original set of incomes
        pvIncs =  sum(pvs.*incs);
      % compute present value of fitted line
        pvLine =  sum(sort(pvs,'descend') .* sort(incsFitted,'ascend'));
      % find additional income for each scenario
        delta =  (pvIncs - pvLine) / sum(pvs);
      % increase each fitted income by a constant so pv = orginal amount
         incsFitted = incsFitted + delta;
      
      % plot sorted cumrets and incomes if desired
        if length(findstr('c',type)) >0  
          plot(cumretsS, incsS,'*','color',clrCurve);
        end;  
        
      % plot fitted line if desired
        if length(findstr('l',type)) >0 & (yr > 1)
           plot([0;cumretsS], [b(1)+delta; incsFitted],'color', clrLine,'Linewidth',4);
        end;
        
      % add title
        ttl1 = [ 'Efficient Real Incomes Year,  ' num2str(yr) '  States: ' num2str(states)];
        title(ttl1, 'color', 'b');  
      
      % pause  
        pause(delay);
        
      % shade points if plotted  
        if length(findstr('p',type)) >0
          plot(cumrets, incs,'*','color',clrPointsShade);
        end;  
       
       % shade sorted cumrets and incomes if plotted
        if length(findstr('c',type)) >0  
          plot(cumretsS, incsS,'*','color',clrCurveShade);
        end;  
        
      % shade fitted line if plotted
        if length(findstr('l',type)) >0 & (yr > 1)
           plot([0;cumretsS], [b(1)+delta; incsFitted],'color', clrLineShade,'Linewidth',4);
        end;
          
      % pause
        pause(delay);
     
     % change delay time   
        delay = delay - delayChange;
        
    end;
  
    
end % analPlotEfficientIncomes(analysis, client,market, types, states);  

