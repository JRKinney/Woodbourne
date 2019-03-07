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
    expenseA = Stabilized_Annual_ExpensePerUnitA * Units * (
                Stabilized_Annual_GrowthRateA ** yearPastStabilizedCommencement)
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
    return rent * (1 - StabilizedVacancyRate)


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
    CashFlowTimeline2a.append(LeaseUpExpenseAnnual / 12 + LeaseUpRentAnnual / 12)  # Divide by 12 to get monthly revenue

# Repeat for timeline b
for i in range(LeaseUpLength2b):
    CashFlowTimeline2b.append(LeaseUpExpenseAnnual / 12 + LeaseUpRentAnnual / 12)  # Divide by 12 to get monthly revenue

# Add the stabilized period
month = 1  # A counter to tell when we have reached one year
year = 0  # A tracker for the year we are in
for i in range(StabilizedLength2a):
    # If we have reached a new year, increment the year counter. Otherwise add one more month to its counter
    if month == 13:
        month = 1
        year = year + 1
    # Divide by 12 to get monthly revenue
    CashFlowTimeline2a.append(StabilizedExpenseAnnualFunction(year) / 12 + StabilizedRentAnnualFunction(year) / 12)
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
    CashFlowTimeline2b.append(StabilizedExpenseAnnualFunction(year) / 12 + StabilizedRentAnnualFunction(year) / 12)
    month = month + 1

# Add the sale proceeds (does the sale happen at the start of the last month? Do we get pad rent the last month?)
annualNOI2a = CashFlowTimeline2a[-1] * 12  # Annual NOI is the previous month's income times 12
annualNOI2b = CashFlowTimeline2b[-1] * 12  # Annual NOI is the previous month's income times 12

saleAmount2a = annualNOI2a / capRate  # The sale amount is the NOI divided by the cap rate
saleAmount2b = annualNOI2b / capRate  # The sale amount is the NOI divided by the cap rate

CashFlowTimeline2a[-1] = CashFlowTimeline2a[-1] + saleAmount2a
CashFlowTimeline2b[-1] = CashFlowTimeline2b[-1] + saleAmount2b

CashFlowTimeline2a = pd.Series(CashFlowTimeline2a)
CashFlowTimeline2b = pd.Series(CashFlowTimeline2b)
Months2a = np.arange(CashFlowTimeline2a.__len__()) + 1
Months2b = np.arange(CashFlowTimeline2b.__len__()) + 1
CashFlowSchedule2a = pd.DataFrame(dict(CashFlow=CashFlowTimeline2a, Month=Months2a))
CashFlowSchedule2b = pd.DataFrame(dict(CashFlow=CashFlowTimeline2b, Month=Months2b))

########################################################################################################################
# Task 2
# Calculate the budget (negative the costs)
Budget = sum([CostSchedule['LandAquisitionCost'], CostSchedule['SoftCosts'], CostSchedule['HardCosts'],
              CostSchedule['FinancingFees'], CostSchedule['InterestReserve']]) * (-1)
# Construction Loan
# Interest Only Loan, maturity date (principal repayment) occurs upon stabilization of the property. Interest costs
# funded through Interest Reserve
Construction_Attachment = 0
Construction_Detachment = 0.75
Construction_InterestRate = .045
Construction_Amount = Budget * (Construction_Detachment - Construction_Attachment)

# Mezzanine Loan
# Interest Only Loan, maturity date (principal repayment) occurs upon sale of the property. Interest costs accrue until
# the property is fully stabilized, at which point all excess proceeds are used to fund any outstanding interest and
# principle. All outstanding interest and principle are payable in full at the maturity date
Mezzanine_Attachment = .75
Mezzanine_Detachment = .875
Mezzanine_InterestRate = 0.12
Mezzanine_Amount = Budget * (Mezzanine_Detachment - Mezzanine_Attachment)

# Equity
# Receives all excess cash flow and must fund all shortfalls
Equity_Attachment = .875
Equity_Detachment = 1
Equity_Amount = Budget * (Equity_Detachment - Equity_Attachment)

