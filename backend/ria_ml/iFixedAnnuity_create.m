function iFixedAnnuity = iFixedAnnuity_create();
    % guaranteed relative or absolute incomes for years 1,...
       iFixedAnnuity.guaranteedIncomes = [];
    % relative incomes in first post-guarantee year for personal states 0,1,2,3 and 4
       iFixedAnnuity.pStateIncomes = [0 .5 .5 1 0]; 
    % graduation ratio of each post-guarantee income to prior post-guarantee income
       iFixedAnnuity.graduationRatio = 1.00;
    % type of incomes (real 'r' or nominal 'n');   
       iFixedAnnuity.realOrNominal = 'r';
    % ratio of value to initial cost
       iFixedAnnuity.valueOverCost = 0.90;
    % cost 
       iFixedAnnuity.cost = 100000;
end