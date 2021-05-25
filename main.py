import pandas

raw_data_df = pandas.read_csv("rawdata.csv", engine='python', keep_default_na=False)
raw_data_dict = raw_data_df.to_dict(orient="records")

BW_payments_df = pandas.read_csv("BWPayments.csv", engine='python', keep_default_na=False)
BW_payments_dict = BW_payments_df.to_dict(orient="records")



used_list = []
used_la_list = []
used_rd_list = []
new_list = []
new_la_list = []
new_rd_list = []



for unit in raw_data_dict:
    new_unit = {}

    # fix year
    if unit['YR'] > 25:
        unit['YR'] = str(unit['YR'])
        unit['YR'] = "19" + unit['YR']
    else:
        unit['YR'] = unit['YR'] + 2000

    # create year-make-model column, add to new_unit
    new_unit['YRMAKEMODEL'] = str(unit['YR']) + " " + unit['BRAND'] + " " + unit['MODEL']

    # add the stock# and serial, etc to the new_unit
    new_unit['STOCK #'] = unit['STOCK #']
    new_unit['CHASSI'] = unit['CHASSI']
    new_unit['LOT'] = unit['LOT']
    new_unit['D'] = unit['D']

    # put lowest price into promo column, add promo price to new_unit
    if unit['WEB PRC'] == '0':
        unit['PROMO PRICE'] = unit['MIN TAKE']
        new_unit['PROMO PRICE'] = unit['PROMO PRICE']
    else:
        unit['PROMO PRICE'] = unit["WEB PRC"]
        new_unit['PROMO PRICE'] = unit['PROMO PRICE']

    # separate new and used
    if int(new_unit['PROMO PRICE'].replace(",", "")) > 2990:
        if str(new_unit['D']) == 'N':
            new_list.append(new_unit)
        else:
            used_list.append(new_unit)

# calc biweekly payments on new units
for unit2 in new_list:
    if len(unit2['PROMO PRICE']) <= 6:
        temp_promo = unit2['PROMO PRICE'][:2]
    else:
        temp_promo = unit2['PROMO PRICE'][:3]

    for payment in BW_payments_dict:
        if int(temp_promo) == int(payment['PRICE']):
            unit2['BW'] = payment['BW']
            unit2['COB'] = payment['COB']
            unit2['INT'] = payment['INT']
            unit2['TERM'] = payment['TERM']
            unit2['AMORT'] = payment['AMORT']

    # fix BW payment format
    unit2['BW'] = "$" + str(unit2['BW'])

    # fix COB format
    unit2['COB'] = str(unit2['COB'])
    if len(unit2['COB']) >= 5:
        unit2['COB'] = unit2['COB'][:2] + ',' + unit2['COB'][2:]
    elif 4 >= len(unit2['COB']) >= 3:
        unit2['COB'] = unit2['COB'][:1] + ',' + unit2['COB'][1:]
    else:
        pass

    # put new units into files sorted by lot
    if unit2['LOT'] == "RD":
        new_rd_list.append(unit2)
    else:
        new_la_list.append(unit2)

# export new info in csv
new_rd_df = pandas.DataFrame(new_rd_list)
new_rd_df.to_csv("new_rd.csv", index=False)

new_la_df = pandas.DataFrame(new_la_list)
new_la_df.to_csv("new_la.csv", index=False)


# export used info to csv

for unit3 in used_list:
    if unit3['LOT'] == "RD":
        used_rd_list.append(unit3)
    else:
        used_la_list.append(unit3)

used_rd_df = pandas.DataFrame(used_rd_list)
used_rd_df.to_csv("used_rd.csv", index=False)

used_la_df = pandas.DataFrame(used_la_list)
used_la_df.to_csv("used_la.csv", index=False)