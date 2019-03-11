import numpy as np
import pandas as pd
import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly
import plotly.plotly as py
import plotly.tools as tls
import cufflinks as cf
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='JamesRKinney', api_key='tkTlLVkZZRmJW4cquWl0')

# Define a function that does the calculations of the cash flow and returns
#######################################################################################################################
def ModelRun(capRate = .04, Units = 260, LeaseUpVacancyRate = .33, StabilizedVacancyRate = .02, RentGrowthRate = 1.025,
             ParkingGrowthRate = 1.025, StorageGrowthRate = 1.025, LandAquisitionCost=-10000000, SoftCosts=-11000000,
             HardCosts=-53000000, FinancingFees=-1000000,InterestReserve=-8000000, ConstructionLength2a = 27,
             LeaseUpLength2a = 12 , StabilizedLength2a = 1,ConstructionLength2b = 27, LeaseUpLength2b = 12,
             StabilizedLength2b = 61, LeaseUp_Annual_ExpensePerUnit = -4838.96,
             Stabilized_Annual_ExpensePerUnit_Scale = 1, StabilizedRental_Monthly_IncomePerUnit = 2.60,
             Construction_Attachment = 0, Construction_Detachment = 0.75, Construction_InterestRate = .045,
             Mezzanine_Attachment = .75, Mezzanine_Detachment = .875, Mezzanine_InterestRate = 0.12,
             Equity_Attachment = .875, Equity_Detachment = 1, maxMortgageLTV = .75, minMortgageDSCR = 1.2,
             mortgageInterestRate = 0.03, amortizationPeriod = 30):
    CostSchedule = dict(LandAquisitionCost=LandAquisitionCost, SoftCosts=SoftCosts, HardCosts=HardCosts,
                        FinancingFees=FinancingFees, InterestReserve=InterestReserve)
    # Calculate lease up and stabilized expenses
    LeaseUpExpenseAnnual = LeaseUp_Annual_ExpensePerUnit * Units

    # The stabilized expenses and their growth rates
    Stabilized_Annual_ExpensePerUnitA = -100 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateA = 1.02
    Stabilized_Annual_ExpensePerUnitB = -30 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateB = 1.02
    Stabilized_Annual_ExpensePerUnitC = -30 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateC = 1.02
    Stabilized_Annual_ExpensePerUnitD = -76 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateD = 1.02
    Stabilized_Annual_ExpensePerUnitE = -309 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateE = 1.03
    Stabilized_Annual_ExpensePerUnitF = -354.96 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateF = 1.02
    Stabilized_Annual_ExpensePerUnitG = -623.53 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateG = 1.02
    Stabilized_Annual_ExpensePerUnitH = -25.5 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateH = 1.02
    Stabilized_Annual_ExpensePerUnitI = -750 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateI = 1.02
    Stabilized_Annual_ExpensePerUnitJ = -782.78 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateJ = 1.02
    Stabilized_Annual_ExpensePerUnitK = -52.02 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateK = 1.02
    Stabilized_Annual_ExpensePerUnitL = -2218.65 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateL = 1.05
    Stabilized_Annual_ExpensePerUnitM = -173.25 * Stabilized_Annual_ExpensePerUnit_Scale
    Stabilized_Annual_GrowthRateM = 1.05

    # The lease up and stabilized revenue for units, parking and storage
    LeaseUpRental_Monthly_IncomePerUnitAve = 2.45 * 627  # $2.45 average per square foot and 627 square foot average
    StabilizedRental_Monthly_IncomePerUnitAve = StabilizedRental_Monthly_IncomePerUnit * 627  # $2.60 average per square
    # foot and 627 square foot average
    print(StabilizedRental_Monthly_IncomePerUnit)

    LeaseUpParking_Monthly_IncomePerStall = 125
    StabilizedParking_Monthly_IncomePerStall = 150
    Stalls = 173

    LeaseUpStorage_Monthly_IncomePerLocker = 50
    StabilizedStorage_Monthly_IncomePerLocker = 60
    Lockers = 74

    #  Lease up rent is the rent average per unit multiplied by the number of units multiplied by 1 minus the vacancy
    #  rate times 12 to make it annual. We do this for the units, parking and storage
    LeaseUpRentAnnual = ((LeaseUpRental_Monthly_IncomePerUnitAve * Units * (1 - LeaseUpVacancyRate)) + (
            LeaseUpParking_Monthly_IncomePerStall * Stalls * (1 - LeaseUpVacancyRate)) + (
                                 LeaseUpStorage_Monthly_IncomePerLocker * Lockers * (1 - LeaseUpVacancyRate))) * 12

    # Calculate the base annual revenue for the stabilized period (no growth yet) for each of the revenue streams
    StabilizedRentAnnual_Base_Units = (StabilizedRental_Monthly_IncomePerUnitAve * Units) * 12
    StabilizedRentAnnual_Base_Parking = (StabilizedParking_Monthly_IncomePerStall * Stalls) * 12
    StabilizedRentAnnual_Base_Storage = (StabilizedStorage_Monthly_IncomePerLocker * Lockers) * 12

    # Define a function that calculates the annual expense given the year. Takes into account all of the expenses and
    # their growth rates. Raises the growth rate to the power of 'years past stabilized commencement'
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
        expense = sum(
            [expenseA, expenseB, expenseC, expenseD, expenseE, expenseF, expenseG, expenseH, expenseI, expenseJ,
             expenseK, expenseL, expenseM])
        return expense

    # Define a function that calculates the annual revenue given the year past commencement of stabilized period
    # This takes into account the vacancy rates by multiplying by 1-the vacancy rate
    def StabilizedRentAnnualFunction(
            yearPastStabilizedCommencement):
        rent = StabilizedRentAnnual_Base_Units * RentGrowthRate ** yearPastStabilizedCommencement +                StabilizedRentAnnual_Base_Parking * ParkingGrowthRate ** yearPastStabilizedCommencement +                StabilizedRentAnnual_Base_Storage * StorageGrowthRate ** yearPastStabilizedCommencement
        return rent * (1 - StabilizedVacancyRate)

    ####################################################################################################################
    # Create the cash flow schedule
    # For each month in the site timeline, add up the revenue and expenses to get the income
    # Start with the initial costs
    CashFlowTimeline2a = [
        CostSchedule['LandAquisitionCost'] + CostSchedule['SoftCosts'] + CostSchedule['FinancingFees']]
    CashFlowTimeline2b = [
        CostSchedule['LandAquisitionCost'] + CostSchedule['SoftCosts'] + CostSchedule['FinancingFees']]

    # Add the construction period (spread evenly across the construction length)
    for i in range(ConstructionLength2a):
        CashFlowTimeline2a.append(CostSchedule['HardCosts'] / ConstructionLength2a)

    # Repeat for timeline b
    for i in range(ConstructionLength2b):
        CashFlowTimeline2b.append(CostSchedule['HardCosts'] / ConstructionLength2b)

    # Add the lease up period
    for i in range(LeaseUpLength2a):
        CashFlowTimeline2a.append(
            LeaseUpExpenseAnnual / 12 + LeaseUpRentAnnual / 12)  # Divide by 12 to get monthly revenue

    # Repeat for timeline b
    for i in range(LeaseUpLength2b):
        CashFlowTimeline2b.append(
            LeaseUpExpenseAnnual / 12 + LeaseUpRentAnnual / 12)  # Divide by 12 to get monthly revenue

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

    ####################################################################################################################
    # Task 2
    # Calculate the budget (negative the costs)
    Budget = sum([CostSchedule['LandAquisitionCost'], CostSchedule['SoftCosts'], CostSchedule['HardCosts'],
                  CostSchedule['FinancingFees'], CostSchedule['InterestReserve']]) * (-1)
    # Construction Loan
    # Interest Only Loan, maturity date (principal repayment) occurs upon stabilization of the property. Interest costs
    # funded through Interest Reserve
    Construction_Amount = Budget * (Construction_Detachment - Construction_Attachment)

    # Mezzanine Loan
    # Interest Only Loan, maturity date (principal repayment) occurs upon sale of the property. Interest costs accrue
    # until the property is fully stabilized, at which point all excess proceeds are used to fund any outstanding
    # interest and principle. All outstanding interest and principle are payable in full at the maturity date
    Mezzanine_Amount = Budget * (Mezzanine_Detachment - Mezzanine_Attachment)

    # Equity
    # Receives all excess cash flow and must fund all shortfalls
    Equity_Amount = Budget * (Equity_Detachment - Equity_Attachment)

    # Set uo the cash flow schedules
    ProjectCash2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
    ProjectCash2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
    ConstructionPaid2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
    ConstructionPaid2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
    ConstructionReceived2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
    ConstructionReceived2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
    MezzanineCash2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
    MezzanineCash2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
    MezzanineInterestPaid2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
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
    # Starting cash comes from equity. Mezz debt is gathered as needed until it is maxed out. Then the construction loan
    # is pulled from
    ProjectCash2a[0] = Equity_Amount + CashFlowSchedule2a['CashFlow'][0]
    ProjectCash2b[0] = Equity_Amount + CashFlowSchedule2a['CashFlow'][0]

    # Reflect the negative cash flow for Equity investors
    EquityCash2a[0] = (-1) * Equity_Amount
    EquityCash2b[0] = (-1) * Equity_Amount

    # If Equity has not paid for the amount needed, pull from mezz debt. Pull at max the mezzanine amount
    if ProjectCash2a[0] < 0:
        MezzanineCash2a[0] = max(ProjectCash2a[0], Mezzanine_Amount * (-1))
        ProjectCash2a[0] = ProjectCash2a[0] - MezzanineCash2a[0]
        if MezzanineCash2a[0] == Mezzanine_Amount * (-1):
            MezzUsed2a = True

    # If the amount is still not covered, pull from the construction loan
    if ProjectCash2a[0] < 0:
        ConstructionPaid2a[0] = max(ProjectCash2a[0], Construction_Amount * (-1))
        ProjectCash2a[0] = ProjectCash2a[0] - ConstructionPaid2a[0]
        if ConstructionPaid2a[0] == Construction_Amount * (-1):
            ConstructionUsed2a = True

    # Repeat for 2b
    if ProjectCash2b[0] < 0:
        MezzanineCash2b[0] = max(ProjectCash2b[0], Mezzanine_Amount * (-1))
        ProjectCash2b[0] = ProjectCash2b[0] - MezzanineCash2b[0]
        if MezzanineCash2b[0] == Mezzanine_Amount * (-1):
            MezzUsed2b = True

    # If the amount is still not covered, pull from the construction loan
    if ProjectCash2b[0] < 0:
        ConstructionPaid2b[0] = max(ProjectCash2b[0], Construction_Amount * (-1))
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
        Mezzanine_InterestedAccrued2a[i] = Mezzanine_InterestedAccrued2a[i - 1] + (
                    Mezzanine_InterestedAccrued2a[i - 1] - MezzanineCash2a.sum()) * Mezzanine_InterestRate / 12
        # Give the interest to the construction lender
        ConstructionReceived2a[i] = ConstructionPaid2a.sum() * (-1) * Construction_InterestRate / 12
        # Augment the project cash by the amount spent/gained from the site and interest
        ProjectCash2a[i] = ProjectCash2a[i - 1] + CashFlowSchedule2a['CashFlow'][i] - ConstructionReceived2a[i]
        # Pull cash as necessary from mezz debt
        if ProjectCash2a[i] < 0 and not MezzUsed2a:
            # Take at max the Mezzanine amount minus the amount used already (negative number so add)
            MezzanineCash2a[i] = max(ProjectCash2a[i], (Mezzanine_Amount + MezzanineCash2a.sum()) * (-1))
            # Let the project cash reflect the amount taken from Mezz debt
            ProjectCash2a[i] = ProjectCash2a[i] - MezzanineCash2a[i]
            # If all the mezz debt was used, show that
            if MezzanineCash2a[i].sum() == Mezzanine_Amount * (-1):
                MezzUsed2a = True

        # If mezz debt has been all used up, use construction debt
        if ProjectCash2a[i] < 0 and not ConstructionUsed2a:
            # Take at max the Construction amount minus the amount used already (negative number so add)
            ConstructionPaid2a[i] = max(ProjectCash2a[i], (Construction_Amount + ConstructionPaid2a.sum()) * (-1))
            # Let the project cash reflect the amount taken from Construction debt
            ProjectCash2a[i] = ProjectCash2a[i] - ConstructionPaid2a[i]
            # If all the construction debt was used, show that
            if ConstructionPaid2a[i].sum() == Construction_Amount * (-1):
                ConstructionUsed2a = True

        # If there is still a need for money, print out an error
        if ProjectCash2a[i] < 0 and ConstructionUsed2a and MezzUsed2a:
            print('All Cash Used up. ERROR')

    # Once this period has completed, the property is stabilized and the construction loan principle will be paid back
    # Excess cash will be used to fund the interest accrued by the mezzanine loan. Excess cash goes to the equity
    # holders

    # In 2a, the sale happens at this point too, so the mezzanine principle gets paid back and all extra cash goes to
    # the equity holder
    i = LeaseUpLength2a + ConstructionLength2a + 1
    # The Mezz debt accrues one more month and construction gets 1 more month of interest
    Mezzanine_InterestedAccrued2a[i] = Mezzanine_InterestedAccrued2a[i - 1] + (
                Mezzanine_InterestedAccrued2a[i - 1] - MezzanineCash2a.sum()) * Mezzanine_InterestRate / 12
    ConstructionReceived2a[i] = ConstructionPaid2a.sum() * (-1) * Construction_InterestRate / 12
    # Then the project cash receives the sale and final month's income. The construction interest for the last month and
    # the principle are paid off. The mezz debt accrued interest and principle are paid off.
    ProjectCash2a[i] = ProjectCash2a[i - 1] + CashFlowSchedule2a['CashFlow'][i] - ConstructionReceived2a[
        i] + ConstructionPaid2a.sum() - (Mezzanine_InterestedAccrued2a[i] - MezzanineCash2a.sum())
    # If there was enough cash to pay back construction and mezz debt, show that
    
    if ProjectCash2a[i] > 0:
        ConstructionReceived2a[i] = ConstructionPaid2a.sum() * (
            -1) * Construction_InterestRate / 12 - ConstructionPaid2a.sum()
        MezzanineCash2a[i] = (-1) * MezzanineCash2a.sum() + Mezzanine_InterestedAccrued2a[i]
    
    # Equity takes the final cash
    EquityCash2a[i] = ProjectCash2a[i]
    ProjectCash2a[i] = ProjectCash2a[i] - EquityCash2a[i]

    # Calculate one cash flow for Construction lender
    ConstructionCash2a = ConstructionPaid2a + ConstructionReceived2a
    
    ExampleInvestorCasha = MezzanineCash2a + .5*EquityCash2a
    
    # Calculate MOICs
    ConstructionMOIC2a = ConstructionReceived2a.sum() / ConstructionPaid2a.sum() * (-1)
    MezzanineMOIC2a = MezzanineCash2a[1:].sum() / MezzanineCash2a[0] * (-1)
    EquityMOIC2a = EquityCash2a[1:].sum() / EquityCash2a[0] * (-1)
    ExampleMOICa = ExampleInvestorCasha[1:].sum() / ExampleInvestorCasha[0]*(-1)

    # Calculate annual IRR. Cash flow is monthly, so annualize it here
    ConstructionIRR2a = (1 + np.irr(ConstructionCash2a)) ** 12 - 1
    MezzanineIRR2a = (1 + np.irr(MezzanineCash2a)) ** 12 - 1
    EquityIRR2a = (1 + np.irr(EquityCash2a)) ** 12 - 1
    ExampleIRRa = (1 + np.irr(ExampleInvestorCasha)) **12 - 1
    
    # Total Profit calculations
    ConstructionTotalProfit2a = ConstructionCash2a.sum()
    MezzanineTotalProfit2a = MezzanineCash2a.sum()
    EquityTotalProfit2a = EquityCash2a.sum()
    ExampleTotalProfita = ExampleInvestorCasha.sum()

    #######################################################################################################################
    # 2b
    # For the period up to the stabilized period, use cash to build the project. Draw from loans as needed, taking most
    # junior loans first. Accrue mezz debt interest and pay construction loan interest
    for i in range(1, LeaseUpLength2b + ConstructionLength2b + 1):
        # Record the amount of interest accrued by the mezzanine loan but don't pay it yet
        # This is calculated by adding the accrued interest to this point plus this months interest (on the loan and
        # accrued interest)
        Mezzanine_InterestedAccrued2b[i] = Mezzanine_InterestedAccrued2b[i - 1] + (
                    Mezzanine_InterestedAccrued2b[i - 1] - MezzanineCash2b.sum()) * Mezzanine_InterestRate / 12
        # Give the interest to the construction lender
        ConstructionReceived2b[i] = ConstructionPaid2b.sum() * (-1) * Construction_InterestRate / 12
        # Augment the project cash by the amount spent/gained from the site and interest
        ProjectCash2b[i] = ProjectCash2b[i - 1] + CashFlowSchedule2b['CashFlow'][i] - ConstructionReceived2b[i]
        # Pull cash as necessary from mezz debt
        if ProjectCash2b[i] < 0 and not MezzUsed2b:
            # Take at max the Mezzanine amount minus the amount used already (negative number so add)
            MezzanineCash2b[i] = max(ProjectCash2b[i], (Mezzanine_Amount + MezzanineCash2b.sum()) * (-1))
            # Let the project cash reflect the amount taken from Mezz debt
            ProjectCash2b[i] = ProjectCash2b[i] - MezzanineCash2b[i]
            # If all the mezz debt was used, show that
            if MezzanineCash2b[i].sum() == Mezzanine_Amount * (-1):
                MezzUsed2b = True

        # If mezz debt has been all used up, use construction debt
        if ProjectCash2b[i] < 0 and not ConstructionUsed2b:
            # Take at max the Construction amount minus the amount used already (negative number so add)
            ConstructionPaid2b[i] = max(ProjectCash2b[i], (Construction_Amount + ConstructionPaid2b.sum()) * (-1))
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
    Mezzanine_InterestedAccrued2b[i] = Mezzanine_InterestedAccrued2b[i - 1] + (
                Mezzanine_InterestedAccrued2b[i - 1] - MezzanineCash2b.sum()) * Mezzanine_InterestRate / 12
    ConstructionReceived2b[i] = ConstructionPaid2b.sum() * (-1) * Construction_InterestRate / 12
    # Then the project cash receives the sale and the month's income. The construction interest for the last month is paid
    ProjectCash2b[i] = ProjectCash2b[i - 1] + CashFlowSchedule2b['CashFlow'][i] - ConstructionReceived2b[i]
    # Max Mortage is limited by max LTV and min DSCR
    mortgageMax = maxMortgageLTV * CashFlowSchedule2b['CashFlow'][i] * 12 / capRate
    # The neccesary mortgage is the amount needed to pay of the construction principle
    mortgageNeccesary = (-1) * ConstructionPaid2b.sum() - ProjectCash2b[i]
    # Confirm that this is allowable under the mortgage conditions. If we aren't, use equity to pay
    if mortgageMax > mortgageNeccesary:
        mortgageAmount = mortgageNeccesary
    else:
        mortgageAmount = mortgageMax
        EquityCash2b[i] = mortgageAmount - mortgageNeccesary
        print('Neccesary Mortgage Not Allowable. Need ' + str(mortgageNeccesary) + ' and can only take out a max of ' +
              str(mortgageMax))
        print('Calculation = ' + str(maxMortgageLTV) + ' * ' + str(CashFlowSchedule2b['CashFlow'][i]) + ' * 12 / ' +
              str(capRate))
    DSCR = CashFlowSchedule2b['CashFlow'][i] / np.pmt(rate=(mortgageInterestRate/2+1)**(2/12)-1,
                                                      fv=0, pv=mortgageAmount, nper=amortizationPeriod * 12) *(-1)
    k=0
    while DSCR < minMortgageDSCR:
        k=k+1
        print('DSCR loop ' + str(k))
        EquityCash2b[i] = EquityCash2b[i] - 100000
        mortgageAmount = mortgageAmount - 100000
        DSCR = CashFlowSchedule2b['CashFlow'][i] / np.pmt(rate=(mortgageInterestRate/2+1)**(2/12)-1,
                                                      fv=0, pv=mortgageAmount, nper=amortizationPeriod * 12)*(-1)
        print('pmt = ')
        print(np.pmt(rate=(mortgageInterestRate/2+1)**(2/12)-1,
                                                      fv=0, pv=mortgageAmount, nper=amortizationPeriod * 12))
        print('mortgage now ' + str(mortgageAmount))
        print('Equity pays ' + str(EquityCash2b[i]))
        print('DSCR = ' + str(DSCR))
    
    if EquityCash2b[i] < 0:
        print('Equity must pay ' + str(EquityCash2b[i]))
        
    # Take out mortgage and put it into the project cash
    mortgagePrinciple = mortgageAmount
    ProjectCash2b[i] = ProjectCash2b[i] + mortgagePrinciple - EquityCash2b[i]

    # Pay off construction loan with the project cash
    ConstructionReceived2b[i] = (-1) * ConstructionPaid2b.sum()
    ProjectCash2b[i] = ProjectCash2b[i] - ConstructionReceived2b[i]

    # Calculate the mortgage payments
    upfront = 0
    monthlyRate = mortgageInterestRate / 12
    periods = amortizationPeriod * 12
    mortgagePrinciplePaid = np.zeros(periods)
    mortgageInterestPaid = np.zeros(periods)
    for period in range(periods):
        mortgagePrinciplePaid[period] = -np.ppmt((mortgageInterestRate/2+1)**(2/12)-1, period, periods, mortgageAmount)
        mortgageInterestPaid[period] = -np.ipmt((mortgageInterestRate/2+1)**(2/12)-1, period, periods, mortgageAmount)

    # Set the payments to end after the term rather than the amortization period
    mortgageInterestPaid = mortgageInterestPaid[:StabilizedLength2b]
    # In the last period, pay off the rest of the principle
    amountLeft = mortgageAmount - mortgagePrinciplePaid[:StabilizedLength2b].sum()
    mortgagePrinciplePaid[StabilizedLength2b - 1] = mortgagePrinciplePaid[StabilizedLength2b - 1] + amountLeft
    mortgagePrinciplePaid = mortgagePrinciplePaid[:StabilizedLength2b]
    
    # Confirm the DSCR is allowable
    DSCR = CashFlowSchedule2b['CashFlow'][i] / (mortgagePrinciplePaid[0] + mortgageInterestPaid[0])
    if DSCR < minMortgageDSCR:
        print('DSCR = ' + str(DSCR) + '. The month is ' + str(i) + ' and we are in default.')

    # Loop, paying off mortgage and mezzanine debt during the stabilized period
    for i in range(LeaseUpLength2b + ConstructionLength2b + 2,
                   LeaseUpLength2b + ConstructionLength2b + StabilizedLength2b):
        ProjectCash2b[i] = ProjectCash2b[i - 1] + CashFlowSchedule2b['CashFlow'][i]
        # Pay mortgage
        ProjectCash2b[i] = ProjectCash2b[i] - mortgageInterestPaid[i - (LeaseUpLength2b + ConstructionLength2b + 2)] -                            mortgagePrinciplePaid[i - (LeaseUpLength2b + ConstructionLength2b + 2)]
        # If not semi annual, then save up money for the semi annual payment =(mortgagePrinciple*mortgageInterestRate/6)
        # Accrue mezzanine interest
        Mezzanine_InterestedAccrued2b[i] = Mezzanine_InterestedAccrued2b[i - 1] + (
                    Mezzanine_InterestedAccrued2b[i - 1] - MezzanineCash2b.sum()) * Mezzanine_InterestRate / 12
        # If it is there to pay, pay mezzanine accrued interest second because mezz debt is expensive 12% money
        if Mezzanine_InterestedAccrued2b[i] > ProjectCash2b[i]:
            # Give project cash to mezzanine lender
            MezzanineInterestPaid2b[i] = ProjectCash2b[i]
            ProjectCash2b[i] = ProjectCash2b[i] - MezzanineInterestPaid2b[i]
            Mezzanine_InterestedAccrued2b[i] = Mezzanine_InterestedAccrued2b[i] - MezzanineInterestPaid2b[i]
        # If we can pay off all of the accrued mezz interest, do so
        if 0 < Mezzanine_InterestedAccrued2b[i] < ProjectCash2b[i]:
            ProjectCash2b[i] = ProjectCash2b[i] - Mezzanine_InterestedAccrued2b[i]
            MezzanineInterestPaid2b[i] = Mezzanine_InterestedAccrued2b[i]
            Mezzanine_InterestedAccrued2b[i] = 0
        # If there is leftover money to pay to mezzanine principle, do so
        if 0 < ProjectCash2b[i] < (-1) * MezzanineCash2b.sum():
            MezzanineCash2b[i] = ProjectCash2b[i]
            ProjectCash2b[i] = ProjectCash2b[i] - MezzanineCash2b[i]
        # If we can pay off the full mezzanine loan, do so
        if 0 < (-1) * MezzanineCash2b.sum() < ProjectCash2b[i]:
            MezzanineCash2b[i] = (-1) * MezzanineCash2b.sum()
            ProjectCash2b[i] = ProjectCash2b[i] - MezzanineCash2b[i]
        # Anything left goes to equity investors
        if ProjectCash2b[i] > 0:
            EquityCash2b[i] = ProjectCash2b[i]
            ProjectCash2b[i] = ProjectCash2b[i] - EquityCash2b[i]

    # In the final month, pay back all mezz debt and accrued interest
    # Pay back rest of mortgage
    # Pay equity investors the rest
    i = LeaseUpLength2b + ConstructionLength2b + StabilizedLength2b
    # Get sale money and pay final mortgage payment
    ProjectCash2b[i] = ProjectCash2b[i - 1] + CashFlowSchedule2b['CashFlow'][i] - (
                mortgagePrinciplePaid[StabilizedLength2b - 1] + mortgageInterestPaid[StabilizedLength2b - 1])
    # Accrue the last month of Mezzanine interest
    Mezzanine_InterestedAccrued2b[i] = Mezzanine_InterestedAccrued2b[i - 1] + (
                Mezzanine_InterestedAccrued2b[i - 1] - MezzanineCash2b.sum()) * Mezzanine_InterestRate / 12
    # Pay the last month of mezzanine interest
    ProjectCash2b[i] = ProjectCash2b[i] - Mezzanine_InterestedAccrued2b[i]
    MezzanineInterestPaid2b[i] = Mezzanine_InterestedAccrued2b[i]
    Mezzanine_InterestedAccrued2b[i] = 0
    # Pay down the mezzanine principle
    MezzanineCash2b[i] = (-1) * MezzanineCash2b.sum()
    ProjectCash2b[i] = ProjectCash2b[i] - MezzanineCash2b[i]

    # Combine the two cash flows for the mezzanine lender
    MezzanineCash2b = MezzanineCash2b + MezzanineInterestPaid2b

    # Equity takes the final cash
    EquityCash2b[i] = ProjectCash2b[i]
    ProjectCash2b[i] = ProjectCash2b[i] - EquityCash2b[i]

    # Calculate one cash flow for Construction lender
    ConstructionCash2b = ConstructionPaid2b + ConstructionReceived2b

    ExampleInvestorCashb = MezzanineCash2b + EquityCash2b * .5
    
    # Calculate MOICs
    ConstructionMOIC2b = ConstructionReceived2b.sum() / ConstructionPaid2b.sum() * (-1)
    MezzanineMOIC2b = MezzanineCash2b[1:].sum() / MezzanineCash2b[0] * (-1)
    EquityMOIC2b = EquityCash2b[EquityCash2b > 0].sum() / EquityCash2b[EquityCash2b < 0].sum() * (-1)
    ExampleMOICb = ExampleInvestorCashb[ExampleInvestorCashb > 0].sum() / ExampleInvestorCashb[ExampleInvestorCashb < 0].sum() * (-1)

    # Calculate annual IRR. Cash flow is monthly, so annualize it here
    ConstructionIRR2b = (1 + np.irr(ConstructionCash2b)) ** 12 - 1
    MezzanineIRR2b = (1 + np.irr(MezzanineCash2b)) ** 12 - 1
    EquityIRR2b = (1 + np.irr(EquityCash2b)) ** 12 - 1
    ExampleIRRb = (1 + np.irr(ExampleInvestorCashb)) ** 12 - 1

    # Total Profit calculations
    ConstructionTotalProfit2b = ConstructionCash2b.sum()
    MezzanineTotalProfit2b = MezzanineCash2b.sum()
    EquityTotalProfit2b = EquityCash2b.sum()
    ExampleTotalProfitb = ExampleInvestorCashb.sum()

    return dict(Timeline2a=dict(ConstructionMOIC=ConstructionMOIC2a, MezzanineMOIC=MezzanineMOIC2a,
                                EquityMOIC=EquityMOIC2a,ConstructionIRR=ConstructionIRR2a,
                                MezzanineIRR=MezzanineIRR2a, EquityIRR=EquityIRR2a,
                                ConstructionTotalProfit=ConstructionTotalProfit2a,
                                MezzanineTotalProfit=MezzanineTotalProfit2a,EquityTotalProfit=EquityTotalProfit2a,
                                exampleMOIC=ExampleMOICa, exampleIRR=ExampleIRRa, exampleTotalProfit=ExampleTotalProfita,
                                cashFlowSchedule=CashFlowSchedule2a),
                Timeline2b=dict(ConstructionMOIC=ConstructionMOIC2b, MezzanineMOIC=MezzanineMOIC2b,
                                EquityMOIC=EquityMOIC2b, ConstructionIRR=ConstructionIRR2b,
                                MezzanineIRR=MezzanineIRR2b, EquityIRR=EquityIRR2b,
                                ConstructionTotalProfit=ConstructionTotalProfit2b,
                                MezzanineTotalProfit=MezzanineTotalProfit2b, EquityTotalProfit=EquityTotalProfit2b,
                                exampleMOIC=ExampleMOICb, exampleIRR=ExampleIRRb, exampleTotalProfit=ExampleTotalProfitb,
                                cashFlowSchedule=CashFlowSchedule2b))


