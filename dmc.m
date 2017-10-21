% Load the fisher iris data set, that will be available in meas
load fisheriris

% Actually getting the dataset
X = meas(:,3:4);

% Calculating preditions and plotting points
figure;

plot(X(:,1), X(:,2), 'k*', 'MarkerSize', 8);
title 'Iris';
xlabel 'Tamanho das Pétalas (cm)'; 
ylabel 'Largura das Pétalas (cm)';

rng(1);
[idx, C] = kmeans(X, 3); % Calculate means

x1 = min(X(:,1)):0.01:max(X(:,1));
x2 = min(X(:,2)):0.01:max(X(:,2));
[x1G, x2G] = meshgrid(x1, x2);
XGrid = [x1G(:), x2G(:)];

idx2Region = kmeans(XGrid, 3, 'MaxIter', 1, 'Start', C);

% Colored chart
figure;
gscatter(XGrid(:,1), XGrid(:,2), idx2Region,...
[1,0.90,0.90;0.90,1,0.90;0.90,0.90,1],'..');
 
hold on;
plot(X(:,1), X(:,2), 'k*','MarkerSize', 8);
title 'Iris';
xlabel 'Tamanho das Pétalas (cm)'; 
ylabel 'Largura das Pétalas (cm)';
legend('Região 1', 'Região 2', 'Região 3', 'Dados', 'Location', 'northwest');
hold off;