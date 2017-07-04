function freqItemset = Programming_Assignment_Apriori(minSup, transFile)

    % Import database from file
    databaseArr = importdata(transFile);
    
    % Remove commas from cell array     
    for i = 1:size(databaseArr)
        databaseArr{i}=strrep(databaseArr{i},',','');
    end
    
    % Transform data into an ASCII column   
    candStr = uint8(strcat(databaseArr{1:end})');
    
    % Get 1-candidates and support    
    candArr = [unique(candStr),histc(candStr(:),unique(candStr))];
    
    % Prune to get frequent 1-itemsets
    candArr(any(candArr < minSup, 2),:) = [];
    freqItem = char(candArr(:,1));
    
    % Push frequent 1-itemsets to final itemset
    freqItemset = num2cell(freqItem);
    
    % End function if there are less than two frequent 1-itemset items
    if(size(freqItem) <= 1)
        return;
    end
    
    % Create 2-candidate table through self-join 
    candArr2 = [];
    for i = 1:size(freqItem)
        for j = (i+1):size(freqItem)
            candArr2 = uint8(cat(1, candArr2, cat(2, ...
                strcat(freqItem(i),freqItem(j)))));
        end    
    end

   % Create 2-candidate frequencies by comparing an ASCII 2-candidate 
   % table to the ASCII-transformed database        
    freqArr2 = [];
    for i = 1:size(candArr2)
        freqCounter = 0;
        for j = 1:size(databaseArr)
            if(all(ismember(candArr2(i,:), uint8(databaseArr{j}))))
                freqCounter = freqCounter + 1;
            end
        end
        freqArr2 = cat(1, freqArr2, freqCounter);
    end
    
    % Combine the candidates and frequencies into one table  
    candArr2 = cat(2, candArr2, freqArr2);

    % Prune to get frequent 2-itemsets
    candArr2(any(candArr2 < minSup, 2),:) = [];
    freqItem2 = {};
    for i = 1:size(candArr2)
        freqItem2{i} = strcat(candArr2(i,1), candArr2(i,2));
    end
    
    % Push frequent 2-itemsets to final itemset
    freqItemset = cat(1, freqItemset, freqItem2');
    
    % End function if there are less than two frequent 2-itemset items
    if(size(freqItem2') <= 1)
        return;
    end
    % Convert the frequent 2-itemsets back from cell
    freqItem2 = cell2mat(freqItem2');
    
    % Set the frequent 2-itemsets to be used in the loop
    freqItemX = freqItem2;
    
    % Loop through self-joining, scanning, and pruning until less than two
    % items remain
    while(size(freqItemX, 2) > 1)
        
        % Self-join by comparing each itemset to check if all but one item
        % are the same
        databaseArrX = [];
        for i = 1:size(freqItemX)
            for j = (i+1):size(freqItemX)
                if((size(freqItemX,2)) - size(intersect(freqItemX(i,:), ...
                    freqItemX(j,:)), 2) == 1)
                    databaseArrX = cat(1, databaseArrX, cat(2, ...
                        freqItemX(i,:), freqItemX(j,:)));
                end
            end    
        end
        
        % Eliminate repeating items in the same row
        uniqueDatabaseArrX = [];
        for i = 1:size(databaseArrX)
            uniqueDatabaseArrX = uint8(unique(cat(1, uniqueDatabaseArrX,...
                unique(databaseArrX(i,:))), 'rows'));
        end
        % Create x-candidate frequencies by comparing an ASCII x-candidate 
        % table to the ASCII-transformed database 
        freqArrX = [];
        for i = 1:size(uniqueDatabaseArrX)
            freqCounter = 0;
            for j = 1:size(databaseArr)
                if(all(ismember(uniqueDatabaseArrX(i,:), ...
                        uint8(databaseArr{j}))))
                    freqCounter = freqCounter + 1;
                end
            end
            freqArrX = cat(1, freqArrX, freqCounter);
        end
        
        % Combine the candidates and frequencies into one table  
        candArrX = cat(2, uniqueDatabaseArrX, freqArrX);
        
         % Prune to get frequent x-itemsets
        candArrX(any(candArrX < minSup, 2),:) = [];
        candArrX = char(candArrX(:,1:end-1));
        
        
        freqItemX = {};
        for i = 1:size(candArrX)
            freqItemX{i} = strcat(candArrX(i,1:end));
        end

        freqItemset = cat(1, freqItemset, freqItemX');
        freqItemX = char(freqItemX');
    end    
end