# Inputs for model
capRatex = .04
Unitsx = 260
LeaseUpVacancyRatex = .33
StabilizedVacancyRatex = .02
RentGrowthRatex = 1.025
ParkingGrowthRatex = 1.025
StorageGrowthRatex = 1.025
# Basic cost schedule
CostSchedulex = dict(LandAquisitionCost=-10000000, SoftCosts=-11000000, HardCosts=-53000000, FinancingFees=-1000000,
                    InterestReserve=-8000000)
ConstructionLength2ax = 27  # The length (in months) of the construction period
LeaseUpLength2ax = 12  # The length (in months) of the lease up period
StabilizedLength2ax = 1  # The length (in months) of the lease up period
ConstructionLength2bx = 27  # The length (in months) of the construction period
LeaseUpLength2bx = 12  # The length (in months) of the lease up period
StabilizedLength2bx = 61  # The length (in months) of the lease up period
LeaseUp_Annual_ExpensePerUnitx = -4838.96  # Calculated from sum in Excel of all of the expenses. There is no growth in
# expense during this period, so no need to split up the expenses
Stabilized_Annual_ExpensePerUnit_Scalex = 1  # A scale for making the rent higher or lower
StabilizedRental_Monthly_IncomePerUnitx = 2.60
Construction_Attachmentx = 0
Construction_Detachmentx = 0.75
Construction_InterestRatex = .045
Mezzanine_Attachmentx = .75
Mezzanine_Detachmentx = .875
Mezzanine_InterestRatex = 0.12
Equity_Attachmentx = .875
Equity_Detachmentx = 1
maxMortgageLTVx = .75
minMortgageDSCRx = 1.2
mortgageInterestRatex = 0.03
amortizationPeriodx = 30

