import pandas as pd
import folium
import json
import numpy as np
import math
from colour import Color
from unidecode import unidecode
import numpy
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform 
import pymongo
def folium_mapp_new(idd=-1,idPostt=None,distance_type='logical',limit=0,price_ratio=0.5,price_new=100.0):
  def get_df():
    client = pymongo.MongoClient("mongodb+srv://thuan:thuan@cluster0.4a1w9.mongodb.net/atomic?authSource=admin&replicaSet=atlas-1i0fgy-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true")
    db = client.atomicbds
    collection = db.data_post
    df = pd.DataFrame(list(collection.find()))
    df['id'] = df['id'].astype(int)
    df['gglat'] = df['gglat'].astype(float)
    df['gglong'] = df['gglong'].astype(float)
    df['address_city'] = df['address_city'].astype(float).astype(int)
    df['position_street'] = df['position_street'].astype(float).astype(int)
    return df
  data_post = get_df()
  data_post = data_post[data_post["address_city"] == 1] # HCM
  print(len(data_post))

  # if(idd==-1 and idPostt is not None):
  #   v1 = np.array([idPostt['gglat'],idPostt['gglong'],idPostt['position_street'],-1.0])
  #   max_len = 999.999
  #   max_idx = -1
  #   f_dict = lambda v1,v2: euc_dist(v1[:2],v2[:2])
  #   if (distance_type == 'logical'):
  #     f_dict = latlong_posstreet_for_max
  #   for indexx, row in data_post.iterrows():
  #     v2 = np.array([row['gglat'],row['gglong'],row['position_street']])
  #     llpt = f_dict(v1,v2)
  #     max_len = min(max_len,llpt)
  #     if(max_len == llpt):
  #         max_idx = row['id']
  #   idd = max_idx
  #   idPost = data_post[data_post["id"] == idd].iloc[0]
  
  
  data_district = pd.read_csv("district.csv")
  labeled = [595347,197574,595347,728022,539702,133762,595347,648824,151611,585779,90505,193579,90505,295901,90505,316913,90505,113096,614411,430301,539702,405019,320512,409878,652053,732480,614411,63428,303680,109919,303680,441339,539702,80248,652053,468045,299557,144908,539702,536729,595347,664312,614411,568236,614411,398661,303680,307731,435447,503553,595347,622751,652053,526136,652053,526136,75320,430195,75320,685946,151611,690287,721528,288939,621291,317757,539702,63818,652053,309152,652053,57550,652053,673630,122845,596146,721528,732288,577544,763033,595347,508729,122845,605561,320512,169733,151611,717646,151611,616848,621291,727332,435447,724328,151611,336802,303680,407222,614411,305266,303680,290332,621291,622003,577544,169279,621291,94057,299557,116847,503553,47888,614411,719986,539702,327366,122845,294564,539702,581740,75320,303817,721528,643041,303680,601918,614411,566384,503553,655052,614411,617461,503553,127978,539702,535122,721528,132468,539702,322154,721528,585622,577544,588940,539702,603657,122845,535670,435447,725757,122845,390904,90505,639116,721528,80300,503553,435447,595347,320682,621291,343055,621291,107399,577544,725366,503553,452345,595347,201498,621291,442576,539702,587892,320512,308147,621291,555167,90505,59078,539702,464764,721528,688220,75320,730348,90505,112705,320512,169733,122845,50954,539702,585667,577544,78046,299557,738857,652053,471501,151611,105324,614411,548107,90505,566362,122845,735541,299557,473644,614411,506172,503553,180465,122845,629412,614411,112692,614411,299384,303680,311072,614411,509482,621291,544250,614411,178290,90505,308169,577544,588940,539702,459370,90505,739050,320512,118873,621291,497351,75320,73580,539702,454142,320512,535680]
  construct_price={'Tiết Kiệm':4500000.0,'Cơ Bản':5100000.0,'Trung Bình':5500000.0,'Khá':5850000.0,'Cao Cấp':8300000.0}
  def cal_land_price_per_m2(row,construct_type='Cơ Bản'):
    try:
      return (float(row.price_sell) - float(row.floor)*construct_price[construct_type])/float(row.area_cal)
    except:
      return (float(row.price_sell) - float(row.floor)*construct_price[construct_type])/float(1.0)
  def cal_house_price(row, land_price_per_m2=0.0,construct_type='Cơ Bản'):
    try:
      return float(row.floor)*construct_price[construct_type] + float(land_price_per_m2)*float(row.area_cal)
    except:
      return float(row.floor)*construct_price[construct_type] + float(land_price_per_m2)*float(1.0)
  
  # def get_price_m2_of_a_point_with_deep(price_m2,deep):
  #   return price_m2*(1+math.pow(1.1,(int(deep)/100)))
  def get_price_ratio_of_a_point_with_deep(price_ratio,deep):
    return 1 + price_ratio/math.pow(1.1,(int(deep)/100))
  
  
  def size_a_point(row,center):
    if int(row['id']) == center:
      return 20
    if int(row['id']) in labeled:
      if int(row['id']) in arr_dist[0]:
        return 15
      else:
        return 10
    elif int(row['id']) in arr_dist[0]:
      return 7
    else:
      return 4
  def color_a_point(row):
    color="#0375B4" # blue
    # for i in range(0, len(arr)):
    for i in arr_dist:
      # if int(row['id']) in labeled:
      #   color = white
      # else:
      if int(row['id']) in arr_dist[i]:
        color = colors[i].get_hex()
      if int(row['id']) in arr_dist[0]:
        color = "#FFCE00" # orange
    return color

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
  def getSurroundings(matrix,x,y,deep):
    res = []
    for direction in get_direction(deep):
      cx = x + direction[0]
      cy = y + direction[1]
      if(cy >=0 and cy < len(matrix)):
        if(cx >=0 and cx < len(matrix[cy])):
          res.append(matrix[cy][cx])
    return res
  def plot_station_counts(data_post):
      i = j = k = 0
      # generate a new map
      folium_map = folium.Map(location=[idPostt['gglat'], idPostt['gglong']],
                              zoom_start=20,
                              max_zoom=25,
                              tiles="CartoDB positron",
                              width='50%')
      folium.CircleMarker(location=(idPostt["gglat"], idPostt["gglong"]),
                              radius=20,
                              color="#0375B4",
                              popup="NEW MARKER, Post street: "+str(idPostt['position_street']),
                              fill=True).add_to(folium_map)
      # for each row in the data, add a cicle marker

      # if(limit==0):
      #   lim = len(data_post)
      # else:
      #   lim = limit

      for index, row in data_post.iterrows():
        # if(index > limit or limit = 0):
        # if(index > lim):
        #   break
        # else:

        # # calculate net departures
        # net_departures = (row["Departure Count"]-row["Arrival Count"])
        
        # generate the popup message that is shown on click.
        i = 0
        # for i in range(0, len(arr)):
        #   if int(row['id']) in arr[i]:
        #     break
        for i in arr_dist:
          if int(row['id']) in arr_dist[i]:
            break
        
        popup_text = """
                ID: {}<br> 
                Address Street: {}<br> 
                Address Ward: {}<br> 
                Address District: {}<br> 
                Position Street: {}<br>
                Latitude: {}<br>
                Longitude: {}<br>
                Deep: {}<br>
                Labeled: {}<br>
                Old Price: {}<br>
                Old Price/m2 in DB: {}<br>
                Old Price/m2 by Formular: {}<br>
                New Price/m2: {}<br>
                New Price2: {}<br>
                Diff: {}<br>
                Ratio: {}<br>
                """
        # new_price_m2 = get_price_m2_of_a_point_with_deep(price_m2,i)
        new_ratio = get_price_ratio_of_a_point_with_deep(price_ratio,i)
        new_price_m2 = float(row["price_sell"])*float(new_ratio)
        popup_text = popup_text.format(
                row["id"],
                unidecode(str(row["address_street"])),
                unidecode(str(row["address_ward"])),
                unidecode(str(row["district_name"])),
                row["position_street"],
                row["gglat"],
                row["gglong"],
                i,
                int(row["id"]) in labeled,
                row["price_sell"],
                row["price_m2"],
                cal_land_price_per_m2(row),
                new_price_m2,
                cal_house_price(row,new_price_m2),
                cal_house_price(row,new_price_m2) - float(row["price_sell"]),
                new_ratio
                )
        # print(popup_text)
        # # radius of circles
        # radius = net_departures/20
        
        # # choose the color of the marker
        # if net_departures>0:
        #     # color="#FFCE00" # orange
        #     # color="#007849" # green
        #     color="#E37222" # tangerine
        # else:
        #     # color="#0375B4" # blue
        #     # color="#FFCE00" # yellow            
        #     color="#0A8A9F" # teal
        
        # add marker to the map
        if color_a_point(row) != "#0375B4":
          folium.CircleMarker(location=(row["gglat"], row["gglong"]),
                            radius=size_a_point(row,idPost['id']),
                            color=color_a_point(row),
                            popup=popup_text,
                            fill=True).add_to(folium_map)
        
        if color_a_point(row) == "#007849":
          i += 1
        if color_a_point(row) == "#FFCE00":
          j += 1
        if color_a_point(row) == "#0375B4":
          folium.CircleMarker(location=(row["gglat"], row["gglong"]),
                            radius=1,
                            color=color_a_point(row),
                            popup=popup_text,
                            fill=True).add_to(folium_map)
          k += 1
          
      print("green: %s, orange: %s, blue: %s" % (i, j, k))
      return folium_map
  def closest_node(data, t, map, m_rows, m_cols):
    # (row,col) of map node closest to data[t]
    result = (0,0)
    small_dist = 1.0e20
    for i in range(m_rows):
      for j in range(m_cols):
        # ed = euc_dist(map[i][j], data[t])
        ed = latlong_posstreet(map[i][j], data[t])
        if ed < small_dist:
          small_dist = ed
          result = (i, j)
    return result

  def closest_node_index(data,list_v2):
    # (row,col) of map node closest to data[t]
    v1 = data[0]
    small_dist = 1.0e20
    result = -1
    for index,v2 in enumerate(list_v2):
      v1[3]=v2[3]
      ed = latlong_posstreet(v1,v2)
      if ed < small_dist:
        small_dist = ed
        result = index
    return result

  def closest_node_physical_index(data,list_v2):
    # (row,col) of map node closest to data[t]
    v1 = data[0]
    small_dist = 1.0e20
    result = -1
    for index,v2 in enumerate(list_v2):
      v1[3]=v2[3]
      ed = euc_dist(v1[:2],v2[:2])
      if ed < small_dist:
        small_dist = ed
        result = index
    return result
  def latlong_posstreet(v1, v2):
    distance_latlong = np.linalg.norm(v1[:2] - v2[:2]) * 1000 # lấy 2 giá trị đầu tính latlong

    delta = np.linalg.norm(v1[2] - v2[2]) 
    distance_district_latlong = np.linalg.norm(v1[3:5] - v2[3:5]) * 1000 / 2
    # distance_street = np.linalg.norm(v1[5:7] - v2[5:7])

    # distance = sigma + alpha * delta + abs(beta * distance_latlong) + gamma * distance_district_latlong + abs(omega * street)
    distance = sigma + alpha * delta + abs(beta * distance_latlong) + gamma * distance_district_latlong
    return distance

  def score_pos_street(id_pos_street): # convert id pos_street to score
    id_pos_street = int(float(id_pos_street))
    if id_pos_street == 1:
      return c[0]
    if id_pos_street == 2:
      return c[1]
    if id_pos_street == 3:
      return c[2]
    if id_pos_street == 4:
      return c[3]
    if id_pos_street == 5:
      return c[4]
    if id_pos_street == 6:
      return c[5]
    return id_pos_street
  
  def euc_dist(v1, v2):
    return np.linalg.norm(v1 - v2) 

  def manhattan_dist(r1, c1, r2, c2):
    return np.abs(r1-r2) + np.abs(c1-c2)

  def most_common(lst, n):
    # lst is a list of values 0 . . n
    if len(lst) == 0: return -1
    counts = np.zeros(shape=n, dtype=np.int)
    for i in range(len(lst)):
      counts[lst[i]] += 1
    return np.argmax(counts)

  
  # Initial variables for model
  

  # Initial variables for logic distance
  # Initial data_x, data_y, name
  [alpha, beta, gamma, omega, sigma, c] = [3.12506638, -9.00115707,  4.35316446, -97.95369439, -6.64789365, [-16.16039254, -12.96374504, -21.42898834, -16.06295894, -16.23441444, -18.69862314]]

  nrows = len(data_post.index)
  data_x = []
  data_x_dictrict = []
  data_x_street = []
  for i in range(0, nrows):
    data_x.append(data_post["latlongpos"].iloc[i])
    data_x_dictrict.append([data_post["district_lat"].iloc[i], data_post["district_long"].iloc[i]])
    data_x_street.append(data_post["latlong_street"].iloc[i])

  data_x = [x[:2]+[score_pos_street(x[2])] for x in data_x]

  for i in range(0, nrows):
    data_x[i].extend(data_x_dictrict[i])
    data_x[i].extend(data_x_street[i])
  # print(data_x)
  data_y = []
  for i in range(0, nrows):
    data_y.append(data_post["id"].iloc[i])
    
  name = []
  for index, row in data_post.iterrows():
    name.append((row.id))  

  
  np.random.seed(1)
  Dim = len(data_x[0])
  Rows = 100; Cols = 100
  RangeMax = Rows + Cols
  LearnMax = 0.5            # 0.5
  StepsMax = 15000          # 20000
  

  # Initial variables for logic distance
  

  map = np.load('Ver.04/map_GAKSOM2.npy', allow_pickle=True)
  mapping = np.load('Ver.04/mapping_GAKSOM2.npy', allow_pickle=True)
  label_map = np.load('Ver.04/label_map_new_GAKSOM2.npy', allow_pickle=True)
  # label_map_district = np.empty(shape=(len(label_map), len(label_map)), dtype=object)
  # m = 0
  # name = []
  # for index, row in data_post.iterrows():
  #   name.append((row.id))
  # for col in range(0, len(label_map_district)):
  #   for row in range(0, len(label_map_district)):
  #     # print(label_map[col][row])
  #     if label_map[col][row] == -1:
  #       label_map_district[col][row] = " || "
  #     else:
  #       # label_map_district[col][row] = name[label_map[col][row]]
  #       m += 1
  label_map_district = np.load('Ver.04/label_map_district_new_GAKSOM2.npy', allow_pickle=True)
  # np.save('Ver.04/label_map_district_GAKSOM2.npy',label_map_district)
  # arr = []
  # try:
  #   LOL = np.array([      [idPost['gglat'], idPost['gglong'], score_pos_street(idPost['position_street'])]      ])
  # except:
  
  LOL = np.array([      [idPostt['gglat'], idPostt['gglong'], score_pos_street(idPostt['position_street']),-1.0]      ])
  predict_idx = closest_node(LOL, 0, map, Rows, Cols)
  # idd = data_y[closest_node_index(LOL, data_x)]
  if (distance_type == 'physical'):
    idd = data_y[closest_node_physical_index(LOL, data_x)]
  else:
    idd = data_y[closest_node_index(LOL, data_x)]
  print(predict_idx)
  print(idd)

  # pred = label_map_district[predict_idx]
  # print(pred)
  try:
    idPost = data_post[data_post["id"] == idd].iloc[0]
  except Exception as e:
    print(e)
    idPost = data_post[data_post["id"] == idd[0]].iloc[0]
  price_m2 = cal_land_price_per_m2(idPost)
  price_ratio = price_new/price_m2 -1.0
  print("predict:")
  # pred = label_map_district[predict_idx]
  # print(pred)
  arr = [[] for i in range(1000)]
  arr_dist = {}
  arr_dist[0]=[]
  count = 0
  for i in range(0, 100):
    # lst = []
    # lst_distance = []
    
    for index in getSurroundings(label_map_district, predict_idx[0],predict_idx[1], i):
      # pred_idx = label_map_district[index]
      # print(i,index,pred_idx)
      pred_idx=index
      if (pred_idx != " || "):
        # lst += [int(pred_idx.split(" _ ")[0][4:])]
        # lst += pred_idx
        # coordinates = []
        idPost_coordinate = np.array([idPost['gglat'], idPost['gglong']])
        
        # distance_post = []
        
        for iddx in pred_idx:
          try:
            pred_idd = np.array([data_post[data_post["id"] == iddx].iloc[0]['gglat'],data_post[data_post["id"] == iddx].iloc[0]['gglong']])
            # distance_post.append(i*10+(int(euc_dist(pred_idd,idPost_coordinate)*100)%10))
            try:
              arr_dist[i*10+(int(euc_dist(pred_idd,idPost_coordinate)*100)%10)].append(iddx)
            except:
              arr_dist[i*10+(int(euc_dist(pred_idd,idPost_coordinate)*100)%10)]=[iddx]
            count +=1
            # print(count)
          except:
            pass

  red = Color("#FE0000")
  green = Color ("#008000")
  blue = Color("#0000FF")
  white = Color("#FFFFFF")
  colors = list(red.range_to(green, 1000))

  # plot_station_counts(data_post)
  mymapp = plot_station_counts(data_post)
  return mymapp


# folium_mapp_new(539702)