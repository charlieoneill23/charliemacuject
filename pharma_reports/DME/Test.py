from Vision import *

if __name__ == "__main__":
    obj = Vision('all', '/brendanvote.csv')
    print(obj.results_table())