#We use the dataset generated in the Python code file
#The data is self generated and organised carefully to NOT require any cleaning

#We define the "fraction of herders" variable described in the manuscript

privateSymmetricMarket$FracOfHerders <- 1 - privateSymmetricMarket$FracOfRandBid - privateSymmetricMarket$FracOfTruth

#We run 6 models described at length in the manuscript and export the results to Latex

model1 <- lm(TotalSurplus ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density, data = privateSymmetricMarket)
summary(model1)

model2 <- lm(TotalSurplus ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + FracOfHerders*TypeHomophily + FracOfRandBid*TypeHomophily, data = privateSymmetricMarket)
summary(model2)

model3 <- lm(TotalSurplus ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + NoOfTransactions, data = privateSymmetricMarket)
summary(model1)

model4 <- lm(TotalSurplus ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + NoOfTransactions + FracOfHerders*TypeHomophily + FracOfRandBid*TypeHomophily, data = privateSymmetricMarket)
summary(model2)

library(texreg)
texreg(list(model1, model2, model3, model4))

model5 <- lm(NoOfTransactions ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density, data = privateSymmetricMarket)
summary(model1)

model6 <- lm(NoOfTransactions ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + FracOfHerders*TypeHomophily + FracOfRandBid*TypeHomophily, data = privateSymmetricMarket)
summary(model2)

texreg(list(model5, model6))
