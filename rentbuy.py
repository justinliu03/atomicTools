# def nearest_metro(zip):
# 
    # return metro, state
# Currently, we will be using a state, instead of a zipcode metro area lookup
import pandas as pd
import numpy as np
prop = pd.read_excel("Rent_Buy_Data.xlsx", sheet_name = "property tax")
prop.set_index('State', inplace = True)
ins = pd.read_excel("Rent_Buy_Data.xlsx", sheet_name = "Insurance")
ins.set_index('State', inplace = True)
appr = pd.read_excel("Rent_Buy_Data.xlsx", sheet_name = "state appr")
appr.set_index('State', inplace = True)

def rent_buy_tool(discount_rate, mortgage_rate, house_cost, state, investment_growth, rent_growth, down_payment, equiv_rent, length_of_stay, loan_term):

    home_appr = appr.loc[state, '1-Year'] * 0.01
    insurance = ins.loc[state, 'Insurance']
    prop_tax = prop.loc[state, 'tax'] * house_cost

    data = []
    mortgage = (1-down_payment) * house_cost
    home_equity = down_payment * house_cost
    cum_rent_buy = 0
    down_payment_equiv = home_equity
    pos = []

    for n in range(1, loan_term + 1):
        arr = []
        # cash spent
        interest = mortgage * mortgage_rate
        principle = interest / (1 - (1+mortgage_rate)**(-loan_term)) - interest
        total_cash_spent = interest + principle + insurance + prop_tax
        mortgage -= interest
        arr.append(total_cash_spent)

        # net cost of buy
        net_equity = home_equity * home_appr + principle
        home_equity += net_equity
        net_cost_buy = total_cash_spent - net_equity

        # net cost of rent
        down_payment_growth = down_payment_equiv * investment_growth
        down_payment_equiv += down_payment_growth
        net_cost_rent = equiv_rent - down_payment_growth

        # rent - buy
        rent_buy = net_cost_rent - net_cost_buy
        cum_rent_buy += rent_buy
        arr.append(net_cost_rent)
        arr.append(net_cost_buy)
        arr.append(rent_buy)
        arr.append(cum_rent_buy)
        data.append(arr)

        #based on yearly cost
        if rent_buy > 0:
            pos.append(n)

    if pos == []:
        verdict = "Rent"
    elif length_of_stay >= pos[0]:
        verdict = "Buy"
    else:
        verdict = "Rent"

    df = pd.DataFrame(data, columns =['Total Spent', 'Net cost rent', 'net cost buy', 'rent - buy', 'cumulative rent - buy']) 
    df.index = np.arange(1, len(df) + 1)
    print(df,'\n',verdict)

rent_buy_tool(0.05, 0.07, 1000000, 'Florida', 0.06, 0.05, 0.2, 60000, 5, 30)