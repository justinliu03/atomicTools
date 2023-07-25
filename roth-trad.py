import pandas as pd
import numpy as np
def roth_trad_tool(age, retirement_age, cur_income, annual_contr, investment_return, cur_tax, retirement_tax):
    if age <= 50:
        annual_contr = max(6500, annual_contr)
    else:
        annual_contr = max(7500, annual_contr)
    money_spent = annual_contr * (1 + cur_tax) #tax doesn't affect how much I can contribute?
    roth = 0
    trad = 0
    for n in range(age, retirement_age):
        roth *= (1 + investment_return)
        trad *= (1 + investment_return)
        if n < 71: #must also consider mandatory withdrawals for trad
            trad += annual_contr
        if cur_income > 133000: # must consider 'phase out'
                annual_contr = 0
        roth += annual_contr
    trad = trad * (1 - retirement_tax)
    #consider withdrawals less than 5 years and before age 60
    print("roth:", roth, "trad:", trad)

roth_trad_tool(20, 80, 40000, 5500, 0.07, 0.1, 0.25)