maxMortgageLTV = .75
minMortgageDSCR = 1.2
mortgageInterestRate = 0.03

# Notes to myself
# Payments
# Up to Stabilized:
#   Construction gets annual interest = Budget*(Construction_Detachment - Construction_Attachment) *
#       Construction_InterestRate
#   Mezzanine accrues interest = Budget * (Mezzanine_Detachment - Mezzanine_Attachment) * Mezzanine_InterestRate
#   Equity gets all excess and funds all shortfalls

ProjectCash2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
ProjectCash2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
ConstructionPaid2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
ConstructionPaid2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
ConstructionReceived2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
ConstructionReceived2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
MezzanineCash2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
MezzanineCash2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
EquityCash2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
EquityCash2b = np.zeros(CashFlowSchedule2b['Month'].__len__())

# Track whether the entirety of the capital source has been used
EquityUsed2a = True
MezzUsed2a = False
ConstructionUsed2a = False
EquityUsed2b = True
MezzUsed2b = False
ConstructionUsed2b = False

# Make a cashflow timeline for Project cash, Construction, Mezzanine and Equity
# Starting cash comes from equity. Mezz debt is gathered as needed until it is maxed out. Then the construction loan is
# pulled from
ProjectCash2a[0] = Equity_Amount + CashFlowSchedule2a['CashFlow'][0]
ProjectCash2b[0] = Equity_Amount + CashFlowSchedule2a['CashFlow'][0]

# Reflect the negative cash flow for Equity investors
EquityCash2a[0] = (-1) * Equity_Amount
EquityCash2b[0] = (-1) * Equity_Amount

# If Equity has not paid for the amount needed, pull from mezz debt. Pull at max the mezzanine amount
if ProjectCash2a[0] < 0:
    MezzanineCash2a[0] = max(ProjectCash2a[0], Mezzanine_Amount*(-1))
    ProjectCash2a[0] = ProjectCash2a[0] - MezzanineCash2a[0]
    if MezzanineCash2a[0] == Mezzanine_Amount * (-1):
        MezzUsed2a = True

# If the amount is still not covered, pull from the construction loan
if ProjectCash2a[0] < 0:
    ConstructionPaid2a[0] = max(ProjectCash2a[0], Construction_Amount*(-1))
    ProjectCash2a[0] = ProjectCash2a[0] - ConstructionPaid2a[0]
    if ConstructionPaid2a[0] == Construction_Amount * (-1):
        ConstructionUsed2a = True

# Repeat for 2b
if ProjectCash2b[0] < 0:
    MezzanineCash2b[0] = max(ProjectCash2b[0], Mezzanine_Amount*(-1))
    ProjectCash2b[0] = ProjectCash2b[0] - MezzanineCash2b[0]
    if MezzanineCash2b[0] == Mezzanine_Amount * (-1):
        MezzUsed2b = True


# If the amount is still not covered, pull from the construction loan
if ProjectCash2b[0] < 0:
    ConstructionPaid2b[0] = max(ProjectCash2b[0], Construction_Amount*(-1))
    ProjectCash2b[0] = ProjectCash2b[0] - ConstructionPaid2b[0]
    if ConstructionPaid2b[0] == Construction_Amount * (-1):
        ConstructionUsed2b = True


# There is initially no mezz debt interest accrued
Mezzanine_InterestedAccrued2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
Mezzanine_InterestedAccrued2b = np.zeros(CashFlowSchedule2b['Month'].__len__())


