from MonteCarlo.MonteCarloSearcher import MonteCarloSearcher

monte_carlo_searcher = MonteCarloSearcher()
# monte_carlo_searcher.makeNewTree()
for i in range(0, 10):
    monte_carlo_searcher.loadTreeData()
    monte_carlo_searcher.runAlgorihm(100)




    
