import ReadData;
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from networkx.algorithms import bipartite

#===============================================================================
# Create networkx graph object
#===============================================================================
def generateDailyGraph(dateLi):
    myUsrDict = deepcopy(ReadData.usrDict);
    myMovDict = deepcopy(ReadData.movDict);
    gx = nx.Graph()

    users = []
    movies = []
    edges = []
    for (uid, mid) in dateLi:
        # add vertex for user if it does not already exist
        if myUsrDict[uid][1] == 0:
            myUsrDict[uid][1] = 1;
            users.append(uid)

        # add vertex for movie if it does not already exist
        if myMovDict[mid][1] == 0:
            myMovDict[mid][1] = 1;
            movies.append(mid)

        edges.append((uid, mid))

    gx.add_nodes_from(users, bipartite=0)
    gx.add_nodes_from(movies, bipartite=1)
    gx.add_edges_from(edges)

    nx.is_connected(gx)

    bottom_nodes, top_nodes = bipartite.sets(gx)

    return gx, bottom_nodes, top_nodes

#===============================================================================
# The main function
#===============================================================================
def main():
    ReadData.readUserInfo();
    ReadData.readMovieInfo();
    ReadData.readRatingInfo();
    dates = ReadData.dateDict;
    dateLi = dates['2000-04-26']; # change the date here if desired.  The selected date only has 3 users.
    g, movies, users = generateDailyGraph(dateLi);

    # generate visual for full bipartite graph
    pos = dict()
    pos.update((n, (1, i * 100)) for i, n in enumerate(users)) # put nodes from users at x=1
    pos.update((n, (2, i)) for i, n in enumerate(movies)) # put nodes from movies at x=2
    nx.draw(g, pos=pos)
    #plt.show()
    plt.savefig("full_bip.png")
    plt.clf()

    # project bipartite graph onto user nodes
    U1 = bipartite.projected_graph(g, users)
    nx.draw(U1)
    #plt.show()
    plt.savefig('Users_one_mode.png')
    plt.clf()

    # Determine number of peers for each user
    peers = []
    for u in users:
        peers.append(U1.degree(u))

    users_df = pd.DataFrame({'num_peers': peers, 'name': list(users)})
    print users_df

    print('')
    print('')
    print('Summary Statistics for Friend Counts')
    print('Min: %d' % min(peers))
    print('Max: %d' % max(peers))
    print('Avg: %d' % np.mean(peers))
    print('Std: %d' % np.std(peers))

    users_df.plot.bar()
    #plt.show()
    plt.savefig('Users_bar.png')
    plt.clf()

    # project bipartite graph onto user nodes
    M1 = bipartite.projected_graph(g, movies)
    nx.draw(M1)
    #plt.show()
    plt.savefig('Movies_one_mode.png')
    plt.clf()

    # Determine number of peers for each user
    num_similar_movies = []
    for m in movies:
        num_similar_movies.append(M1.degree(m))

    movies_df = pd.DataFrame({'num_similar_movies': num_similar_movies, 'movie_id': list(movies)})
    print movies_df

    movies_df.plot.bar()
    #plt.show()
    plt.savefig('movies_bar.png')
    plt.clf()

    # project bipartite graph onto user nodes
    M2 = bipartite.weighted_projected_graph(g, movies)
    nx.draw(M2)
    # plt.show()
    plt.savefig('Movies_one_mode_weighted.png')
    plt.clf()

    # Determine number of peers for each user
    num_similar_movies = []
    for m in movies:
        num_similar_movies.append(M2.degree(m))

    movies_df_w = pd.DataFrame({'num_similar_movies': num_similar_movies, 'movie_id': list(movies)})
    print movies_df_w


#===============================================================================
# Execution
#===============================================================================
if __name__ == '__main__':
    main();