# The number of runs for each sensitivity (i.e. how many steps between the outside edges of cap rate and rental rate)
numRuns = 25

# Set up carry vectors
mezzMOICa = np.zeros([numRuns,numRuns])
constrMOICa = np.zeros([numRuns,numRuns])
equiMOICa = np.zeros([numRuns,numRuns])
mezzIRRa = np.zeros([numRuns,numRuns])
constrIRRa = np.zeros([numRuns,numRuns])
equiIRRa = np.zeros([numRuns,numRuns])
mezzTotProfita = np.zeros([numRuns,numRuns])
constrTotProfita = np.zeros([numRuns,numRuns])
equiTotProfita = np.zeros([numRuns,numRuns])
mezzMOICb = np.zeros([numRuns,numRuns])
constrMOICb = np.zeros([numRuns,numRuns])
equiMOICb = np.zeros([numRuns,numRuns])
mezzIRRb = np.zeros([numRuns,numRuns])
constrIRRb = np.zeros([numRuns,numRuns])
equiIRRb = np.zeros([numRuns,numRuns])
mezzTotProfitb = np.zeros([numRuns,numRuns])
constrTotProfitb = np.zeros([numRuns,numRuns])
equiTotProfitb = np.zeros([numRuns,numRuns])

exampleIRRa = np.zeros([numRuns,numRuns])
exampleMOICa = np.zeros([numRuns,numRuns])
exampleTotProfita = np.zeros([numRuns,numRuns])
exampleIRRb = np.zeros([numRuns,numRuns])
exampleMOICb = np.zeros([numRuns,numRuns])
exampleTotProfitb = np.zeros([numRuns,numRuns])

