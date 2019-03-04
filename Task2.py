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

# Notes to myself
# All money comes in at month 0
# Payments
# Up to Stabilized:
#   Construction gets annual interest = Budget*(Construction_Detachment - Construction_Attachment) *
#       Construction_InterestRate
#   Mezzanine accrues interest = Budget * (Mezzanine_Detachment - Mezzanine_Attachment) * Mezzanine_InterestRate
#   Equity gets all excess and funds all shortfalls

ProjectCash2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
ProjectCash2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
ConstructionCash2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
ConstructionCash2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
MezzanineCash2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
MezzanineCash2b = np.zeros(CashFlowSchedule2b['Month'].__len__())
EquityCash2a = np.zeros(CashFlowSchedule2a['Month'].__len__())
EquityCash2b = np.zeros(CashFlowSchedule2b['Month'].__len__())

# Make a timeline for Project cash, Construction, Mezzanine and equity
# Starting cash amounts
ProjectCash2a[0] = Budget + CashFlowSchedule2a['CashFlow'][0]
ProjectCash2b[0] = Budget + CashFlowSchedule2a['CashFlow'][0]

ConstructionCash2a[0] = (-1) * Construction_Amount
ConstructionCash2a[0] = (-1) * Construction_Amount

MezzanineCash2a[0] = (-1) * Mezzanine_Amount
MezzanineCash2b[0] = (-1) * Mezzanine_Amount
Mezzanine_InterestedAccrued = 0

EquityCash2a[0] = (-1) * Equity_Amount
EquityCash2b[0] = (-1) * Equity_Amount

# For the period up to the stabilized period, use cash to build the project and pay construction loan. Mezzanine loan
for i in range(1, LeaseUpLength2a + ConstructionLength2a + 1):
    # Augment the project cash by the amount spent/gained and the interest paid. In the lease up an construction period,
    # the only interest paid is on the construction loan
    ProjectCash2a[i] = ProjectCash2a[i-1] + CashFlowSchedule2a['CashFlow'][i] - Construction_Amount * Construction_InterestRate / 12)
    # Record the amount of interest accrued by the mezzanine loan but don't pay it yet
    Mezzanine_InterestedAccrued = Mezzanine_InterestedAccrued + Mezzanine_Amount * Mezzanine_InterestRate / 12
    # Give the interest to the construction loaner
    ConstructionCash2a.append(ConstructionCash2a + Construction_Amount * Construction_InterestRate / 12)

# Once this period has completed, the property is stabilized and the construction loan principle will be paid back
# Excess cash will be used to fund the interest accrued by the mezzanine loan

