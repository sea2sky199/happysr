function analPlotSurvivalProbabilities(analysis,client,market);
   % plot survival probabilities
   % called by analysis_process function
   % get probabilities of survival
     probSurvive1only =  mean(client.pStatesM == 1);
     probSurvive2only =  mean(client.pStatesM == 2);
     probSurviveBoth =   mean(client.pStatesM == 3);
     probSurviveAll = [probSurviveBoth ; probSurvive1only; probSurvive2only]';
  % create graph   
    set(gcf,'name','Recipient Survival Probabilities');
    set(gcf,'Position',analysis.figPosition); 
    bar(probSurviveAll,'stacked');
    grid on;
    title('Recipient Survival Probabilities','color',[0 0 1]);
    xlabel('Year');
    ylabel('Probability');
    legend('Both', [client.p1Name ' only'],[client.p2Name ' only']);
    cmap = [0 .8 0; 1 0 0; 0 0 1];
    colormap(gcf,cmap);
end % plotSurvivalProbabilities(analysis, client,market);  
