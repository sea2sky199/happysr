function client = client_create()
  % create a client data structure with default values
    client.p1Name = 'Bob';
    client.p1Sex =  'M';
    client.p1Age =  67;
    client.p2Name = 'Sue';
    client.p2Sex = 'F';
    client.p2Age =  65;
    client.Year = 2015;
    client.nScenarios = 100000;
    client.budget = 1000000;
    % figure size in pixels: width, height
    %    set to [ ] to use full screen
      client.figureSize = [1500  900];
end
