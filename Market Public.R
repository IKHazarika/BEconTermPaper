publicSymmetricMarket$FracOfHerders <- 1 - publicSymmetricMarket$FracOfRandBid - publicSymmetricMarket$FracOfTruth

library(texreg)

model1 <- lm(NoOfTransactions ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density, data = publicSymmetricMarket)
summary(model1)

model2 <- lm(NoOfTransactions ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + FracOfHerders*TypeHomophily + FracOfRandBid*TypeHomophily, data = publicSymmetricMarket)
summary(model2)

model3 <- lm(NoOfTransactions ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + TrueValue, data = publicSymmetricMarket)
summary(model3)

model4 <- lm(NoOfTransactions ~ NumSellers + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + FracOfHerders*TypeHomophily + FracOfRandBid*TypeHomophily + TrueValue, data = publicSymmetricMarket)
summary(model4)

texreg(list(model1, model2, model3, model4))
