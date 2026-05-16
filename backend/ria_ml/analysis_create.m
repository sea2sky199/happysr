function analysis = analysis_create( );
   % create an analysis data structure 
   
   % case name
       analysis.caseName = 'Smith Case';
       
   % animation first and last delay times in seconds 
       analysis.animationDelays = [1 0.5];
   % animation shadow shade of original (0 to 1)
       analysis.animationShadowShade = 0.2;
   % delay time between figures (0 for beep and keypress) in seconds
       analysis.figureDelay = 0;
   % stack figures or replace each one with the next
       analysis.stackFigures = 'n';
   % close figures when done
       analysis.figuresCloseWhenDone = 'y';
       
   % plot survival probabilities -- y/n
       analysis.plotSurvivalProbabilities = 'n';
 
   % plot scenarios
       analysis.plotScenarios = 'n';
   % plot scenarios: set of cases with real (r) or nominal (n) and 
   %   income (i), estate (e) and/or fees (f) 
       analysis.plotScenariosTypes = {'ri' 'rie' 'rif' 'rief'};
    % plot scenarios: number of scenarios
       analysis.plotScenariosNumber = 10;
       
   % plot income distributions   
       analysis.plotIncomeDistributions = 'n';
   % plot income distributions: set of cases with real or nominal (r/n) and 
   %   conditional or unconditional (c/u) types
       analysis.plotIncomeDistributionsTypes = {'rc' 'ru' 'nc' 'nu'};
   % plot income distributions: sets of states (one set per graph)
       analysis.plotIncomeDistributionsStates = {[3] [1 2]};
   % plot income distributions: minimum percent of scenarios
       analysis.plotIncomeDistributionsMinPctScenarios = 0.5;
   % proportion of incomes to be shown
       analysis.plotIncomeDistributionsProportionShown = 1.00;
   % plot income distributions: percent of maximum income plotted
       analysis.plotIncomeDistributionsPctMaxIncome = 100;
     
   % plot income maps 
       analysis.plotIncomeMaps = 'n';
   % plot income maps: set of value types -- real or nominal (r/n) and
   %   conditional or unconditional (c/u) types
       analysis.plotIncomeMapsTypes = {'ru' 'rc'};
   % plot income maps: sets of states (one set per graph)
       analysis.plotIncomeMapsStates = {[3] [1 2]};
   % plot income maps: minimum percent of scenarios
       analysis.plotIncomeMapsMinPctScenarios = 0.5;
   % plot income maps: percent of maximum income plotted
       analysis.plotIncomeMapsPctMaxIncome = 100;
      
   % plot year over year incomes 
       analysis.plotYOYIncomes = 'n';
   % plot year over year incomes -- real or nominal (r/n) 
       analysis.plotYOYIncomesTypes = {'r' 'n'};
   % plot year over year incomes -- sets of states (one set per graph)
       analysis.plotYOYIncomesStates = {[3] [1 2]};
   % plot year over year incomes -- include zero (y/n)
       analysis.plotYOYIncomesWithZero = 'y';
            
   % plot recipient present values -- y (yes) or n (no)
       analysis.plotRecipientPVs = 'n';
       
   % plot PPCs and Incomes -- y/n
       analysis.plotPPCSandIncomes = 'n';
   % plot PPC and Incomes -- semilog or loglog
       analysis.plotPPCSandIncomesSemilog = 'y';
   % plot PPCs and Incomes -- sets of states (one set per graph)
       analysis.plotPPCSandIncomesStates = {[3]};
    % plot PPCs and Incomes: minimum percent of scenarios
       analysis.plotPPCSandIncomesMinPctScenarios = 0.5;
       
        
   % plot PPCs and Incomes -- sets of states (one set per graph)
       analysis.plotPPCSandIncomesStates = {[3]};
       
   % plot yearly present values -- y (yes) or n (no)
       analysis.plotYearlyPVs = 'n';
   % plot yearly present values-- sets of states (one set per graph)
       analysis.plotYearlyPVsStates = {[3 1 2]};
   % plot yearly present values: minimum percent of scenarios
       analysis.plotYearlyPVsMinPctScenarios = 0.5;
  
   % plot efficient incomes -- y (yes) or n (no)
       analysis.plotEfficientIncomes = 'n';
   % plot efficient incomes -- sets of states (one set per graph)
       analysis.plotEfficientIncomesStates = {[3] [1 2]};
   % plot points (actual) curves (efficient) and/or 
   %   lines (two-asset market-based strategies
   %   combinations of (p,c,l) -- one graph per type
       analysis.plotEfficientIncomesTypes = {'pcl'}; 
   % plot efficient incomes: minimum percent of scenarios
       analysis.plotEfficientIncomesMinPctScenarios = 0.5;
  
end