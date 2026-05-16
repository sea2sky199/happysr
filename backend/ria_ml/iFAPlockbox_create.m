function iFAPlockbox = iFAPlockbox_create( )
  % create a data structure for a lockbox to fund
  %   future purchase of a fixed annuity

  % year in which annuity is to be purchased
      iFAPlockbox.yearOfAnnuityPurchase = 20;
      
  % initial proportion ($) in TIPS in lockbox (0 to 1.0)
  %   with the remainder in the market portfolio
      iFAPlockbox.proportionInTIPS = 0.50;
  
  % initial amount ($) in the lockbox
      iFAPlockbox.investedAmount = 100000;
  
  % annuity ratio of value to initial cost
     iFAPlockbox.annuityValueOverCost = 0.90;
  
end