cashFlowa = []
cashFlowb = []

# Run a sensitivity analysis on cap rate and stabilized income per unit
StabilizedRental_Monthly_IncomePerUnitList = np.linspace(2.34, 2.86, numRuns)
capRateList = np.linspace(.035, .045, numRuns)
capRates = np.zeros(numRuns*numRuns)
StabilizedRental_Monthly_IncomePerUnits = np.zeros(numRuns*numRuns)
counter = 0
rounds = 0
for i in range(numRuns*numRuns):
    StabilizedRental_Monthly_IncomePerUnitX = StabilizedRental_Monthly_IncomePerUnitList[rounds]
    print(StabilizedRental_Monthly_IncomePerUnitX)
    capRatex = capRateList[counter]
    capRates[i] = capRatex
    StabilizedRental_Monthly_IncomePerUnits[i] = StabilizedRental_Monthly_IncomePerUnitX
    output = ModelRun(capRate=capRatex, Units=Unitsx, LeaseUpVacancyRate=LeaseUpVacancyRatex,
                      StabilizedVacancyRate=StabilizedVacancyRatex, RentGrowthRate=RentGrowthRatex,
                      ParkingGrowthRate=ParkingGrowthRatex, StorageGrowthRate=StorageGrowthRatex,
                      LandAquisitionCost=CostSchedulex['LandAquisitionCost'], SoftCosts=CostSchedulex['SoftCosts'],
                      HardCosts=CostSchedulex['HardCosts'], FinancingFees=CostSchedulex['FinancingFees'],
                      InterestReserve=CostSchedulex['FinancingFees'], ConstructionLength2a=ConstructionLength2ax,
                      LeaseUpLength2a=LeaseUpLength2ax, StabilizedLength2a=StabilizedLength2ax,
                      ConstructionLength2b=ConstructionLength2bx, LeaseUpLength2b=LeaseUpLength2bx,
                      StabilizedLength2b=StabilizedLength2bx,
                      LeaseUp_Annual_ExpensePerUnit=LeaseUp_Annual_ExpensePerUnitx,
                      Stabilized_Annual_ExpensePerUnit_Scale=Stabilized_Annual_ExpensePerUnit_Scalex,
                      StabilizedRental_Monthly_IncomePerUnit=StabilizedRental_Monthly_IncomePerUnitX,
                      Construction_Attachment=Construction_Attachmentx,
                      Construction_Detachment=Construction_Detachmentx,
                      Construction_InterestRate=Construction_InterestRatex, Mezzanine_Attachment=Mezzanine_Attachmentx,
                      Mezzanine_Detachment=Mezzanine_Detachmentx, Mezzanine_InterestRate=Mezzanine_InterestRatex,
                      Equity_Attachment=Equity_Attachmentx, Equity_Detachment=Equity_Detachmentx,
                      maxMortgageLTV=maxMortgageLTVx, minMortgageDSCR=minMortgageDSCRx,
                      mortgageInterestRate=mortgageInterestRatex, amortizationPeriod=amortizationPeriodx)
    mezzMOICa[counter, rounds] = output['Timeline2a']['MezzanineMOIC']
    constrMOICa[counter, rounds] = output['Timeline2a']['ConstructionMOIC']
    equiMOICa[counter, rounds] = output['Timeline2a']['EquityMOIC']
    mezzIRRa[counter, rounds] = output['Timeline2a']['MezzanineIRR']
    constrIRRa[counter, rounds] = output['Timeline2a']['ConstructionIRR']
    equiIRRa[counter, rounds] = output['Timeline2a']['EquityIRR']
    mezzTotProfita[counter, rounds] = output['Timeline2a']['MezzanineTotalProfit']
    constrTotProfita[counter, rounds] = output['Timeline2a']['ConstructionTotalProfit']
    equiTotProfita[counter, rounds] = output['Timeline2a']['EquityTotalProfit']
    cashFlowa.append(output['Timeline2a']['cashFlowSchedule'])

    mezzMOICb[counter, rounds] = output['Timeline2b']['MezzanineMOIC']
    constrMOICb[counter, rounds] = output['Timeline2b']['ConstructionMOIC']
    equiMOICb[counter, rounds] = output['Timeline2b']['EquityMOIC']
    mezzIRRb[counter, rounds] = output['Timeline2b']['MezzanineIRR']
    constrIRRb[counter, rounds] = output['Timeline2b']['ConstructionIRR']
    equiIRRb[counter, rounds] = output['Timeline2b']['EquityIRR']
    mezzTotProfitb[counter, rounds] = output['Timeline2b']['MezzanineTotalProfit']
    constrTotProfitb[counter, rounds] = output['Timeline2b']['ConstructionTotalProfit']
    equiTotProfitb[counter, rounds] = output['Timeline2b']['EquityTotalProfit']
    cashFlowb.append(output['Timeline2b']['cashFlowSchedule'])
    
    exampleIRRa[counter, rounds] = output['Timeline2a']['exampleIRR']
    exampleMOICa[counter, rounds] = output['Timeline2a']['exampleMOIC']
    exampleTotProfita[counter, rounds] = output['Timeline2a']['exampleTotalProfit']
    exampleIRRb[counter, rounds] = output['Timeline2b']['exampleIRR']
    exampleMOICb[counter, rounds] = output['Timeline2b']['exampleMOIC']
    exampleTotProfitb[counter, rounds] = output['Timeline2b']['exampleTotalProfit']

    counter = counter + 1
    if counter == numRuns:
        rounds = rounds + 1
        counter = 0

