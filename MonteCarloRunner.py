from MonteCarlo.MonteCarloSearcher import MonteCarloSearcher
# import git
# import os

monte_carlo_searcher = MonteCarloSearcher()
#monte_carlo_searcher.makeNewTree()
for i in range(0, 20):
    monte_carlo_searcher.loadTreeData()
    try:
        monte_carlo_searcher.runAlgorihm(120)
    except Exception:
        monte_carlo_searcher.saveDataToFile()
        continue


# my_repo = git.Repo(os.getcwd())
# if my_repo.is_dirty(untracked_files=True):
#     print('Changes detected.')
#     # print(my_repo.git.diff(my_repo.head.commit.tree))
#     my_repo.index.add('MonteCarloRunner.py',open("MonteCarlo\database.db", "r"))
#     my_repo.index.commit('database update')
# print(my_repo.remotes.origin.push())




    
