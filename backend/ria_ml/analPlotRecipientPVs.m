function analPlotRecipientPVs(analysis,client,market);
  % plot recipient present values as pie or bar chart
  % called by analysis_process function
  % compute values for state incomes
     pvs = [];
     for state = 0:4
        ii = find(client.pStatesM == state);
        pv = market.pvsM(ii)'* client.incomesM(ii);
        pvs = [pvs pv]; 
     end; %    
  % add states 0 to state 4 for estate total   
     pvs = [pvs(2:4) pvs(1)+pvs(5)]; 
  % compute fees
     fees = sum(sum(market.pvsM.*client.feesM));
  % add fees to present values    
     pvs = [pvs fees];
  % compute total value and create string in $thousands
     totalVal = sum(pvs);
     totalValStg = (num2str(round(totalVal)/1000));
  % if any value is zero change to small positive value
     for i = 1:length(pvs); 
        if pvs(i) == 0; pvs(i) = 0.00001; end;
     end;   
  % compute proportions 
    props = 100*(pvs/sum(pvs));
    
  % create chart  
     set(gcf,'name', 'RecipientPresent Values');
     set(gcf,'Position',analysis.figPosition); 
  % create legends
     legends = {};
     legends{1} = [client.p1Name ': ' num2str(props(1),'%7.1f') ' %'];
     legends{2} = [client.p2Name ': ' num2str(props(2),'%7.1f') ' %'];
     legends{3} = ['Both: '   num2str(props(3),'%7.1f') ' %'];
     legends{4} = ['Estate: ' num2str(props(4),'%7.1f') ' %'];
     legends{5} = ['Fees: '  num2str(props(5),'%7.1f') ' %'];

   % create chart
     if min(props) >= 0
      % create a pie chart
        if min(props)>0.05
           labels = {client.p1Name, client.p2Name, 'Both', 'Estate', 'Fees'};
        else
           labels = {'','','','',''}; 
        end;
        h = pie(props,labels);
        set(h(2:2:10),'FontSize',20);
      % create legend
        legends = {};
        legends{1} = [client.p1Name ': ' num2str(props(1),'%7.1f') ' %'];
        legends{2} = [client.p2Name ': ' num2str(props(2),'%7.1f') ' %'];
        legends{3} = ['Both: '   num2str(props(3),'%7.1f') ' %'];
        legends{4} = ['Estate: ' num2str(props(4),'%7.1f') ' %'];
        legends{5} = ['Fees: '  num2str(props(5),'%7.1f') ' %'];
        legend(legends,'Location','SouthEastOutside');
        cmap = [1 0 0; 0 0 1; 0 .8 0; 1 .5 0; 0 0 0]; colormap(gcf,cmap);
      else
      % create a bar chart 
        bar(props);
        grid;
        ylabel('Percent of Total Value');
        labels = {client.p1Name, client.p2Name, 'Both','Estate','Fees'};
        set(gca,'XTickLabel', labels);
    end; % if min(props) >= 0
    
    % add title
      title2 = ['Total Value = $' totalValStg ' thousand'];
      title({'Recipient Present Values',title2},'color',[0 0 1]);
    
end % function recipientPVs