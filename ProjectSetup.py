# A script that calculates cash flow schedules for the Woodbourne exercise

import numpy as np
import pandas as pd

# Inputs
capRate = .04
Units = 260
LeaseUpVacancyRate = .33
StabilizedVacancyRate = .02
RentGrowthRate = 1.025
ParkingGrowthRate = 1.025
StorageGrowthRate = 1.025
# Basic cost schedule
CostSchedule = dict(LandAquisitionCost=-10000000, SoftCosts=-11000000, HardCosts=-53000000, FinancingFees=-1000000,
                    InterestReserve=-8000000)
ConstructionLength2a = 27  # The length (in months) of the construction period
LeaseUpLength2a = 12  # The length (in months) of the lease up period
StabilizedLength2a = 1  # The length (in months) of the lease up period
ConstructionLength2b = 27  # The length (in months) of the construction period
LeaseUpLength2b = 12  # The length (in months) of the lease up period
StabilizedLength2b = 61  # The length (in months) of the lease up period


#######################################################################################################################
# Calculate lease up and stabilized expenses
LeaseUp_Annual_ExpensePerUnit = -4838.96  # Calculated from sum in Excel of all of the expenses. There is no growth in
# expense during this period, so no need to split up the expenses
LeaseUpExpenseAnnual = LeaseUp_Annual_ExpensePerUnit * Units

# The stabilized expenses and their growth rates
Stabilized_Annual_ExpensePerUnitA = -100
Stabilized_Annual_GrowthRateA = 1.02
Stabilized_Annual_ExpensePerUnitB = -30
Stabilized_Annual_GrowthRateB = 1.02
Stabilized_Annual_ExpensePerUnitC = -30
Stabilized_Annual_GrowthRateC = 1.02
Stabilized_Annual_ExpensePerUnitD = -76
Stabilized_Annual_GrowthRateD = 1.02
Stabilized_Annual_ExpensePerUnitE = -309
Stabilized_Annual_GrowthRateE = 1.03
Stabilized_Annual_ExpensePerUnitF = -354.96
Stabilized_Annual_GrowthRateF = 1.02
Stabilized_Annual_ExpensePerUnitG = -623.53
Stabilized_Annual_GrowthRateG = 1.02
Stabilized_Annual_ExpensePerUnitH = -25.5
Stabilized_Annual_GrowthRateH = 1.02
Stabilized_Annual_ExpensePerUnitI = -750
Stabilized_Annual_GrowthRateI = 1.02
Stabilized_Annual_ExpensePerUnitJ = -782.78
Stabilized_Annual_GrowthRateJ = 1.02
Stabilized_Annual_ExpensePerUnitK = -52.02
Stabilized_Annual_GrowthRateK = 1.02
Stabilized_Annual_ExpensePerUnitL = -2218.65
Stabilized_Annual_GrowthRateL = 1.05
Stabilized_Annual_ExpensePerUnitM = -173.25
Stabilized_Annual_GrowthRateM = 1.05

# The lease up and stabilized revenue for units, parking and storage
LeaseUpRental_Monthly_IncomePerUnitAve = 2.45 * 627  # $2.45 average per square foot and 627 square foot average
StabilizedRental_Monthly_IncomePerUnitAve = 2.60 * 627  # $2.60 average per square foot and 627 square foot average

LeaseUpParking_Monthly_IncomePerStall = 125
StabilizedParking_Monthly_IncomePerStall = 150
Stalls = 173

LeaseUpStorage_Monthly_IncomePerLocker = 50
StabilizedStorage_Monthly_IncomePerLocker = 60
Lockers = 74

#  Lease up rent is the rent average per unit multiplied by the number of units multiplied by 1 minus the vacancy rate
#  times 12 to make it annual. We do this for the units, parking and storage
LeaseUpRentAnnual = ((LeaseUpRental_Monthly_IncomePerUnitAve * Units * (1 - LeaseUpVacancyRate)) + (
        LeaseUpParking_Monthly_IncomePerStall * Stalls * (1 - LeaseUpVacancyRate)) + (
                             LeaseUpStorage_Monthly_IncomePerLocker * Lockers * (1 - LeaseUpVacancyRate))) * 12

# Calculate the base annual revenue for the stabilized period (no growth yet) for each of the revenue streams
StabilizedRentAnnual_Base_Units = (StabilizedRental_Monthly_IncomePerUnitAve * Units) * 12
StabilizedRentAnnual_Base_Parking = (StabilizedParking_Monthly_IncomePerStall * Stalls) * 12
StabilizedRentAnnual_Base_Storage = (StabilizedStorage_Monthly_IncomePerLocker * Lockers) * 12

