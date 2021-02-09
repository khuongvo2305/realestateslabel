import pandas as pd
district = pd.read_csv("district.csv")
def whichdistrict(id):
    d =  district[district.id ==id]
    return (d.prefix.values + ' ' + d.name.values)
lst = [whichdistrict(x) for x in district.id]
district['district_name']=lst
district.to
print(whichdistrict(1))