import numpy as np
import pandas as pd


# Fixes
# 1) Investigate the income numbers becasue they look too big
# 2) Take into account the varying growth rates (right now you assumed expenses grow at the same rate)
# Inputs
capRate = .04
###############   Cost Schedule   ##############
# Calculate lease up and stabilized expenses
LeaseUp_Annual_ExpensePerUnit = -4838.96  # Calculated from sum in Excel
Stabilized_Annual_ExpensePerUnit = -5525.69  # Calculated from sum in Excel
Stabilized_Annual_GrowthRate = 1.02
Units = 260

LeaseUpExpenseAnnual = LeaseUp_Annual_ExpensePerUnit * Units
StabilizedExpense_Base = Stabilized_Annual_ExpensePerUnit * Units


def StabilizedExpenseAnnualFunction(
        yearPastStabilizedCommencement):  # A function that calculates the expense given the year
    expense = StabilizedExpense_Base * Stabilized_Annual_GrowthRate ** yearPastStabilizedCommencement
    return expense


# Calculate lease up and stabilized rent
LeaseUpVacancyRate = .33
StabilizedVacancyRate = .02
LeaseUpRental_Monthly_IncomePerUnitAve = 2.45 * 627  # $2.45 average per square foot and 627 square foot average
StabilizedRental_Monthly_IncomePerUnitAve = 2.60 * 627  # $2.60 average per square foot and 627 square foot average
RentGrowthRate = 1.025

LeaseUpParking_Monthly_IncomePerStall = 125
StabilizedParking_Monthly_IncomePerStall = 150
Stalls = 173
ParkingGrowthRate = 1.025

LeaseUpStorage_Monthly_IncomePerLocker = 50
StabilizedStorage_Monthly_IncomePerLocker = 60
Lockers = 74
StorageGrowthRate = 1.025

LeaseUpRentAnnual = ((LeaseUpRental_Monthly_IncomePerUnitAve * Units * (1 - LeaseUpVacancyRate)) + (
        LeaseUpParking_Monthly_IncomePerStall * Stalls * (1 - LeaseUpVacancyRate)) + (
                             LeaseUpStorage_Monthly_IncomePerLocker * Lockers * (
                             1 - LeaseUpVacancyRate))) * 12  # Lease up rent is the rent
# average per unit multiplied by the number of units multiplied by 1 minus the vacancy rate times 12 to make it annual.
# We do this for the units, parking and storage

StabilizedRentAnnual_Base_Units = (StabilizedRental_Monthly_IncomePerUnitAve * Units * (1 - StabilizedVacancyRate)) * 12
StabilizedRentAnnual_Base_Parking = (StabilizedParking_Monthly_IncomePerStall * Stalls * (
            1 - StabilizedVacancyRate)) * 12
StabilizedRentAnnual_Base_Storage = (StabilizedStorage_Monthly_IncomePerLocker * Lockers * (
            1 - StabilizedVacancyRate)) * 12


# Lease up rent is the
# rent average per unit multiplied by the number of units multiplied by 1 minus the vacancy rate times 12 to make it
# annual. We do this for the units, parking and storage

def StabilizedRentAnnualFunction(
        yearPastStabilizedCommencement):  # A function that calculates the expense given the year
    rent = StabilizedRentAnnual_Base_Units * RentGrowthRate ** yearPastStabilizedCommencement + \
           StabilizedRentAnnual_Base_Parking * ParkingGrowthRate ** yearPastStabilizedCommencement + \
           StabilizedRentAnnual_Base_Storage * StorageGrowthRate ** yearPastStabilizedCommencement
    return rent

# Basic
CostSchedule = dict(LandAquisitionCost=-10000000, SoftCosts=-11000000, HardCosts=-53000000, FinancingFees=-1000000,
                    InterestReserve=-8000000)
# ExpenseSchedule = dict(LeaseUpRent= , SatbilizedRent= , SalesProceeds=)
ConstructionLength = 27
LeaseUpLength = 12
StabilizedLength = 61
IncomeTimeline2a = [CostSchedule['LandAquisitionCost'] + CostSchedule['SoftCosts'] + CostSchedule['FinancingFees']]
for i in range(ConstructionLength):
    IncomeTimeline2a.append(CostSchedule['HardCosts'] / ConstructionLength)

for i in range(LeaseUpLength):
    IncomeTimeline2a.append(LeaseUpExpenseAnnual/12 + LeaseUpRentAnnual/12)

month = 1  # A counter to tell when we have reached one year
year = 0
for i in range(StabilizedLength):
    if month == 13:
        month = 1
        year = year + 1
    IncomeTimeline2a.append(StabilizedExpenseAnnualFunction(year) + StabilizedRentAnnualFunction(year)) # Need to make annual increases
    month = month + 1

# Sale proceeds (does the sale happen at the start of the last month? Do we get pad rent the last month?
annualNOI = np.array(IncomeTimeline2a[-12:]).sum()
saleAmount = annualNOI/capRate
IncomeTimeline2a[-1] = IncomeTimeline2a[-1] + saleAmount

IncomeTimeline2a_Series = pd.Series(IncomeTimeline2a)
###############   Timeline   ##############
LandAquisition = dict(CostsDeployed=CostSchedule['LandAquisitionCost'], IncomeRecieved=0, Expenses=0,
                      Period=list(range(1, 2)), Notes="")
PreConstruction = dict(CostsDeployed=CostSchedule['SoftCosts'] + CostSchedule['FinancingFees'], IncomeRecieved=0,
                       Expenses=0, Period=list(range(1, 2)), Notes="")
Construction = dict(CostsDeployed=CostSchedule['HardCosts'], IncomeRecieved=0, Expenses=0, Period=list(range(2, 29)),
                    Notes="Costs deployed evenly during period")
LeaseUp = dict(CostsDeployed=0, IncomeRecieved=CostSchedule['LeaseUpRent'], Expenses=LeaseUpExpenses,
               Period=list(range(29, 41)), Notes="")
FullyStabilized = dict(CostsDeployed=, IncomeRecieved=StabilizedRent, Expenses=StabilizedExpenses,
                       Period=list(range(41, 42)), Notes="")
Sale = dict(CostsDeployed=0, IncomeRecieved=SaleProceeds, Expenses=0, Period=list(range(41, 42)), Notes="")
Timeline = dict(LandAquisition=LandAquisition, PreConstruction=PreConstruction, Contruction=Construction,
                LeaseUp=LeaseUp, FullyStabilized=FullyStabilized, Sale=Sale)

###############   Exit Assumptions   ##############


###############   Financing Assumptions   ##############


###############   Operating Assumptions   ##############
