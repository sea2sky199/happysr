function [client,iLockboxSpending]  = iLockboxSpending_process(iLockboxSpending, client, market);
  % creates LB spending income matrix and fees matrix
  % then adds values to client incomes matrix and fees matrices
  
  % the lockbox proportions matrix can be computed by AMDnLockboxes_process
  %   or in some other manner. The first row is TIPS, the second is Market
  %   proportions, and there is a column for each year in the client matrix

  % get number of scenarios and years
     [nscen nyrs] = size(client.pStatesM);
     
  % fill lockbox proportions with zeros if needed
     props =  iLockboxSpending.lockboxProportions;
     nlbyears = size(props,2);
     props = [props(:,1:nlbyears) zeros(2,nyrs-nlbyears)];
     if size(props,2)>nyrs
        props = props(:,1:nyrs); 
     end;    
     
  % compute survival rates
     surv1 = cumprod(1-client.mortP1);
     surv2 = cumprod(1-client.mortP2);
     survboth = surv1.*surv2;
     surv1only = surv1.*(1-surv2);
     surv2only = surv2.*(1-surv1);
     survanyone = survboth + surv1only + surv2only;   
  
  % adjust proportions to take bequest utility ratio into account   
    % adjust market lockbox values 
       ranyoneV = exp(log(survanyone)/market.b);
       rmaxV = ones(1,nyrs);
       bur = iLockboxSpending.bequestUtilityRatio;
       ratioV =  bur*rmaxV + (1-bur)*ranyoneV;
    % change market proportions to keep total the same
       oldsum = sum(props(2,:));
       newmktprops = ratioV.*props(2,:);
       newsum = sum(newmktprops);
       newmktprops = (newmktprops/newsum) * oldsum;
       newprops =[ props(1,:) ; newmktprops];
    % save new proportions   
       iLockboxSpending.adjustedLockboxProportions = newprops;
     
  % compute lockbox dollar values   
      LBVals =(newprops/sum(sum(newprops)))*iLockboxSpending.investedAmount;  
     
  % plot lockbox amounts if requested
     if lower(iLockboxSpending.showLockboxAmounts) == 'y'
        xs =  LBVals;
        nyrs = size(xs,2);
        fig = figure;
        x = 1:1:size(xs,2);
        bar(x,xs','stacked'); grid;
        set(gca,'FontSize',30);
        ss = client.figurePosition;
        set(gcf,'Position',ss);
        set(gcf,'Color',[1 1 1]);
        xlabel('Lockbox Maturity Year ','fontsize',30);
        ylabel('Amount Invested at Inception   ','fontsize',30);
        legend('TIPS ','Market ');
        ax = axis; ax(1) = 0; ax(2) = nyrs+1; ax(3) = 0; ax(4) = max(sum(xs)); axis(ax);
        t = ['Lockbox Amounts at Inception '];
        title(t,'Fontsize',40,'Color','b');
        beep; pause;
     end; %if lower(combinedLockboxes.showContents) = 'y'    
     
    
  % create incomes
    incsM = zeros(nscen,nyrs); 
    for yr = 1:nyrs
     % scenarios with anyone alive  
         ii = find((client.pStatesM(:,yr)>0) & (client.pStatesM(:,yr)<4));  
        % add cumulative value of tips  
         incsM(ii,yr) = LBVals(1,yr)*market.cumRfsM(ii,yr);
        % add cumulative value of market   
         incsM(ii,yr) = incsM(ii,yr) + LBVals(2,yr)*market.cumRmsM(ii,yr);
     % scenarios with estate 
         ii = find(client.pStatesM(:,yr) == 4); 
        % values of current and remaining lockboxes
           m = sum(LBVals(:,yr:nyrs),2);
        % add cumulative values of tips
           incsM(ii,yr) = m(1)*market.cumRfsM(ii,yr);
        % add cumulative value of market   
           incsM(ii,yr) = incsM(ii,yr) + m(2)*market.cumRmsM(ii,yr);
    end; % for yr = 1:nyrs    
    
 
  % add incomes to client incomes matrix
     client.incomesM = client.incomesM + incsM;
    
end 
         
 