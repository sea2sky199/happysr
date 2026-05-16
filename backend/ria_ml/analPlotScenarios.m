function analPlotScenarios(analysis,client,market, plottype);
   % plot scenarios for income, estates and/or fees
   % called by analysis_process function

   % make plottype lower case
     plottype = lower(plottype);

   % add labels
     set(gcf,'name',['Scenarios: ' plottype]);
     set(gcf,'Position',analysis.figPosition);
     grid on;
     title(['Scenarios'],'color',[0 0 1]);
     xlabel('Year');
     if findstr(plottype,'r')>0
        ylabel('Real Income, Estate or Fees');
     else
        ylabel('Nominal Income, Estate or Fees');
     end;
     hold on;

  % set colors for states 0,1,2,3,4 and fees (5)
     % orange; red; blue; green; orange; black
     cmap = [1 .5 0 ; 1 0 0; 0 0 1; 0 .8 0; 1 .5 0; 0 0 0];


  % convert client income and fees to nominal values if required
     if findstr(plottype,'n')> 0
         client.incomesM = market.cumCsM .* client.incomesM;
         client.feesM    = market.cumCsM .* client.feesM;
     end;

  % extract sample matrices for at least 100 scenarios
     n = max(100, analysis.plotScenariosNumber);
     [nscen nyrs] = size(client.incomesM);
     firstScen = randi([1 nscen - n]);
     lastScen = firstScen + n-1;
     scenPStates = client.pStatesM(firstScen:lastScen,:);
     scenIncomes = client.incomesM(firstScen:lastScen,:);
     scenFees    = client.feesM(firstScen:lastScen,:);

  % set personal states to be shown
     if findstr(plottype,'i')>0
        states = [1 2 3];
     end;
     if findstr(plottype,'e')>0
        states = [states 4];
     end;

  % find maximum value for y axis
      incomeCells = zeros(size(scenPStates));
      for i = 1:length(states)
         incomeCells = incomeCells + (scenPStates == states(i));
      end;
      maxIncome = 1.01*( max(max((incomeCells>0).*scenIncomes)));
  % if fee is to be included, find maximum fee for sample states
     if findstr(plottype,'f')>0
        maxFee = max(max(scenFees));
     else
        maxFee = 0;
     end;
  % set maximum for y axis
     maxY = 1.01*max(maxIncome,maxFee);

  % set axes
     axis([0 nyrs 0 maxY]);

  % set shade and delay parameter
     shade = analysis.animationShadowShade;
     delays = analysis.animationDelays;
     delayChange = (delays(2)-delays(1))/(analysis.plotScenariosNumber -1);

  % show scenarios
     delay = delays(1);
     for scenNum = 1:analysis.plotScenariosNumber

        % plot incomes
          incomes = scenIncomes(scenNum,:);
          pstates = scenPStates(scenNum,:);
          for pstate = states
             x = find(pstates == pstate);
             if length(x) > 0
                y =incomes(x);
                plot(x,y,'-*','color',cmap(pstate+1,:),'Linewidth',2.5);
             end;
          end;

        % plot fees
          if findstr(plottype,'f')>0
             fees = scenFees(scenNum,:);
             plot(1:nyrs,fees,'*', 'color',cmap(6,:),'Linewidth',2.5);
          end;

        % pause
           pause(delay);
           delay = delay + delayChange;

        % re-plot incomes using shading
           for pstate = states
             x = find(pstates == pstate);
             if length(x) > 0
                y =incomes(x);
                clr = shade*cmap(pstate+1,:) + (1-shade)*[1 1 1];
                plot(x,y,'-*','color',clr,'Linewidth',2.5);
             end;
           end;

        % re-plot fees using shading
           if findstr(plottype,'f')>0
              clr = shade*cmap(6) + (1-shade)*[1 1 1];
              plot(1:nyrs,fees,'*', 'color',clr,'Linewidth',2.5);
           end;

     end; % for scenNum = 1:analysis.plotScenariosNumber

end % plotScenarios(analysis, client,market, caseNum;

