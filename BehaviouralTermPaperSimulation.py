#This is part of the code used in the term paper submitted by Ishan Kashyap Hazarika for the Behavioural Economics Course at DSE in Winter 2022
#The paper investigates how herding as a heuristic, as opposed to a rational strategy, performs vis-a-vis other strategies in different social networks
#The paper uses simulations (as coded below) where double-auctions are held between pre-designated buyers and sellers, who bid and ask using different strategies
#Separate simulations are run for private value and common value auctions

##Private Value Double Auctions

#Choose number of agents, n, an even number, randomly from 10 to 100
#Generate n agents as an n-member list
#Each agent is a 4-tuple
#The first value in the tuple is how much the agent values the good
#We start with a uniform distribution and then experiment with other distributions
#The second value in the tuple specifies whether the agent is a buyer or seller
#We make sure that the number of buyers and sellers is the same
#The third value in the tuple specifies the type of the agent: truth tellers, random bidder or herder
#Rational bidders bid their true bids, random bidders bid a random value from 0 to 100, herders use a herding heuristic to bid, we run different simulations for each heuristic
#We vary their shares randomly
#The fourth value lists the nodes whose values and types are visible to the agent
#This is selected on the basis of a randomly selected level of homophily in values, homophily in types, homophily in buyers/ sellers connectedness
#For value homophily, we divide the agents into two categories: those with value less than 0.5 and others

#Each seller has exactly 1 unit of the good which she decides whether to sell or not and to whom

#Each auction takes place as follows:
#Each agent chooses her bid simultaneously
#Then one by one, the highest bidder and lowest asker exchange the good at price 0.5(ask + bid)
#This keeps happening till the ask value exceeds the bid value

import numpy as np

#We write the code to generate a social network with randomly chosen number of sellers/ buyers, values, agents types and links
#We begin with a uniform distribution for values

#This function calculates the probabolity of two given nodes, a1 and a2, being connected
#The formula used is stated, described and justified in the manuscript
def connectProb(a1, a2, dns, probSameValue, probSameType, probSamePosi, valuHom, typeHom, posiHom):
    valType1 = 0
    valType2 = 0
    
    if a1[0] >= 0.5:
        valType1 = 1
    if a2[0] >= 0.5:
        valType2 = 1
    
    valDif = 0    
    typeDif = 0
    posiDif = 0
    
    if valType1 != valType2:
        valDif = 1
    if a1[1] != a2[1]:
        typeDif = 1
    if a1[2] != a2[2]:
        posiDif = 1
    
    probBase = dns - (probSameValue - 1 + probSameValue) * valuHom - (probSameType - 1 + probSameType) * typeHom - (probSamePosi - 1 + probSamePosi) * posiHom
    probConnect = probBase - valDif * valuHom - typeDif * typeHom - posiDif * posiHom
    
    return probConnect

#This function generates the social network of agents for each round of the simulation
def generateNetwork():
    agents = []
    
    #The number of agents and the fraction of agents following particular strategies is chosen randomly
    numSellers = np.random.randint(5, 50)
    numBuyers = numSellers
    valuesList = np.random.uniform(0, 1, numSellers*2)
    truthFraction = np.random.uniform(0, 1)
    randomFraction = np.random.uniform(0, 1 - truthFraction)
    
    #Characteristics of the network of interest in the paper, namely, the density, type, position and value homophily are specified randomly
    #The upper and lower limits for the homophilies are decided based on the value of the density, as specified below
    #The definitions of these characteristics are included in the manuscript
    density = np.random.uniform(0.1, 0.9)
    if density >= 0.5:
        ulim = 1 - density
        typeHom = np.random.uniform(0, ulim)
        posiHom = np.random.uniform(0, ulim)
        valuHom = np.random.uniform(0, ulim)
    if density < 0.5:
        ulim = density
        typeHom = np.random.uniform(0, ulim)
        posiHom = np.random.uniform(0, ulim)
        valuHom = np.random.uniform(0, ulim)
    
    #These are calculated for the adjustment factor needed to maintain independence of density and homophilies. This is necessisated by reasons discussed in the manuscript
    probSameValue = 0.5
    probSameType = truthFraction**2 + randomFraction**2 + (1 - truthFraction - randomFraction)**2
    probSamePosi = 0.5
    
    #Each buyer is assigned a type, as described in the manuscript
    for agent in range(numSellers):
        val = valuesList[agent]
        posi = 'B'
        
        typeLottery = np.random.uniform(0, 1)
        if typeLottery < truthFraction:
            typ = 'tt'
        if typeLottery >= truthFraction and typeLottery < truthFraction + randomFraction:
            typ = 'rd'
        if typeLottery > truthFraction + randomFraction:
            typ = 'hd'
        
        #This is added for convenience, will be clear later on
        connectedNodes = []
        agents.append([val, posi, typ, connectedNodes])
    
    #Each seller is assigned a type, as described in the manuscript
    for agent in range(numSellers):
        val = valuesList[agent]
        posi = 'S'
        
        typeLottery = np.random.uniform(0, 1)
        if typeLottery < truthFraction:
            typ = 'tt'
        if typeLottery >= truthFraction and typeLottery < truthFraction + randomFraction:
            typ = 'rd'
        if typeLottery > truthFraction + randomFraction:
            typ = 'hd'
        
        #This is added for convenience, will be clear later on
        connectedNodes = []
        agents.append([val, posi, typ, connectedNodes])
    
    #For each pair of nodes (agents) agent1 and agent2, the probability of being connected is calculated using the connectProb function defined earlier, and they are connected based on that probability
    #Note that this is NOT a symmetric graph, so we repeat the exercise twice for each pair
    for agent1 in range(numSellers * 2):
        for agent2 in range(numSellers * 2):
            if agent1 != agent2:
                connectLottery = np.random.uniform(0, 1)
                if connectLottery <= connectProb(agents[agent1], agents[agent2], density, probSameValue, probSameType, probSamePosi, valuHom, typeHom, posiHom):
                    agents[agent1][3].append(agent2)
    
    #We define each agent as specified in the beginning of this document
    for agent in agents:
        agent.append(numSellers)
        agent.append(truthFraction)
        agent.append(randomFraction)
        agent.append(typeHom)
        agent.append(posiHom)
        agent.append(valuHom)
    
    return agents

