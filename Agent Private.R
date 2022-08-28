privateSymmetricAgent$NumAgents <- privateSymmetricAgent$`Number of agents`
privateSymmetricAgent$FracOfHerders <- 1 - privateSymmetricAgent$FracOfTruth - privateSymmetricAgent$NumOfRandBid
privateSymmetricAgent$FracOfRandBid <- privateSymmetricAgent$NumOfRandBid

model1 <- lm(Surplus ~ Value + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density, data = privateSymmetricAgent)
summary(model1)

model2 <- lm(Surplus ~ Value + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + Value*ValueHomophily + Type*TypeHomophily + Position*PositionHomophily, data = privateSymmetricAgent)
summary(model2)

model3 <- lm(Surplus ~ Value + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + Value*ValueHomophily + Type*TypeHomophily + Position*PositionHomophily + FracOfRandBid*TypeHomophily, data = privateSymmetricAgent)
summary(model3)

model4 <- lm(Surplus ~ Value + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + Value*ValueHomophily + Type*TypeHomophily + Position*PositionHomophily + FracOfRandBid*TypeHomophily + FracOfRandBid*Value, data = privateSymmetricAgent)
summary(model4)

library(texreg)
texreg(list(model1, model2, model3, model4))
