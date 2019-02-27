# Inputs
###############   Cost Schedule   ##############
LandAquisitionCost = 10000000
SoftCosts = 11000000
HardCosts = 53000000
FinancingFees = 1000000
InterestReserve = 8000000
CostSchedule = dict(LandAquisitionCost=10000000, SoftCosts=11000000, HardCosts=53000000, FinancingFees=1000000,
                    InterestReserve=8000000)

###############   Timeline   ##############
LandAquisition = dict(CostsDeployed=LandAquisitionCost, IncomeRecieved=0, Expenses=0, Period=list(range(1,2)), Notes="")
PreConstruction = dict(CostsDeployed=SoftCosts+FinancingFees, IncomeRecieved=0, Expenses=0, Period=list(range(1,2)),
                       Notes="")
Contruction = dict(CostsDeployed=HardCosts, IncomeRecieved=0, Expenses=0, Period=list(range(2,29)),
                   Notes="Costs deployed evenly during period")
LeaseUp = dict(CostsDeployed=0, IncomeRecieved=LeaseUpRent, Expenses=LeaseUpExpenses, Period=list(range(29,41)),
               Notes="")
FullyStabilized = dict(CostsDeployed=, IncomeRecieved=StabilizedRent, Expenses=StabilizedExpenses,
                       Period=list(range(41,42)), Notes="")
Sale = dict(CostsDeployed=0, IncomeRecieved=SaleProceeds, Expenses=0, Period=list(range(41,42)), Notes="")
Timeline = dict(LandAquisition=LandAquisition, PreConstruction=PreConstruction, Contruction=Contruction, LeaseUp=LeaseUp
                , FullyStabilized=FullyStabilized, Sale=Sale)

###############   Exit Assumptions   ##############




###############   Financing Assumptions   ##############




###############   Operating Assumptions   ##############


