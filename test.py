# import pandas as pd
# district = pd.read_csv("district.csv")
# def whichdistrict(id):
#     d =  district[district.id ==id]
#     return (d.prefix.values + ' ' + d.name.values)
# lst = [whichdistrict(x) for x in district.id]
# district['district_name']=lst
# district.to
# print(whichdistrict(1))
import numpy as np

map = np.load('Ver.04/map_GAKSOM2.npy', allow_pickle=True)
mapping = np.load('Ver.04/mapping_GAKSOM2.npy', allow_pickle=True)
label_map = np.load('Ver.04/label_map_new_GAKSOM2.npy', allow_pickle=True)
label_map_district = np.load('Ver.04/label_map_district_new_GAKSOM2.npy', allow_pickle=True)
c = 0
for i in range(100):
    for j in range(100):
        if(isinstance(label_map_district[i][j],list)):
            c +=len(label_map_district[i][j])
print(c)

def get_direction(deep):
    if(deep == 0):
        return [[0,0]]
    if(deep > 0):
        lst = []
        for x in range(-deep,deep+1):
            for y in range(-deep,deep+1):
                if x == deep or y == deep or x == -deep or y == -deep:
                    lst.append([x,y])
        return lst
def getSurroundings(matrix,x,y,deep=5):
	res = []
	for direction in get_direction(deep):
		cx = x + direction[0]*deep
		cy = y + direction[1]*deep
		if(cy >=0 and cy < len(matrix)):
			if(cx >=0 and cx < len(matrix[cy])):
				res.append(matrix[cy][cx])
	return res

# print(getSurroundings(label_map_district,10,10))
print(get_direction(10))