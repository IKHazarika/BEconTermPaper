#We use the dataset generated in the Python code file
#The data is self generated and organised carefully to NOT require any cleaning

#We define the "fraction of herders" variable described in the manuscript

#We run 4 models described at length in the manuscript

publicSymmetricMarket$FracOfHerders <- 1 - publicSymmetricMarket$FracOfRandBid - publicSymmetricMarket$FracOfTruth

model1 <- lm(NoOfTransactions ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density, data = publicSymmetricMarket)
summary(model1)

model2 <- lm(NoOfTransactions ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + FracOfHerders*TypeHomophily + FracOfRandBid*TypeHomophily, data = publicSymmetricMarket)
summary(model2)

model3 <- lm(NoOfTransactions ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + TrueValue, data = publicSymmetricMarket)
summary(model3)

model4 <- lm(NoOfTransactions ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + FracOfHerders*TypeHomophily + FracOfRandBid*TypeHomophily + TrueValue, data = publicSymmetricMarket)
summary(model4)

#We export the results to Latex
library(texreg)
texreg(list(model1, model2, model3, model4))
