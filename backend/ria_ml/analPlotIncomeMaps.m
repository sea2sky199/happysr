function analPlotIncomeMaps( analysis, client, market, plottype, states)
  % plots income images using personal states in vector states
  
  % initialize graph
     set(gcf,'name',['Income Images ' plottype] );
     set(gcf,'Position', analysis.figPosition); 
     grid on;
  % make plottype lower case
     plottype = lower(plottype);
     
  % set real or nominal text
     if findstr('n',plottype) > 0 
          rntext2 = 'Nominal '; 
       else
          rntext2 = 'Real '; 
     end;
     if findstr('c',plottype) > 0 
          rntext1 = 'Conditional'; 
       else
          rntext1 = ''; 
     end;
     
  % set states text
     statestext = ['States = ' num2str(states)]; 
     
  % convert client incomes  to nominal values if required
     if findstr('n',plottype) > 0
         client.incomesM = market.cumCsM .* client.incomesM;
     end;  
 
  % create matrix with 1 for each personal state to be included
     nscenarios = size(client.pStatesM,1);
     cells = zeros(size(client.pStatesM));
     for s = 1:length(states)
        cells = cells + (client.pStatesM == states(s)); 
     end;    

  % make matrix with incomes for included personal states
    incomes = cells.*client.incomesM;
  
  % find cells with included personal states
     ii = find(cells > 0);

  % find minimum and maximum incomes for included personal states
     mininc = min(incomes(ii));
     maxinc = max(incomes(ii));
    
  % find last year with sufficient included states
    [nscen,nyrs] = size(incomes);
    numstates = sum( cells > 0);
    minprop = analysis.plotIncomeMapsMinPctScenarios;
    minnum = (minprop/100)*nscen;
    lastyear = max((numstates > minnum).*(1:1:nyrs));
    
  % reduce matrices to cover only included years  
    incomes = incomes(:,1:lastyear);
    cells =  cells(:,1:lastyear);

  % create colormap
    colormap('default');
    map = colormap;
    map(1,:) = [1 1 1];
    colormap(map);
  % put a lower value in each excluded personal state
    ii = find(cells < 1);   
    incomes(ii) = mininc - 1;   
    
  % make changes if map is to be conditional 
   if findstr('c',plottype) > 0  % convert to conditional incomes
      incs = incomes(:,1:lastyear);
      condincs = [ ];
      for yr = 1:size(incs,2)
          % extract values for chosen personal states
             yrincs = incs(:,yr);
             yrcells = cells(:,yr);
             ii = find(yrcells > 0);
             vals = yrincs(ii);
          % create full vector of values greater than the minimum
             num = length(vals);
             m = vals * ones(1,ceil(nscen/num));
          % extract the first nscen values as a vector
             v =  m(1:nscen);
             if size(v,2) > 1; v = v'; end;
          % add to conditional incomes matrix
             condincs = [condincs v];
      end; % for yr = 1:size(m,2)      
      incomes = condincs;
      colormap('default');
   end; % if findstr('c',plottpe) > 0 
   
  % truncate incomes above percentage of maximum income
      prop = .01*analysis.plotIncomeMapsPctMaxIncome;
      maxinc = prop*max(max(incomes(:,1:lastyear)));
      incomes(:,1:lastyear) = min(maxinc,incomes(:,1:lastyear));
   
  % plot 
    imagesc(sort(incomes(:,1:lastyear),'ascend'));
    grid;
    cb = colorbar;
    set(cb,'Fontsize',30);
    set(gca,'Fontsize',30);
    set(gca,'YtickLabel',[.9 .8 .7 .6 .5 .4 .3 .2 .1 0]);
     
  % set labels
    xlabel(['Year'],'Fontsize',30);
    ylabel(['Probability of Exceeding ' rntext2 'Income '],'Fontsize',30);
    ttl = [rntext1 ' Probabilities of Exceeding ' rntext2 'Income in ' statestext];
    title(ttl,'Fontsize',40,'color','b');
    
end
