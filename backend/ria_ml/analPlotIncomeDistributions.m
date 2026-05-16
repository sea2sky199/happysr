function analPlotIncomeDistributions( analysis, client, market, plottype, states)
  % plots income distributions using personal states in vector states
  
  % initialize graph
     set(gcf,'name',['Income Distributions ' plottype] );
     set(gcf,'Position', analysis.figPosition); 
     grid on;
  % make plottype lower case
     plottype = lower(plottype);
  % set colors for states 0,1,2,3 and 4
     % orange; red; blue; green; orange; black  
     cmap = [1 .5 0 ; 1 0 0; 0 0 1; 0 .8 0; 1 .5 0]; 
     
  % set condition labels
     if findstr('c',plottype)>0
           condition = 'if ';
        else
           condition = 'and ';   
     end;    
     
   % set real or nominal text
     if findstr('n',plottype)>0
          rntext = 'Nominal '; 
       else
          rntext = 'Real '; 
     end;
     
   % set states text
     statestext = [condition 'States = ' num2str(states)]; 
     
   % set labels
     xlabel([rntext 'Income (x)']);
     ylabel(['Probability ' rntext 'Income Exceeds x']);
     ttlstart = [rntext 'Incomes ' statestext ': Year '];
 
   % create matrix with 1 for each personal state to be included
     cells = zeros(size(client.pStatesM));
     for s = 1:length(states)
        cells = cells + (client.pStatesM == states(s)); 
     end;    
     
   % convert client incomes  to nominal values if required
     if findstr('n',plottype)>0
         client.incomesM = market.cumCsM .* client.incomesM;
     end;  

  % create vector with number of scenarios for each year
     nscens = sum(cells);
  % find number of years to plot
     nyrs = sum(nscens>0);
  % find maximum income
     incomes = client.incomesM .* cells;
     maxIncome = max(max(incomes));

     
  % set axes for figure
     prop = .01*analysis.plotIncomeDistributionsPctMaxIncome;
     maxIncome = prop* maxIncome;  
     propShown  =  analysis.plotIncomeDistributionsProportionShown;
     if propShown < 1.0
         ii = find(cells == 1);
         v =  sort(incomes(ii),'ascend');
         i = fix(propShown * length(v));
         i = max(1,i);
         maxIncome = v(i);
     end;    
     ax = [0 maxIncome 0 1];
     axis(ax);   
     hold on;
     
     
  % set delay change parameter
     delays = analysis.animationDelays;
     delayChange = (delays(2)-delays(1))/(nyrs -1);
     
  % set initial delay  
     delay = delays(1);
     
  % set parameters
     % set full color based on states
       clrmat = [];
       for s = 1:length(states)
          clrmat = [clrmat; cmap(states(s)+1,:)];  
       end;     
       clrFull = mean(clrmat,1);
     % set shade color
       shade = analysis.animationShadowShade;
       clrShade = shade * clrFull + (1-shade)*[1 1 1]; 
     % set initial delay 
       delay = delays(1);
       
   % plot each year's distribution
     for yr = 1:nyrs
         
       % find values for y axis 
           rows = find(cells(:,yr) == 1); 
           incomes = client.incomesM(rows,yr);
           yx = 1:1:length(incomes);
           if findstr('c',lower(plottype))>0
                yx = yx/length(yx);
             else
                yx = yx/size(client.incomesM,1);            
           end;
        
       % compute probability of states and round to one decimal place
           if findstr('c',lower(plottype))>0
               probPstates = length(incomes)/size(client.incomesM,1);
             else
               probPstates = length(incomes)/size(client.incomesM,1);
           end;    
           probPstates = round(1000*probPstates)/10;
           
       % plot if probability large enough  
          if probPstates >=  analysis.plotIncomeDistributionsMinPctScenarios
             plot(sort(incomes,'ascend'),sort(yx,'descend'),'color',clrFull,'Linewidth',3);
             ttl1 = [ttlstart num2str(yr)];
             ttl2 = [ num2str(probPstates) ' Percent of Scenarios'];
             title({ttl1, ttl2},'color','b');
             pause(delay);
             plot(sort(incomes,'ascend'),sort(yx,'descend'),'color',clrShade,'Linewidth',3);
             delay = delay + delayChange;
          end; % if probPStates >= 0.5;  
        
     end; % for yr = 1,nyrs
    
end