# For the period up to the stabilized period, use cash to build the project. Draw from loans as needed, taking most
# junior loans first. Accrue mezz debt interest and pay construction loan interest
for i in range(1, LeaseUpLength2a + ConstructionLength2a + 1):
    # Record the amount of interest accrued by the mezzanine loan but don't pay it yet
    # This is calculated by adding the accrued interest to this point plus this months interest (on the loan and
    # accrued interest)
    Mezzanine_InterestedAccrued2a[i] = Mezzanine_InterestedAccrued2a[i-1] + (Mezzanine_InterestedAccrued2a[i-1] - MezzanineCash2a.sum()) * Mezzanine_InterestRate / 12
    # Give the interest to the construction lender
    ConstructionReceived2a[i] = ConstructionPaid2a.sum() * (-1) * Construction_InterestRate / 12
    # Augment the project cash by the amount spent/gained from the site and interest
    ProjectCash2a[i] = ProjectCash2a[i - 1] + CashFlowSchedule2a['CashFlow'][i] - ConstructionReceived2a[i]
    # Pull cash as necessary from mezz debt
    if ProjectCash2a[i] < 0 and not MezzUsed2a:
        # Take at max the Mezzanine amount minus the amount used already (negative number so add)
        MezzanineCash2a[i] = max(ProjectCash2a[i], (Mezzanine_Amount+MezzanineCash2a.sum())*(-1))
        # Let the project cash reflect the amount taken from Mezz debt
        ProjectCash2a[i] = ProjectCash2a[i] - MezzanineCash2a[i]
        # If all the mezz debt was used, show that
        if MezzanineCash2a[i].sum() == Mezzanine_Amount*(-1):
            MezzUsed2a = True

    # If mezz debt has been all used up, use construction debt
    if ProjectCash2a[i] < 0 and not ConstructionUsed2a:
        # Take at max the Construction amount minus the amount used already (negative number so add)
        ConstructionPaid2a[i] = max(ProjectCash2a[i], (Construction_Amount + ConstructionPaid2a.sum())*(-1))
        # Let the project cash reflect the amount taken from Construction debt
        ProjectCash2a[i] = ProjectCash2a[i] - ConstructionPaid2a[i]
        # If all the construction debt was used, show that
        if ConstructionPaid2a[i].sum() == Construction_Amount * (-1):
            ConstructionUsed2a = True

    # If there is still a need for money, print out an error
    if ProjectCash2a[i] < 0 and ConstructionUsed2a and MezzUsed2a:
        print('All Cash Used up. ERROR')


# Once this period has completed, the property is stabilized and the construction loan principle will be paid back
# Excess cash will be used to fund the interest accrued by the mezzanine loan. Excess cash goes to the equity holders

# In 2a, the sale happens at this point too, so the mezzanine principle gets paid back and all extra cash goes to the
# equity holder
i = LeaseUpLength2a + ConstructionLength2a + 1
# The Mezz debt accrues one more month and construction gets 1 more month of interest
Mezzanine_InterestedAccrued2a[i] = Mezzanine_InterestedAccrued2a[i-1] + (Mezzanine_InterestedAccrued2a[i-1] - MezzanineCash2a.sum()) * Mezzanine_InterestRate / 12
ConstructionReceived2a[i] = ConstructionPaid2a.sum() * (-1) * Construction_InterestRate / 12
# Then the project cash receives the sale and final month's income. The construction interest for the last month and the
#  principle are paid off. The mezz debt accrued interest and principle are paid off.
ProjectCash2a[i] = ProjectCash2a[i-1] + CashFlowSchedule2a['CashFlow'][i] - ConstructionReceived2a[i] + ConstructionPaid2a.sum() - (Mezzanine_InterestedAccrued2a[i] - MezzanineCash2a.sum())
# If there was enough cash to pay back construction and mezz debt, show that
if ProjectCash2a[i] > 0:
    ConstructionReceived2a[i] = ConstructionPaid2a.sum() * (-1) * Construction_InterestRate / 12 - ConstructionPaid2a.sum()
    MezzanineCash2a[i] = (-1)*MezzanineCash2a.sum() + Mezzanine_InterestedAccrued2a[i]

# Equity takes the final cash
EquityCash2a[i] = ProjectCash2a[i]
ProjectCash2a[i] = ProjectCash2a[i] - EquityCash2a[i]

