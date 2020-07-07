import sys
import math
# print(f"name : {sys.argv[0]=}")
# print(f"arguments : {sys.argv[1:]=}")
# print(sys.argv[1:])
d = {
    "type" : None,
    "payment" : None,
    "principal" : None,
    "periods" : None,
    'interest' : None
}
for i in sys.argv[1:]:
    a = i.split('=')
    d.update({a[0][2:] : a[1]})
# print(d)
counter_error = 0


if d.get('type') not in ['diff', 'annuity']:
    print("Incorrect parameters")
    quit()
if d.get("interest") is None:
    print("Incorrect parameters")
    quit()
if d.get('type') == 'diff' and d.get('payment'):
    print("Incorrect parameters")
    quit()
if d.get("type") == 'diff':
    if d.get("principal") is None or d.get("periods") is None or d.get("interest") is None:
        print("Incorrect parameters")
        quit()
if d.get("type") == 'annuity':
    for i in d.values():
        if i is None:
            counter_error += 1
    if counter_error >=2:
        print("Incorrect parameters")
        quit()



if d.get("type") == 'diff':
    pay_list = []
    if float(d.get("principal")) < 0 or float(d.get("periods")) < 0 or float(d.get("interest")) < 0:
        print("Incorrect parameters")
        quit()
    i = float(d.get('interest')) / 1200
    principal = float(d.get('principal'))
    periods = int(d.get("periods"))
    for m in range(1, periods+1):
        calc = (principal / periods) + i * ( principal - ((principal * (m - 1))/periods))
        pay_list.append(math.ceil(calc))
    # print(pay_list)
    counter_month = 1
    for k in pay_list:
        print("Month {}: paid out {}".format(counter_month, k))
        counter_month += 1
    print("Overpayment = ",int(sum(pay_list) - principal))

if d.get("type") == "annuity":

    if d.get("periods") is None:
        if float(d.get("principal")) < 0 or float(d.get("interest")) < 0:
            print("Incorrect parameters")
            quit()
        principal = float(d.get('principal'))
        monthly_payment = int(d.get('payment'))
        i = float(d.get('interest')) / 1200
        n = math.log(monthly_payment / (monthly_payment - (i * principal)), 1 + i)
        months = math.ceil(n)

        if months < 12:
            print("You need {} months to repay this credit!".format(months))

        elif months == 12:
            print("You need 1 year to repay this credit!")
        elif 12 < months < 24:
            if months == 13:
                print("You need 1 year and 1 month to repay this credit!")
            else:
                print("You need 1 year and {} months to repay this credit!".format(months - 12))
        elif months > 12 and months % 12 == 0:
            print("You need {} years to repay this credit!".format(months // 12))
        elif months >= 24:
            if months % 12 == 1:
                print("You need {} years and 1 month to repay this credit!".format(months // 12))
            else:
                print("You need {} years and {} months to repay this credit!".format(months // 12, months % 12))
        print("Overpayment = ", int(months * monthly_payment - principal))
    if d.get("payment") is None:
        if float(d.get("principal")) < 0 or float(d.get("periods")) < 0 or float(d.get("interest")) < 0:
            print("Incorrect parameters")
            quit()
        principal = float(d.get('principal'))
        months = int(d.get("periods"))
        i = float(d.get('interest')) / 1200
        monthly_payment = principal * (i * (1 + i) ** months) / ((1 + i) ** months - 1)
        print("Your annuity payment = {}!".format(math.ceil(monthly_payment)))
        print("Overpayment = ", int(months * math.ceil(monthly_payment) - principal))#не было округления

    if d.get("principal") is None:
        if  float(d.get("periods")) < 0 or float(d.get("interest")) < 0:
            print("Incorrect parameters")
            quit()
        monthly_payment = int(d.get('payment'))
        months = int(d.get("periods"))
        i = float(d.get('interest')) / 1200
        principal = monthly_payment / ((i * ((1 + i) ** months)) / ((1 + i) ** months - 1))
        print("Your credit principal = {}!".format(math.floor(principal)))#ранее был round
        print("Overpayment = ", int(months * monthly_payment - math.floor(principal)))#ранее не было округления