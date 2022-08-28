publicSymmetricAgent$SignalError <- abs(publicSymmetricAgent$Signal - publicSymmetricAgent$TrueValue)
publicSymmetricAgent$FracOfHerders <- 1 - publicSymmetricAgent$FracOfRandBid - publicSymmetricAgent$FracOfRandBid

model1 <- lm(Surplus ~ SignalError + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density, data = publicSymmetricAgent)
summary(model1)

model2 <- lm(Surplus ~ SignalError + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + SignalError*ValueHomophily + Type*TypeHomophily + Position*PositionHomophily, data = publicSymmetricAgent)
summary(model2)

model3 <- lm(Surplus ~ SignalError + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + SignalError*ValueHomophily + Type*TypeHomophily + Position*PositionHomophily + FracOfRandBid*TypeHomophily, data = publicSymmetricAgent)
summary(model3)

model4 <- lm(Surplus ~ SignalError + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + SignalError*ValueHomophily + Type*TypeHomophily + Position*PositionHomophily + FracOfRandBid*TypeHomophily + FracOfRandBid*SignalError, data = publicSymmetricAgent)
summary(model4)

library(texreg)
texreg(list(model1, model2, model3, model4))