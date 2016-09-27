import ReadData;
from copy import deepcopy;
from igraph import *
from scipy import stats
import numpy as np

#===============================================================================
# Create iGraph graph object
#===============================================================================
def generateDailyGraph(dateLi):
    myUsrDict = deepcopy(ReadData.usrDict);
    myMovDict = deepcopy(ReadData.movDict);
    g = Graph()

    for (uid, mid) in dateLi:
        # add vertex for user if it does not already exist
        if myUsrDict[uid][1] == 0:
            myUsrDict[uid][1] = 1;
            g.add_vertex(name=uid, type='user', gender=myUsrDict[uid][0][0], age=myUsrDict[uid][0][1])

        # add vertex for movie if it does not already exist
        if myMovDict[mid][1] == 0:
            myMovDict[mid][1] = 1;
            g.add_vertex(name=mid, type='movie', title=myMovDict[mid][0][0], genre=myMovDict[mid][0][1])

        uV = g.vs.find(str(uid)).index
        mV = g.vs.find(str(mid)).index

        # add edge from user to movie
        g.add_edge(uV, mV)

    return g

#===============================================================================
# The main function
#===============================================================================
def main():
    ReadData.readUserInfo();
    ReadData.readMovieInfo();
    ReadData.readRatingInfo();
    dates = ReadData.dateDict;
    dateLi = dates['2000-04-25']; # change the date here if desired
    g = generateDailyGraph(dateLi);
    #summary(g)

    # Calculate some metrics, including diameter (required by assignment) for entire graph
    diameter = Graph.diameter(g)
    radius = Graph.radius(g)
    ec = Graph.eccentricity(g)

    eigen = Graph.eigenvector_centrality(g)
    betweenness = Graph.betweenness(g)
    closeness = Graph.closeness(g)
    degree = Graph.degree(g)

    comedyVs = g.vs.select(lambda x:x["type"]=="movie" and x["genre"]=="Comedy")
    dramaVs = g.vs.select(lambda x: x["type"] == "movie" and x["genre"] == "Documentary")

    print "Comedy Movie Analyis:"
    print "Comedy Degree: " + str(g.degree(comedyVs))
    print "Comedy Eigen vector centrality: " + str(g.eigenvector_centrality(comedyVs))
    print "Comedy Betweenness: " + str(g.betweenness(comedyVs))
    print "Comedy Closeness: " + str(g.closeness(comedyVs))

    print "Drama Movie Analyis:"
    print "Drama Degree: " + str(g.degree(dramaVs))
    print "Drama Eigen vector centrality: " + str(g.eigenvector_centrality(dramaVs))
    print "Drama Betweenness: " + str(g.betweenness(dramaVs))
    print "Drama Closeness: " + str(g.closeness(dramaVs))

    t, p =  stats.ttest_ind(np.array(g.betweenness(comedyVs)), np.array(g.betweenness(dramaVs)), equal_var=False)
    print t
    print p
    # Null hypothesis cannot be rejected at any reasonable significance level due to large p

#===============================================================================
# Execution
#===============================================================================
if __name__ == '__main__':
    main();


