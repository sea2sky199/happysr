 function analysis_process(analysis, client, market)
   % process an analysis data structure to produce analysis output  
   
   % initialize
       analysis = initialize(analysis,client);  % *******
       
   % analysis: plot survival probabilities
       if analysis.plotSurvivalProbabilities == 'y' 
          % create figure
            analysis = createFigure(analysis);
          % call external function analPlotSurvivalProbabilities
            analPlotSurvivalProbabilities(analysis, client, market);
          % process figure
            analysis = processFigure(analysis); 
       end;   
       
   % analysis: plot scenarios 
       if analysis.plotScenarios == 'y'
          % find types
            types = analysis.plotScenariosTypes;
          % create figures
            for i = 1:length(types)
              % create figure
                  analysis = createFigure(analysis); 
              % call external function analPlotScenarios
                  analPlotScenarios(analysis,client,market,types{i}); 
              % process figure
                  analysis = processFigure(analysis);
            end;  
       end;     
            
     % analysis: plot income distributions
       if analysis.plotIncomeDistributions == 'y'
          % find states; 
            states = analysis.plotIncomeDistributionsStates;
          % find types
            types = analysis.plotIncomeDistributionsTypes;
          % create figures
            for i = 1:length(types)
              for j = 1:length(states)
                  % create Figure
                    analysis = createFigure(analysis);
                  % call external function analPlotIncomeDistributions
                    analPlotIncomeDistributions(analysis, client, market, types{i}, states{j} );
                  % process figure
                    analysis = processFigure(analysis);
              end; %j      
            end; %i   
       end;   
       
     % analysis: plot income maps
       if analysis.plotIncomeMaps == 'y'
          % find states; 
            states = analysis.plotIncomeMapsStates;
          % find types
            types = analysis.plotIncomeMapsTypes;
          % create figures
            for i = 1:length(types)
              for j = 1:length(states)
                  % create Figure
                   analysis = createFigure(analysis);
                  % call external function analPlotIncomeMaps
                    analPlotIncomeMaps(analysis, client, market, types{i}, states{j} );
                  % process figure
                    analysis = processFigure(analysis);
              end; %j      
            end; %i   
       end;   
       
      % analysis: plot year over year incomes
       if analysis.plotYOYIncomes == 'y'
          % find states; 
            states = analysis.plotYOYIncomesStates;
          % find types
            types = analysis.plotYOYIncomesTypes;
          % create figures
            for i = 1:length(types)
              for j = 1:length(states)
                  % create Figure
                   analysis = createFigure(analysis);
                  % call external function analPlotYOYIncomes
                    analPlotYOYIncomes(analysis, client, market, types{i}, states{j} );
                  % process figure
                    analysis = processFigure(analysis);
              end; %j      
            end; %i   
       end;     
       
       
   % analysis: plot recipient present values 
       if analysis.plotRecipientPVs == 'y'
          % create figure
            analysis = createFigure(analysis); 
          % call external function analPlotRecipientPVs
            analPlotRecipientPVs(analysis, client, market);
          % process figure
            analysis = processFigure(analysis);
       end;   
  
      
    % analysis: plot PPCs and Incomes
       if analysis.plotPPCSandIncomes == 'y'
          % find states; 
            states = analysis.plotPPCSandIncomesStates;
          % create figures
             for i = 1:length(states)
                % create Figure
                   analysis = createFigure(analysis);
                % call external function analPlotPPCSandIncomes
                    analPlotPPCSandIncomes(analysis, client, market, states{i} );
                % process figure
                    analysis = processFigure(analysis);
              end; %i   
       end; % if analysis.plotPPCSandIncomes == 'y'    
       
       
       
    % analysis: plot yearly PVs
       if analysis.plotYearlyPVs == 'y'
          % find states; 
            states = analysis.plotYearlyPVsStates;
          % create figures
             for i = 1:length(states)
                % create Figure
                   analysis = createFigure(analysis);
                % call external function analPlotPPCSandIncomes
                    analPlotYearlyPVs(analysis, client, market, states{i} );
                % process figure
                    analysis = processFigure(analysis);
              end; %i   
       end; % if analysis.plotYearlyPVs == 'y'    
  
    % analysis: plot efficient incomes
       if analysis.plotEfficientIncomes == 'y'
          % find states; 
            states = analysis.plotEfficientIncomesStates;
          % find types
            types = analysis.plotEfficientIncomesTypes;
          % create figures
             for i = 1:length(types)
               for j = 1:length(states)  
                 % create Figure
                    analysis = createFigure(analysis);
                 % call external function analPlotPPCSandIncomes
                    analPlotEfficientIncomes(analysis, client, market,types{i}, states{j});
                % process figure
                    analysis = processFigure(analysis);
               end; %j     
             end; %i   
       end; % if analysis.plotEfficientIncomes == 'y'    

       
   % finish all analyses
      finish(analysis);
       
end % function analysis_process(analysis, client, market)  


function analysis = initialize(analysis, client) 
 % initialize variables 
   % set figure position and number
     figsize = client.figureSize;
     if length(figsize) < 2
        ss = get(0,'screenSize');  
        figsize(1) = .9*ss(3);
        figsize(2) = .9*ss(4);
     end;   
     figw = figsize(1);
     figh = figsize(2);
     ss = get(0,'screenSize');
     x1 = (ss(3) - figw)/2;
     x2 = (ss(4) - figh)/2;
     analysis.figPosition = [x1 x2 figw figh];
  % set figure number and initialize stack      
     analysis.figNum = 1;
     analysis.stack = [ ];
  end % function initialize
  

function analysis = createFigure(analysis)
  
  % create a new figure 
      fignum = figure;
      set(gcf,'Position',analysis.figPosition);
      analysis.stack = [analysis.stack fignum];         
  % set colormap to the default set of colors
      colormap('default');
  % set font sizes 
      xl = get(gca,'XLabel');
      set(xl,'Fontsize',30);
      yl = get(gca,'YLabel');
      set(yl,'Fontsize',30);   
      ttl = get(gca,'Title');
      set(ttl,'Fontsize',40);
      set(gca,'Fontsize',30);
      h = findobj(gcf,'type','text');
      for i = 1:length(h)
        set(h(i),'Fontsize',30);
      end;   
  % set background color
     set(gcf,'color',[1 1 1]);
  % if figures not stacked, remove bottom figure
     if lower(analysis.stackFigures) == 'n'
        if length(analysis.stack) > 2
            close(analysis.stack(1));
            analysis.stack = analysis.stack(2:length(analysis.stack));
        end;
        
     end;
   
end % function CreateFigure(analysis)     
     

function analysis = processFigure(analysis)

  % change figure number
     analysis.figNum = analysis.figNum + 1;
     
  % delay before next figure or end
     if analysis.figureDelay > 0
          pause(analysis.figureDelay);
       else
          beep;
          pause;
     end;
    
     
end % function analysis = processFigure(analysis)


function finish(analysis)

    if lower(analysis.stackFigures) == 'n'
       if length(analysis.stack) > 1
          close(analysis.stack(1)); 
       end;    
    end;    
  
    if analysis.figuresCloseWhenDone == 'y'
        close all;
    end;    
    
end % function finish(analysis)

