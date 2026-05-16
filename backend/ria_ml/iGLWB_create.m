function iGLWB = iGLWB_create( );
   % create a guaranteed lifetime withdrawal benefit data structure 

   % initial amount invested 
       iGLWB.initialValue = 100000;
       
   % single (s) or joint (j) life    
       iGLWB.singleOrJoint = 'j';
       
   % single life withdrawal proportions of TWB (from-age to-age proportion)
      iGLWB.singleLifeWithdrawalRates = [ 59 64 0.040; 65 79 0.050 ;80 120 0.060];
      
   % joint life withdrawal proportions of TWB (from-age to-age proportion)
   %   based on age of younger spouse
      iGLWB.jointLifeWithdrawalRates = [ 59 64 0.035; 65 79 0.045 ;80 120 0.055];
  
   % expense ratio for insurance rider as proportion of TWB
      iGLWB.expenseRatioOfTWB = 0.0120;
      
   % expense ratio for fund management and other fees 
   %   as proportion of account value
      iGLWB.expenseRatioOfFund = 0.0054;
      
   % save fee matrices with iGLWB data structure (y or n)
      iGLWB.saveFeeMatrices = 'n';

end