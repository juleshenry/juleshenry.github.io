d = '''-25% Housing
-15% Transportation
-12% Groceries
-10% Savings
-10% Utilities
-5% Holidays/Gifts
-5% Charity
-5% Clothing
-5% Entertainment
-3% Miscellaneous
'''
dd = [o.split(' ')[1] for o in d.split('\n') if o]

single = 59384
single_monthly = 3925
def allots(x,p):return [p/100*xx for xx in x]

(e:=allots([25,15,12,10,10,5,5,5,5,3],single_monthly))
s = ' '.join([str(int(ee)) + ' for ' + d.lower() + ',' for d,ee in zip(dd,e)])
print(s)

family_household =  74580
family_household_monthly = 4767

(e:=allots([25,15,12,10,10,5,5,5,5,3],family_household_monthly))
s = ' '.join([str(int(ee)) + ' for ' + d.lower() + ',' for d,ee in zip(dd,e)])
print(s)