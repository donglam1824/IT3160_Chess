from MonteCarlo.MonteCarloSearcher import MonteCarloSearcher
import git
import os

# monte_carlo_searcher = MonteCarloSearcher()
# # monte_carlo_searcher.makeNewTree()
# for i in range(0, 10):
#     monte_carlo_searcher.loadTreeData()
#     monte_carlo_searcher.runAlgorihm(100)

my_repo = git.Repo(os.getcwd())
if my_repo.is_dirty(untracked_files=True):
    print('Changes detected.')
    my_repo.index.add('MonteCarloRunner.py')
    my_repo.index.commit('database update')




    
