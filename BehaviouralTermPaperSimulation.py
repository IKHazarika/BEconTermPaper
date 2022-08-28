#!/usr/bin/env python
# coding: utf-8

# In[222]:


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


# In[223]:


import numpy as np


# In[224]:


#We write the code to generate a social network with randomly chosen number of sellers/ buyers, values, agents types and links
#We begin with a uniform distribution for values

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

def generateNetwork():
    agents = []
    
    numSellers = np.random.randint(5, 50)
    numBuyers = numSellers
    valuesList = np.random.uniform(0, 1, numSellers*2)
    truthFraction = np.random.uniform(0, 1)
    randomFraction = np.random.uniform(0, 1 - truthFraction)
    
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
    
    probSameValue = 0.5
    probSameType = truthFraction**2 + randomFraction**2 + (1 - truthFraction - randomFraction)**2
    probSamePosi = 0.5
    
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
        
        connectedNodes = []
        agents.append([val, posi, typ, connectedNodes])
    
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
        
        connectedNodes = []
        agents.append([val, posi, typ, connectedNodes])
    
    for agent1 in range(numSellers * 2):
        for agent2 in range(numSellers * 2):
            if agent1 != agent2:
                connectLottery = np.random.uniform(0, 1)
                if connectLottery <= connectProb(agents[agent1], agents[agent2], density, probSameValue, probSameType, probSamePosi, valuHom, typeHom, posiHom):
                    agents[agent1][3].append(agent2)
    
    for agent in agents:
        agent.append(numSellers)
        agent.append(truthFraction)
        agent.append(randomFraction)
        agent.append(typeHom)
        agent.append(posiHom)
        agent.append(valuHom)
    
    return agents

def runAuction(network):
    numSellers = int(len(network) / 2)
    agents = network
    
    transactions = 0
    totalSurplus = 0
    
    for agent in agents:
        if agent[2] == 'tt':
            agent.append(agent[0])
        if agent[2] == 'rd':
            bid = np.random.uniform(0, 1)
            agent.append(bid)
        if agent[2] == 'hd' and len(agent[3]) == 0:
            agent.append(agent[0])
    
    for agent in agents:
        if agent[2] == 'hd' and len(agent[3]) != 0:
            visibleBids = []
            for friend in agent[3]:
                vb = agents[friend][0]
                visibleBids.append(vb)
            myBid = np.mean(visibleBids)
            agent.append(myBid)
    
    buyers = []
    sellers = []
    
    for j in range(numSellers):
        buyers.append(agents[j])
        sellers.append(agents[numSellers + j])
    
    bids = []
    asks = []
    
    for agent in range(numSellers):
        bids.append(buyers[agent][10])
        asks.append(sellers[agent][10])
    
    asksOrdered = asks.copy()
    bidsOrdered = bids.copy()
    
    asksOrdered.sort()
    bidsOrdered.sort(reverse = True)
    
    for transaction in range(numSellers):
        ask = asksOrdered[transaction]
        bid = bidsOrdered[transaction]
        
        seller = asks.index(ask)
        buyer = bids.index(bid)
        buyer = numSellers + buyer
        
        sellerValue = agents[seller][0]
        buyerValue = agents[buyer][0]
        
        if ask <= bid:
            transactions += 1
            price = 0.5 * (ask + bid)
            sellerSurplus = price - sellerValue
            buyerSurplus = buyerValue - price
            
            agents[seller].append(sellerSurplus)
            agents[buyer].append(buyerSurplus)
            
            totalSurplus += sellerSurplus + buyerSurplus
            
        if ask > bid:
            sellerSurplus = 0
            buyerSurplus = 0
            
            agents[seller].append(sellerSurplus)
            agents[buyer].append(buyerSurplus)
        
    return [agents, transactions, totalSurplus]


# In[225]:


marketStats = []
agentStats = []

for turn in range(1000):
    network = generateNetwork()
    auction = runAuction(network)
    
    marketStats.append([network[0][4] * 2, network[0][5], network[0][6], network[0][7], network[0][8], network[0][9], auction[1], auction[2]])
    for k in range(len(auction[0])):
        auction[0][k][3] = len(auction[0][k][3])
        agentStats.append(auction[0][k])

agentStats[3]


# In[226]:


import pandas as pd


# In[230]:


marketLevelData = pd.DataFrame(marketStats, columns = ['NumSellers', 'FracOfTruth', 'NumOfRandBid', 'TypeHomophily', 'PositionHomophily', 'ValueHomophily', 'NoOfTransactions', 'TotalSurplus'])
agentLevelData = pd.DataFrame(agentStats, columns = ['Value', 'Position', 'Type', 'Connectedness', 'Number of agents', 'FracOfTruth', 'NumOfRandBid', 'TypeHomophily', 'PositionHomophily', 'ValueHomophily', 'Offer', 'Surplus', 'dfd', 'fgg', 'dfg'])
agentLevelData


# In[231]:


import openpyxl


# In[232]:


marketLevelData.to_excel(r'E:\Behavioural Economics Term Paper\Data\Private Symmetric\privateSymmetricMarket.xlsx')
print('Done')
agentLevelData.to_excel(r'E:\Behavioural Economics Term Paper\Data\Private Symmetric\privateSymmetricAgent.xlsx')
print('Done')


# In[234]:


#We now try a skewed distribution
#For this, we will redefine the network generating function to have a skewness parameter, and randomly choose the parameter before every simulation
#We draw the values from a beta distribution with support 0 to 1

def generateNetwork():
    agents = []
    
    numSellers = np.random.randint(5, 50)
    numBuyers = numSellers
    
    
    valuesList = np.random.uniform(0, 1, numSellers*2)
    
    truthFraction = np.random.uniform(0, 1)
    randomFraction = np.random.uniform(0, 1 - truthFraction)
    
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
    
    probSameValue = 0.5
    probSameType = truthFraction**2 + randomFraction**2 + (1 - truthFraction - randomFraction)**2
    probSamePosi = 0.5
    
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
        
        connectedNodes = []
        agents.append([val, posi, typ, connectedNodes])
    
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
        
        connectedNodes = []
        agents.append([val, posi, typ, connectedNodes])
    
    for agent1 in range(numSellers * 2):
        for agent2 in range(numSellers * 2):
            if agent1 != agent2:
                connectLottery = np.random.uniform(0, 1)
                if connectLottery <= connectProb(agents[agent1], agents[agent2], density, probSameValue, probSameType, probSamePosi, valuHom, typeHom, posiHom):
                    agents[agent1][3].append(agent2)
    
    for agent in agents:
        agent.append(numSellers)
        agent.append(truthFraction)
        agent.append(randomFraction)
        agent.append(typeHom)
        agent.append(posiHom)
        agent.append(valuHom)
    
    return agents


# In[252]:


from sympy import *

a, b, c, d, x, skw, mn = symbols('a, b, c, d, x, skw, mn')

#intg = integrate(fx, (x, 0, 1))

#mean = integrate(fx * x, (x, 0, 1))

#variance = integrate(fx * x**2, (x, 0, 1)) - mean**2
#sd = variance**0.5

#zval = (x - mean) / sd

#skewness = integrate(fx * zval**3, (x, 0, 1))

from sympy.calculus.util import *

intv = Interval(0, 1)
minval = minimum(fx, x, intv)