# Collect the data in a dataframe to graph it
z_data = pd.DataFrame(equiIRRa)
y_data = pd.DataFrame(equiIRRb)

# Set the column and row labels
z_data.columns = capRateList
z_data.set_index(StabilizedRental_Monthly_IncomePerUnitList, inplace=True)
y_data.columns = capRateList
y_data.set_index(StabilizedRental_Monthly_IncomePerUnitList, inplace=True)

# Plot a 3d mesh of the sensitivity
trace1 = go.Mesh3d(x=capRates,
                   y=StabilizedRental_Monthly_IncomePerUnits,
                   z=equiIRRa.flatten(),
                   opacity=0.7,
                   colorscale='Viridis',
                   name = 'Timeline A',
                   showscale = True
                  )
trace2 = go.Mesh3d(x=capRates,
                   y=StabilizedRental_Monthly_IncomePerUnits,
                   z=equiIRRb.flatten(),
                   opacity=0.7,
                   colorscale='Viridis',
                   name = 'Timeline B',
                   showscale = True
                  )
layout = go.Layout(showlegend=True,
                    scene = dict(
                    xaxis = dict(
                        title='Cap Rate'),
                    yaxis = dict(
                        title='Unit Rate'),
                    zaxis = dict(
                        title='Equity IRR'),),
                    width=700,
                    margin=dict(
                    r=20, b=10,
                    l=10, t=10)
                  )
