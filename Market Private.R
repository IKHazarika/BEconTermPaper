privateSymmetricMarket[1,]

privateSymmetricMarket$FracOfHerders <- 1 - privateSymmetricMarket$FracOfRandBid - privateSymmetricMarket$FracOfTruth

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