#This function runs the double auction once the network is generated
def runAuction(network):
    #These are calculated for convenience, to be used later on
    numSellers = int(len(network) / 2)
    agents = network
    
    #These are defined to keep track of the number of transactions anf the total surplus generated, as they are of interest in the paper
    transactions = 0
    totalSurplus = 0
    
    #The bids of each agent is calculated here
    for agent in agents:
        if agent[2] == 'tt':
            #The bid/ ask of a "truth teller" is simply their value
            agent.append(agent[0])
        if agent[2] == 'rd':
            #The bid/ ask of a "random offerer" is randomly chosen
            bid = np.random.uniform(0, 1)
            agent.append(bid)
        if agent[2] == 'hd' and len(agent[3]) == 0:
            #We temporarily assign the value as the bid for "herders", we will modify this later
            agent.append(agent[0])
    
    #For each herder, we calculate the average of the bids of those nodes who are visible to th given herder
    for agent in agents:
        if agent[2] == 'hd' and len(agent[3]) != 0:
            visibleBids = []
            for friend in agent[3]:
                vb = agents[friend][0]
                visibleBids.append(vb)
            myBid = np.mean(visibleBids)
            agent.append(myBid)
    
    #We separate the buyers and the sellers into two separate vectors
    buyers = []
    sellers = []
    
    for j in range(numSellers):
        buyers.append(agents[j])
        sellers.append(agents[numSellers + j])
    
    #WE list out the bids and asks separately in the same order as above
    bids = []
    asks = []
    
    for agent in range(numSellers):
        bids.append(buyers[agent][10])
        asks.append(sellers[agent][10])
    
    #We now sort the bids in ascending order and the asks in descending order
    #We begin by copying the vectors defined above because new variable names simply point to older ones in Python, and modifying them would modify the original variables
    #This makes the program a bit slower, but we have no choice.... And for our purposes, it is not too slow, therefore we do not pay much attention to it
    asksOrdered = asks.copy()
    bidsOrdered = bids.copy()
    
    asksOrdered.sort()
    bidsOrdered.sort(reverse = True)
    
    #The transactions are held: the highest bidder is paired with the lowest asker, the second highest bidder with the second lowest asker and so on
    for transaction in range(numSellers):
        ask = asksOrdered[transaction]
        bid = bidsOrdered[transaction]
        
        seller = asks.index(ask)
        buyer = bids.index(bid)
        buyer = numSellers + buyer
        
        sellerValue = agents[seller][0]
        buyerValue = agents[buyer][0]
        
        #The transaction is executed only if the ask is less than or equal to the bid
        #The number of transactions and marginal surplus is recorded
        #The price is the average of the ask and the bid
        if ask <= bid:
            transactions += 1
            price = 0.5 * (ask + bid)
            sellerSurplus = price - sellerValue
            buyerSurplus = buyerValue - price
            
            agents[seller].append(sellerSurplus)
            agents[buyer].append(buyerSurplus)
            
            totalSurplus += sellerSurplus + buyerSurplus
            
        #Otherwise, no transaction takes place, and the surplues are 0
        if ask > bid:
            sellerSurplus = 0
            buyerSurplus = 0
            
            agents[seller].append(sellerSurplus)
            agents[buyer].append(buyerSurplus)
        
    #At the end of the simulation, the data included in the agents vector, the number of transactions and the total surplus generated are returned
    #Individual level statistics are included in the agents vector
    return [agents, transactions, totalSurplus]

#We now actually begin the simulation

#These are defined to record statistics of interest
marketStats = []
agentStats = []

#We run the simulation 1000 times, by generating the network and then running the auction in each round
for turn in range(1000):
    network = generateNetwork()
    auction = runAuction(network)
    
    marketStats.append([network[0][4] * 2, network[0][5], network[0][6], network[0][7], network[0][8], network[0][9], auction[1], auction[2]])
    for k in range(len(auction[0])):
        auction[0][k][3] = len(auction[0][k][3])
        agentStats.append(auction[0][k])

#We now convert the data into suitable format for data analysis
import pandas as pd

#The data is bifurcated into two: market level data containing market level variables and agent level data including agent level variables
marketLevelData = pd.DataFrame(marketStats, columns = ['NumSellers', 'FracOfTruth', 'NumOfRandBid', 'TypeHomophily', 'PositionHomophily', 'ValueHomophily', 'NoOfTransactions', 'TotalSurplus'])
agentLevelData = pd.DataFrame(agentStats, columns = ['Value', 'Position', 'Type', 'Connectedness', 'Number of agents', 'FracOfTruth', 'NumOfRandBid', 'TypeHomophily', 'PositionHomophily', 'ValueHomophily', 'Offer', 'Surplus', 'dfd', 'fgg', 'dfg'])
agentLevelData

#We also export the data to excel
import openpyxl

marketLevelData.to_excel(r'E:\Behavioural Economics Term Paper\Data\Private Symmetric\privateSymmetricMarket.xlsx')
print('Done')
agentLevelData.to_excel(r'E:\Behavioural Economics Term Paper\Data\Private Symmetric\privateSymmetricAgent.xlsx')
print('Done')