fig = go.Figure(data=[trace1,trace2], layout=layout)
py.iplot(fig, filename='Equity IRR Sensitivity to Cap Rate and Rental Rates')


# Repeat the above for MOIC and total profit
trace1 = go.Mesh3d(x=capRates,
                   y=StabilizedRental_Monthly_IncomePerUnits,
                   z=equiMOICa.flatten(),
                   opacity=0.7,
                   colorscale='Viridis',
                   name = 'Timeline A'
                  )
trace2 = go.Mesh3d(x=capRates,
                   y=StabilizedRental_Monthly_IncomePerUnits,
                   z=equiMOICb.flatten(),
                   opacity=0.7,
                   colorscale='Viridis',
                   name = 'Timeline B'
                  )
layout = go.Layout(showlegend=True,
                    scene = dict(
                    xaxis = dict(
                        title='Cap Rate'),
                    yaxis = dict(
                        title='Unit Rate'),
                    zaxis = dict(
                        title='Equity MOIC'),),
                    width=700,
                    margin=dict(
                    r=20, b=10,
                    l=10, t=10)
                  )
fig = go.Figure(data=[trace1,trace2], layout=layout)
py.iplot(fig, filename='Equity MOIC Sensitivity to Cap Rate and Rental Rates')

trace1 = go.Mesh3d(x=capRates,
                   y=StabilizedRental_Monthly_IncomePerUnits,
                   z=equiTotProfita.flatten(),
                   opacity=0.7,
                   colorscale='Viridis',
                   name = 'Timeline A'
                  )