# Calculate one cash flow for Construction lender
ConstructionCash2a = ConstructionPaid2a + ConstructionReceived2a

# Calculate MOICs
ConstructionMOIC2a = ConstructionReceived2a.sum()/ConstructionPaid2a.sum()*(-1)
MezzanineMOIC2a = MezzanineCash2a[i]/MezzanineCash2a[:-1].sum()*(-1)
EquityMOIC2a = EquityCash2a[i]/EquityCash2a[:-1].sum()*(-1)

# Calculate annual IRR. Cash flow is monthly, so annualize it here
ConstructionIRR2a = (1+np.irr(ConstructionCash2a))**12 - 1
MezzanineIRR2a = (1+np.irr(MezzanineCash2a))**12 - 1
EquityIRR2a = (1+np.irr(EquityCash2a))**12 - 1

# Total Profit calculations
ConstructionTotalProfit2a = ConstructionCash2a.sum()
MezzanineTotalProfit2a = MezzanineCash2a.sum()
EquityTotalProfit2a = EquityCash2a.sum()


#######################################################################################################################
# 2b
# For the period up to the stabilized period, use cash to build the project. Draw from loans as needed, taking most
# junior loans first. Accrue mezz debt interest and pay construction loan interest
for i in range(1, LeaseUpLength2b + ConstructionLength2b + 1):
    # Record the amount of interest accrued by the mezzanine loan but don't pay it yet
    # This is calculated by adding the accrued interest to this point plus this months interest (on the loan and
    # accrued interest)
    Mezzanine_InterestedAccrued2b[i] = Mezzanine_InterestedAccrued2b[i-1] + (Mezzanine_InterestedAccrued2b[i-1] - MezzanineCash2b.sum()) * Mezzanine_InterestRate / 12
    # Give the interest to the construction lender
    ConstructionReceived2b[i] = ConstructionPaid2b.sum() * (-1) * Construction_InterestRate / 12
    # Augment the project cash by the amount spent/gained from the site and interest
    ProjectCash2b[i] = ProjectCash2b[i - 1] + CashFlowSchedule2b['CashFlow'][i] - ConstructionReceived2b[i]
    # Pull cash as necessary from mezz debt
    if ProjectCash2b[i] < 0 and not MezzUsed2b:
        # Take at max the Mezzanine amount minus the amount used already (negative number so add)
        MezzanineCash2b[i] = max(ProjectCash2b[i], (Mezzanine_Amount+MezzanineCash2b.sum())*(-1))
        # Let the project cash reflect the amount taken from Mezz debt
        ProjectCash2b[i] = ProjectCash2b[i] - MezzanineCash2b[i]
        # If all the mezz debt was used, show that
        if MezzanineCash2b[i].sum() == Mezzanine_Amount*(-1):
            MezzUsed2b = True

    # If mezz debt has been all used up, use construction debt
    if ProjectCash2b[i] < 0 and not ConstructionUsed2b:
        # Take at max the Construction amount minus the amount used already (negative number so add)
        ConstructionPaid2b[i] = max(ProjectCash2b[i], (Construction_Amount + ConstructionPaid2b.sum())*(-1))
        # Let the project cash reflect the amount taken from Construction debt
        ProjectCash2b[i] = ProjectCash2b[i] - ConstructionPaid2b[i]
        # If all the construction debt was used, show that
        if ConstructionPaid2b[i].sum() == Construction_Amount * (-1):
            ConstructionUsed2b = True

    # If there is still a need for money, print out an error
    if ProjectCash2b[i] < 0 and ConstructionUsed2b and MezzUsed2b:
        print('All Cash Used up. ERROR')


# Once this period has completed, the property is stabilized and the construction loan principle will be paid back
# Excess cash will be used to fund the interest accrued by the mezzanine loan. Excess cash goes to the equity holders