# Define a function that calculates the annual expense given the year. Takes into account all of the expenses and their
# growth rates. Raises the growth rate to the power of 'years past stabilized commencement'
def StabilizedExpenseAnnualFunction(yearPastStabilizedCommencement):
    expenseA = Stabilized_Annual_ExpensePerUnitA * Units * (Stabilized_Annual_GrowthRateA ** yearPastStabilizedCommencement)
    expenseB = Stabilized_Annual_ExpensePerUnitB * Units * (
                Stabilized_Annual_GrowthRateB ** yearPastStabilizedCommencement)
    expenseC = Stabilized_Annual_ExpensePerUnitC * Units * (
                Stabilized_Annual_GrowthRateC ** yearPastStabilizedCommencement)
    expenseD = Stabilized_Annual_ExpensePerUnitD * Units * (
                Stabilized_Annual_GrowthRateD ** yearPastStabilizedCommencement)
    expenseE = Stabilized_Annual_ExpensePerUnitE * Units * (
                Stabilized_Annual_GrowthRateE ** yearPastStabilizedCommencement)
    expenseF = Stabilized_Annual_ExpensePerUnitF * Units * (
                Stabilized_Annual_GrowthRateF ** yearPastStabilizedCommencement)
    expenseG = Stabilized_Annual_ExpensePerUnitG * Units * (
                Stabilized_Annual_GrowthRateG ** yearPastStabilizedCommencement)
    expenseH = Stabilized_Annual_ExpensePerUnitH * Units * (
                Stabilized_Annual_GrowthRateH ** yearPastStabilizedCommencement)
    expenseI = Stabilized_Annual_ExpensePerUnitI * Units * (
                Stabilized_Annual_GrowthRateI ** yearPastStabilizedCommencement)
    expenseJ = Stabilized_Annual_ExpensePerUnitJ * Units * (
                Stabilized_Annual_GrowthRateJ ** yearPastStabilizedCommencement)
    expenseK = Stabilized_Annual_ExpensePerUnitK * Units * (
                Stabilized_Annual_GrowthRateK ** yearPastStabilizedCommencement)
    expenseL = Stabilized_Annual_ExpensePerUnitL * Units * (
                Stabilized_Annual_GrowthRateL ** yearPastStabilizedCommencement)
    expenseM = Stabilized_Annual_ExpensePerUnitM * Units * (
                Stabilized_Annual_GrowthRateM ** yearPastStabilizedCommencement)
    expense = sum([expenseA, expenseB, expenseC, expenseD, expenseE, expenseF, expenseG, expenseH, expenseI, expenseJ,
                   expenseK, expenseL, expenseM])
    return expense


# Define a function that calculates the annual revenue given the year past commencement of stabilized period
# This takes into account the vacancy rates by multiplying by 1-the vacancy rate
def StabilizedRentAnnualFunction(
        yearPastStabilizedCommencement):
    rent = StabilizedRentAnnual_Base_Units * RentGrowthRate ** yearPastStabilizedCommencement + \
           StabilizedRentAnnual_Base_Parking * ParkingGrowthRate ** yearPastStabilizedCommencement + \
           StabilizedRentAnnual_Base_Storage * StorageGrowthRate ** yearPastStabilizedCommencement
    return rent*(1 - StabilizedVacancyRate)


#######################################################################################################################
# Create the cash flow schedule
# For each month in the site timeline, add up the revenue and expenses to get the income
# Start with the initial costs
CashFlowTimeline2a = [CostSchedule['LandAquisitionCost'] + CostSchedule['SoftCosts'] + CostSchedule['FinancingFees']]
CashFlowTimeline2b = [CostSchedule['LandAquisitionCost'] + CostSchedule['SoftCosts'] + CostSchedule['FinancingFees']]

# Add the construction period (spread evenly across the construction length)
for i in range(ConstructionLength2a):
    CashFlowTimeline2a.append(CostSchedule['HardCosts'] / ConstructionLength2a)

# Repeat for timeline b
for i in range(ConstructionLength2b):
    CashFlowTimeline2b.append(CostSchedule['HardCosts'] / ConstructionLength2b)

# Add the lease up period
for i in range(LeaseUpLength2a):
    CashFlowTimeline2a.append(LeaseUpExpenseAnnual/12 + LeaseUpRentAnnual/12)  # Divide by 12 to get monthly revenue

# Repeat for timeline b
for i in range(LeaseUpLength2b):
    CashFlowTimeline2b.append(LeaseUpExpenseAnnual/12 + LeaseUpRentAnnual/12)  # Divide by 12 to get monthly revenue

# Add the stabilized period
month = 1  # A counter to tell when we have reached one year
year = 0  # A tracker for the year we are in
for i in range(StabilizedLength2a):
    # If we have reached a new year, increment the year counter. Otherwise add one more month to its counter
    if month == 13:
        month = 1
        year = year + 1
    # Divide by 12 to get monthly revenue
    CashFlowTimeline2a.append(StabilizedExpenseAnnualFunction(year)/12 + StabilizedRentAnnualFunction(year)/12)
    month = month + 1

# Repeat for timeline b
month = 1  # A counter to tell when we have reached one year
year = 0  # A tracker for the year we are in
for i in range(StabilizedLength2b):
    # If we have reached a new year, increment the year counter. Otherwise add one more month to its counter
    if month == 13:
        month = 1
        year = year + 1
    # Divide by 12 to get monthly revenue
    CashFlowTimeline2b.append(StabilizedExpenseAnnualFunction(year)/12 + StabilizedRentAnnualFunction(year)/12)
    month = month + 1

# Add the sale proceeds (does the sale happen at the start of the last month? Do we get pad rent the last month?)
annualNOI2a = CashFlowTimeline2a[-1]*12  # Annual NOI is the previous month's income times 12
annualNOI2b = CashFlowTimeline2b[-1]*12  # Annual NOI is the previous month's income times 12

saleAmount2a = annualNOI2a/capRate  # The sale amount is the NOI divided by the cap rate
saleAmount2b = annualNOI2b/capRate  # The sale amount is the NOI divided by the cap rate

CashFlowTimeline2a[-1] = CashFlowTimeline2a[-1] + saleAmount2a
CashFlowTimeline2b[-1] = CashFlowTimeline2b[-1] + saleAmount2b

CashFlowTimeline2a = pd.Series(CashFlowTimeline2a)
CashFlowTimeline2b = pd.Series(CashFlowTimeline2b)
Months2a = np.arange(CashFlowTimeline2a.__len__())+1
Months2b = np.arange(CashFlowTimeline2b.__len__())+1
CashFlowSchedule2a = pd.DataFrame(dict(CashFlow=CashFlowTimeline2a, Month=Months2a))
CashFlowSchedule2b = pd.DataFrame(dict(CashFlow=CashFlowTimeline2b, Month=Months2b))