trace2 = go.Mesh3d(x=capRates,
                   y=StabilizedRental_Monthly_IncomePerUnits,
                   z=equiTotProfitb.flatten(),
                   opacity=0.7,
                   colorscale='Viridis',
                   name = 'Timeline B'
                  )
layout = go.Layout(showlegend=True,
                    scene = dict(
                    xaxis = dict(
                        title='Cap Rate'),
                    yaxis = dict(
                        title='Unit Rate'),
                    zaxis = dict(
                        title='Equity Total Profit'),),
                    width=700,
                    margin=dict(
                    r=20, b=10,
                    l=10, t=10)
                  )
fig = go.Figure(data=[trace1,trace2], layout=layout)
py.iplot(fig, filename='Equity Total Profit Sensitivity to Cap Rate and Rental Rates')

# Run the base model to get the investor returns and the sensitivity data tables
Base = ModelRun()

# Write out cash flow schedules
cashFlowa = pd.DataFrame(Base['Timeline2a']['cashFlowSchedule'])
cashFlowa.columns = ['Cash Flow Timeline A', 'Month']
cashFlowb = pd.DataFrame(Base['Timeline2b']['cashFlowSchedule'])
cashFlowb.columns = ['Cash Flow Timeline B', 'Month']

cashFlowa.to_csv('~/CashFlowTimeline2a.csv')
cashFlowb.to_csv('~/CashFlowTimeline2b.csv')

