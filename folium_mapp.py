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
def folium_mapp(idd,idPost=None,limit=0):
  data_post = pd.read_csv("dataset/all.csv")
  print(len(data_post))
  center_id = idd
  # data_post = data_post[data_post["address_district"] == 11] # Quan 10
  data_post = data_post[data_post["address_city"] == 1] # HCM
  # print(idd)
  # print(data_post[data_post["id"] == idd].iloc[0])
  idPost = data_post[data_post["id"] == idd].iloc[0]
  data_district = pd.read_csv("district.csv")
  labeled = [595347,197574,595347,728022,539702,133762,595347,648824,151611,585779,90505,193579,90505,295901,90505,316913,90505,113096,614411,430301,539702,405019,320512,409878,652053,732480,614411,63428,303680,109919,303680,441339,539702,80248,652053,468045,299557,144908,539702,536729,595347,664312,614411,568236,614411,398661,303680,307731,435447,503553,595347,622751,652053,526136,652053,526136,75320,430195,75320,685946,151611,690287,721528,288939,621291,317757,539702,63818,652053,309152,652053,57550,652053,673630,122845,596146,721528,732288,577544,763033,595347,508729,122845,605561,320512,169733,151611,717646,151611,616848,621291,727332,435447,724328,151611,336802,303680,407222,614411,305266,303680,290332,621291,622003,577544,169279,621291,94057,299557,116847,503553,47888,614411,719986,539702,327366,122845,294564,539702,581740,75320,303817,721528,643041,303680,601918,614411,566384,503553,655052,614411,617461,503553,127978,539702,535122,721528,132468,539702,322154,721528,585622,577544,588940,539702,603657,122845,535670,435447,725757,122845,390904,90505,639116,721528,80300,503553,435447,595347,320682,621291,343055,621291,107399,577544,725366,503553,452345,595347,201498,621291,442576,539702,587892,320512,308147,621291,555167,90505,59078,539702,464764,721528,688220,75320,730348,90505,112705,320512,169733,122845,50954,539702,585667,577544,78046,299557,738857,652053,471501,151611,105324,614411,548107,90505,566362,122845,735541,299557,473644,614411,506172,503553,180465,122845,629412,614411,112692,614411,299384,303680,311072,614411,509482,621291,544250,614411,178290,90505,308169,577544,588940,539702,459370,90505,739050,320512,118873,621291,497351,75320,73580,539702,454142,320512,535680]
  def size_a_point(row):
    if int(row['id']) == center_id:
      return 20
    if int(row['id']) in labeled:
      if int(row['id']) in arr_dist[0]:
        return 20
      else:
        return 15
    elif int(row['id']) in arr_dist[0]:
      return 7
    else:
      return 3
  def color_a_point(row):
    color="#0375B4" # blue
    if int(row['id']) == center_id:
      return color
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

  def plot_station_counts(data_post):
      i = j = k = 0
      # generate a new map
      folium_map = folium.Map(location=[idPost['gglat'], idPost['gglong']],
                              zoom_start=13,
                              max_zoom=25,
                              tiles="CartoDB positron",
                              # tiles="CartoDB dark_matter",
                              width='50%')

      # for each row in the data, add a cicle marker
      if(limit==0):
        lim = len(data_post)
      else:
        lim = limit
      for index, row in data_post.iterrows():
        # if(index > limit or limit = 0):
        if(index > lim):
          break
        else:

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
                  """
          popup_text = popup_text.format(
                  row["id"],
                  unidecode(str(row["address_street"])),
                  unidecode(str(row["address_ward"])),
                  unidecode(str(data_district[data_district["id"] == int(row["address_district"])]["name"].values[0])),
                  row["position_street"],
                  row["gglat"],
                  row["gglong"],
                  i,
                  int(row["id"]) in labeled)
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
                              radius=size_a_point(row),
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
  def surroundingMatrixIndex(arr, idx, deep): # surround an element in array
    # print(getSurroundings(arr,idx[0],idx[1]))
    return getSurroundings(arr,idx[0],idx[1])[deep]
    # indexSurround = []
    # if len(arr) == 0 or deep > len(arr)/2:
    #   return []
    # if deep == 0:
    #   return [idx]
    # if deep > 0 and deep <len(arr)/2 +1:
    #   indexSurround = []
      
    #   if (idx[0]-deep > 0):
    #     for j in range(idx[1]-deep,idx[1]+deep+1):
    #       if (j>=0 and j<len(arr[0])):
    #         indexSurround.append((idx[0]-deep,j))

    #   if (idx[0]+deep < len(arr)):
    #     for j in range(idx[1]-deep,idx[1]+deep+1):
    #       if (j>=0 and j<len(arr[0])):
    #         indexSurround.append((idx[0]+deep,j))

    #   for i in range(idx[1]-deep+1,idx[1]+deep):
    #     if(i>=0 or i<=len(arr[0])):
    #       if (idx[1]+deep < len(arr[0])):
    #         indexSurround.append((i,idx[1]+deep))
    #       if (idx[1]-deep > 0):
    #         indexSurround.append((i,idx[1]-deep))
    #   return [x for x in set(indexSurround) if len(arr[0])>x[0] >=0 and len(arr[1])>x[1]>=0]
    # return []

  def score_pos_street(id_pos_street): # convert id pos_street to score
    id_pos_street = float(id_pos_street)
    if id_pos_street == 1:
      return 5.13000151
    if id_pos_street == 2:
      return -4.11031906
    if id_pos_street == 3:
      return -5.37830437
    if id_pos_street == 4:
      return 2.54340878
    if id_pos_street == 5:
      return 1.11500722
    if id_pos_street == 6:
      return -4.5762099
    return id_pos_street
    # closest_node(data_x, t, map, Rows, Cols)
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

  def latlong_posstreet(v1, v2):
    distance_latlong = np.linalg.norm(v1[:2] - v2[:2]) # lấy 2 giá trị đầu tính latlong

    p1 = (v1[2])
    p2 = score_pos_street((v2[2]))
    delta = np.linalg.norm(p1 - p2) 
    distance = (beta + alpha * math.exp( gamma * delta  )) * distance_latlong
    return distance

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
  np.random.seed(1)
  Dim = 3
  Rows = 100; Cols = 100
  RangeMax = Rows + Cols
  LearnMax = 0.7            # 0.5
  StepsMax = 12000          # 20000

  # Initial variables for logic distance
  beta = -8.30421441
  alpha = 0.06557144
  gamma = 0.88806504

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
  LOL = np.array([      [idPost['gglat'], idPost['gglong'], score_pos_street(idPost['position_street'])]      ])
  predict_idx = closest_node(LOL, 0, map, Rows, Cols)
  print("predict:")
  pred = label_map_district[predict_idx]
  # print(pred)
  arr = [[] for i in range(1000)]
  arr_dist = {}
  arr_dist[0]=[]
  count = 0
  for i in range(0, 100):
    # lst = []
    # lst_distance = []
    
    for index in getSurroundings(label_map_district, predict_idx[0],predict_idx[1], i):
    # for index in surroundingMatrixIndex(label_map_district, predict_idx, i):

      # print(index)
      # pred_idx = label_map_district[index]
      pred_idx=index
      # print(i,index,pred_idx)
      if (pred_idx != " || "):
        # lst += [int(pred_idx.split(" _ ")[0][4:])]
        # lst += pred_idx
        # coordinates = []
        idPost_coordinate = np.array([idPost['gglat'], idPost['gglong']])
        
        # distance_post = []
        
        for idd in pred_idx:
          try:
            pred_idd = np.array([data_post[data_post["id"] == idd].iloc[0]['gglat'],data_post[data_post["id"] == idd].iloc[0]['gglong']])
            # distance_post.append(i*10+(int(euc_dist(pred_idd,idPost_coordinate)*100)%10))
            # print(i*10+(int(euc_dist(pred_idd,idPost_coordinate)*100)%10))
            try:
              arr_dist[i*10+(int(euc_dist(pred_idd,idPost_coordinate)*100)%10)].append(idd)
            except:
              arr_dist[i*10+(int(euc_dist(pred_idd,idPost_coordinate)*100)%10)]=[idd]
            count +=1
            
          except Exception as e:
            print(str(e) + ' id: ' + str(idd))
  # print(count)
          # print(i*10+(int(euc_dist(pred_idd,idPost_coordinate)*100)%10),idd)
        # lst_distance.append(distance_post)

        # if(len(coordinates)>1):
          # coordinates_array = numpy.array(coordinates)
          # dist_array = pdist(coordinates_array)
          # dist_matrix = squareform(dist_array)
          # for i_x,x in enumerate(dist_matrix):
          #   for i_y,y in enumerate(x):
          #     if(i_x > i_y):
          #       print(pred_idx[i_x],pred_idx[i_y])
          #       print(i*10+(int(y*100)%10))

    # print(lst)
    # print(lst_distance)
    
    # arr.append(lst)
  # print(arr_deep)


  # asda = [len(arr_dist[x]) for x in arr_dist]
  # print([x for x in arr_dist])
  # print(asda)
  # print(sum(asda))


  red = Color("#FE0000")
  green = Color ("#008000")
  blue = Color("#0000FF")
  white = Color("#FFFFFF")
  colors = list(red.range_to(green, 1000))

  # plot_station_counts(data_post)
  mymapp = plot_station_counts(data_post)
  return mymapp


# folium_mapp(539702)