# In 2b, this is when the refinancing happens so we need to calculate the right mortgage and pay off the construction
i = LeaseUpLength2b + ConstructionLength2b + 1
# The Mezz debt accrues one more month and construction gets 1 more month of interest
Mezzanine_InterestedAccrued2b[i] = Mezzanine_InterestedAccrued2b[i-1] + (Mezzanine_InterestedAccrued2b[i-1] - MezzanineCash2b.sum()) * Mezzanine_InterestRate / 12
ConstructionReceived2b[i] = ConstructionPaid2b.sum() * (-1) * Construction_InterestRate / 12
# Then the project cash receives the sale and the month's income. The construction interest for the last month is paid
ProjectCash2b[i] = ProjectCash2b[i-1] + CashFlowSchedule2b['CashFlow'][i] - ConstructionReceived2b[i]
# Max Mortage is limited by max LTV and min DSCR
mortgageMax = maxMortgageLTV * CashFlowSchedule2b['CashFlow'][i]*12/capRate
# The neccesary mortgage is the amount needed to pay of the construction principle
mortgageNeccesary = (-1)*ConstructionPaid2b.sum() - ProjectCash2b[i]
# Confirm that this is allowable under the mortgage conditions
if mortgageMax > mortgageNeccesary:
    mortgageAmount = mortgageNeccesary
else:
    print('Neccesary Mortgage Not Allowable')

# Confirm the DSCR is allowable
DSCR = CashFlowSchedule2b['CashFlow'][i]/(mortgageAmount*mortageInterestRate/12)
if DSCR < minMortgageDSCR:
    print('DSCR = ' + str(DSCR) + '. The month is ' + str(i) + ' and we are in default.')

# Take out mortgage and put it into the project cash
mortgagePrinciple = mortgageAmount
ProjectCash2b[i] = ProjectCash2b[i] + mortgagePrinciple

# Pay off construction loan with the project cash
ConstructionReceived2b[i] = (-1)*ConstructionPaid2b.sum()
ProjectCash2b[i] = ProjectCash2b[i]-ConstructionReceived2b[i]







fv = 0
pv = 200000
rate = 0.075 / 12
nper = 15 * 12

for per in range(nper):
  principal = -np.ppmt(rate, per, nper, pv)
  interest = -np.ipmt(rate, per, nper, pv)
  print(principal, interest, principal + interest)




# Loop, paying off mortgage and mezzanine debt during the stabilized period
for i in range(StabilizedLength2b):
    # Pay mortgage interest semi annually at .5*annual interest rate first because we don't want to default
    # If not semi annual, then save up money for the semi annual payment =(mortgagePrinciple*mortgageInterestRate/6)
    # Accrue mezzanine interest
    # Pay mezzanine accrued interest second becasue mezz debt is 12% money
    # Pay mezzanine principle
    # Pay mortgage principle last because it is 4% money





# Equity takes the final cash
EquityCash2b[i] = ProjectCash2b[i]
ProjectCash2b[i] = ProjectCash2b[i] - EquityCash2b[i]

# Calculate one cash flow for Construction lender
ConstructionCash2b = ConstructionPaid2b + ConstructionReceived2b

# Calculate MOICs
ConstructionMOIC2b = ConstructionReceived2b.sum()/ConstructionPaid2b.sum()*(-1)
MezzanineMOIC2b = MezzanineCash2b[i]/MezzanineCash2b[:-1].sum()*(-1)
EquityMOIC2b = EquityCash2b[i]/EquityCash2b[:-1].sum()*(-1)

# Calculate annual IRR. Cash flow is monthly, so annualize it here
ConstructionIRR2b = (1+np.irr(ConstructionCash2b))**12 - 1
MezzanineIRR2b = (1+np.irr(MezzanineCash2b))**12 - 1
EquityIRR2b = (1+np.irr(EquityCash2b))**12 - 1

# Total Profit calculations
ConstructionTotalProfit2b = ConstructionCash2b.sum()
MezzanineTotalProfit2b = MezzanineCash2b.sum()
EquityTotalProfit2b = EquityCash2b.sum()
