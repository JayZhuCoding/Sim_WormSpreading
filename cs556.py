from networkx import *
import csv
import random
import matplotlib.pyplot as plt

#Create Graph - Random
def creategraph():
    V=600 # nodes
    E=2000 # edges

    G=gnm_random_graph(V,E)
    nx.draw(G)
    #plt.show()
    #Generate CSV file
    file = open("Random_Network.CSV", "w")
    for line in nx.generate_edgelist(G, delimiter=',', data=False):
        file.write(line)
        file.write("\n")

#Read CSV file
def readcsv():
    file=open("Random_Network.CSV", 'rb')
    G1=nx.read_edgelist(file, delimiter=',',nodetype=int)
    return G1

def simulation(G1, p, WormList):
    time = 0
    plt.figure()
    while len(WormList) < number_of_nodes(G1):
        time+=1
        for edge in G1.edges():
            if (edge[1] in WormList and edge[0] not in WormList) or \
                    (edge[1] not in WormList and edge[0] in WormList):
                if random.random() < p:
                    if edge[1] in WormList:
                        WormList.append(edge[0])
                    else:
                        WormList.append(edge[1])
        plt.plot(time, len(WormList), marker = 'o', color='b')
    plt.xlabel('Time')
    plt.ylabel('Bad Nodes')
    plt.title('Worm Spreading')
    plt.show()
    return time

def simulation2(G1, p, WormList, p2, CureList):
    time = 0
    while len(WormList) > 0:
        time+=1
        #
        for edge in G1.edges():
            if (edge[1] in WormList and edge[0] not in WormList) or \
                    (edge[1] not in WormList and edge[0] in WormList):
                if (edge[1] not in CureList) and (edge[0] not in CureList):
                    if random.random() < p:
                        if edge[1] not in WormList:
                            WormList.append(edge[1])
                        if edge[0] not in WormList:
                            WormList.append(edge[0])

        #Probability to get cured
        for edge in G1.edges():
            if (edge[1] in CureList and edge[0] not in CureList) or \
                    (edge[1] not in CureList and edge[0] in CureList):
                if random.random() < p2:
                    if edge[0] not in CureList:
                        CureList.append(edge[0])
                    if edge[1] not in CureList:
                        CureList.append(edge[1])
                    if edge[1] in WormList:
                        WormList.remove(edge[1])
                    if edge[0] in WormList:
                        WormList.remove(edge[0])

        #print len(WormList)
        plt.plot(time, len(WormList), marker = 'o', color='r')
    plt.xlabel('Time')
    plt.ylabel('Bad Nodes')
    plt.title('Worm Spreading 2')
    plt.show()
    return time



if __name__=='__main__' :
    p = 0.1
    p2 = 0.05
    iterations = 1
    #These 2 in-outs are initializations for infected and curing node
    worm_node = 100
    cure_node = 333
    #The following function creates a new random network and generate csv file
    # (remove # to activate/put on # to use current csv file)
    creategraph()

    G1 = readcsv()
    #print number_of_nodes(G1)

    #Program1
    i = 0
    sum = 0
    for i in range(iterations):
        #Initialization of Worm
        WormList=[]
        WormList.append(worm_node)
        sum+=simulation(G1, p, WormList)
        percentage = 100*float(i+1)/iterations
        print 'Simulating... %d percent' % percentage
    t = float(sum)/iterations
    print 'The total average number of time unit is: %f' % t

    #Program 2
    i = 0
    sum = 0
    for i in range(iterations):
        #Initialization of Worm
        WormList=[]
        CureList=[]
        WormList.append(worm_node)
        CureList.append(cure_node)
        sum+=simulation2(G1, p, WormList, p2, CureList)
        percentage = 100*float(i+1)/iterations
        print 'Simulating... %d percent' % percentage
    t = float(sum)/iterations
    print 'The total average number of time unit is: %f' % t
