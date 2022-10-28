#We use the data generated in the Python simulation file
#The data is self generated and organised carefully to NOT require any cleaning

#We define a the "signal error" and "fraction of herders" variables which are described in the manuscript
publicSymmetricAgent$SignalError <- abs(publicSymmetricAgent$Signal - publicSymmetricAgent$TrueValue)
publicSymmetricAgent$FracOfHerders <- 1 - publicSymmetricAgent$FracOfRandBid - publicSymmetricAgent$FracOfRandBid

#We run 4 models described at length in the manuscript
model1 <- lm(Surplus ~ SignalError + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density, data = publicSymmetricAgent)
summary(model1)

model2 <- lm(Surplus ~ SignalError + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + SignalError*ValueHomophily + Type*TypeHomophily + Position*PositionHomophily, data = publicSymmetricAgent)
summary(model2)

model3 <- lm(Surplus ~ SignalError + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + SignalError*ValueHomophily + Type*TypeHomophily + Position*PositionHomophily + FracOfRandBid*TypeHomophily, data = publicSymmetricAgent)
summary(model3)

model4 <- lm(Surplus ~ SignalError + Position + Type + Connectedness + NumAgents + FracOfHerders + FracOfRandBid + TypeHomophily + PositionHomophily + ValueHomophily + Density + SignalError*ValueHomophily + Type*TypeHomophily + Position*PositionHomophily + FracOfRandBid*TypeHomophily + FracOfRandBid*SignalError, data = publicSymmetricAgent)
summary(model4)

#We export the results to Latex
library(texreg)
texreg(list(model1, model2, model3, model4))