# Write out investor returns
Investor = pd.DataFrame(dict(ExampleInvestorTimeline2a=[Base['Timeline2a']['exampleIRR'], Base['Timeline2a']['exampleMOIC'], 
                                                Base['Timeline2a']['exampleTotalProfit']], 
                            ExampleInvestorTimeline2b = [Base['Timeline2b']['exampleIRR'], Base['Timeline2b']['exampleMOIC'],
                                                  Base['Timeline2b']['exampleTotalProfit']], 
                            ConstructionTimeline2a=[Base['Timeline2a']['ConstructionIRR'], Base['Timeline2a']['ConstructionMOIC'], 
                                                Base['Timeline2a']['ConstructionTotalProfit']], 
                            ConstructionTimeline2b=[Base['Timeline2b']['ConstructionIRR'], Base['Timeline2b']['ConstructionMOIC'],
                                                  Base['Timeline2b']['ConstructionTotalProfit']], 
                            MezzanineTimeline2a=[Base['Timeline2a']['MezzanineIRR'], Base['Timeline2a']['MezzanineMOIC'], 
                                                Base['Timeline2a']['MezzanineTotalProfit']], 
                            MezzanineTimeline2b=[Base['Timeline2b']['MezzanineIRR'], Base['Timeline2b']['MezzanineMOIC'],
                                                  Base['Timeline2b']['MezzanineTotalProfit']], 
                             EquityTimeline2a=[Base['Timeline2a']['EquityIRR'], Base['Timeline2a']['EquityMOIC'], 
                                                Base['Timeline2a']['EquityTotalProfit']], 
                            EquityTimeline2b=[Base['Timeline2b']['EquityIRR'], Base['Timeline2b']['EquityMOIC'],
                                                  Base['Timeline2b']['EquityTotalProfit']], 
                            ))

Investor['Return Type'] = ['IRR', 'MOIC', 'Total Profit']

Investor.set_index('Return Type', inplace=True)
Investor.to_csv('~/InvestorReturns.csv')

# Write out sensitivities
SensitivityAEquityIRR = pd.DataFrame(equiIRRa)
SensitivityAEquityIRR.columns = np.array(StabilizedRental_Monthly_IncomePerUnitList).round(3)
SensitivityAEquityIRR['Cap Rate'] = np.array(capRateList).round(5)
SensitivityAEquityIRR.set_index('Cap Rate', inplace=True)
SensitivityAEquityIRR.to_csv('~/EquityIRRSensitivity_TimelineA.csv')

SensitivityBEquityIRR = pd.DataFrame(equiIRRb)
SensitivityBEquityIRR.columns = np.array(StabilizedRental_Monthly_IncomePerUnitList).round(3)
SensitivityBEquityIRR['Cap Rate'] = np.array(capRateList).round(5)
SensitivityBEquityIRR.set_index('Cap Rate', inplace=True)
SensitivityBEquityIRR.to_csv('~/EquityIRRSensitivity_TimelineB.csv')

SensitivityBEquityMOIC = pd.DataFrame(equiMOICb)
SensitivityBEquityMOIC.columns = np.array(StabilizedRental_Monthly_IncomePerUnitList).round(3)
SensitivityBEquityMOIC['Cap Rate'] = np.array(capRateList).round(5)
SensitivityBEquityMOIC.set_index('Cap Rate', inplace=True)
SensitivityBEquityMOIC.to_csv('~/EquityMOICSensitivity_TimelineB.csv')

SensitivityAEquityMOIC = pd.DataFrame(equiMOICa)
SensitivityAEquityMOIC.columns = np.array(StabilizedRental_Monthly_IncomePerUnitList).round(3)
SensitivityAEquityMOIC['Cap Rate'] = np.array(capRateList).round(5)
SensitivityAEquityMOIC.set_index('Cap Rate', inplace=True)
SensitivityAEquityMOIC.to_csv('~/EquityMOICSensitivity_TimelineA.csv')

