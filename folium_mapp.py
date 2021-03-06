import pandas as pd
import folium
import json
import numpy as np
import math
from colour import Color
from unidecode import unidecode
def folium_mapp(idd):
  data_post = pd.read_csv("dataset/all100.csv")
  # data_post = data_post[data_post["address_district"] == 11] # Quan 10
  data_post = data_post[data_post["address_city"] == 1] # HCM
  # print(idd)
  print(data_post[data_post["id"] == idd])
  idPost = data_post[data_post["id"] == idd].iloc[0]
  data_district = pd.read_csv("district.csv")

  def color_a_point(row):
    color="#0375B4" # blue
    for i in range(0, len(arr)):
      if int(row['id']) in arr[i]:
        color = colors[i].get_hex()
      if int(row['id']) in arr[0]:
        color = "#FFCE00" # orange
    return color

  def plot_station_counts(data_post):
      i = j = k = 0
      # generate a new map
      folium_map = folium.Map(location=[idPost['gglat'], idPost['gglong']],
                              zoom_start=13,
                              max_zoom=25,
                              tiles="CartoDB dark_matter",
                              width='50%')

      # for each row in the data, add a cicle marker
      for index, row in data_post.iterrows():
          # # calculate net departures
          # net_departures = (row["Departure Count"]-row["Arrival Count"])
          
          # generate the popup message that is shown on click.
          i = 0
          for i in range(0, len(arr)):
            if int(row['id']) in arr[i]:
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
                  """
          popup_text = popup_text.format(
                  row["id"],
                  unidecode(str(row["address_street"])),
                  unidecode(str(row["address_ward"])),
                  unidecode(str(data_district[data_district["id"] == int(row["address_district"])]["name"].values[0])),
                  row["position_street"],
                  row["gglat"],
                  row["gglong"],
                  i)
          
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
                              radius=3 if color_a_point(row) == "#FFCE00" else 1,
                              color=color_a_point(row),
                              popup=popup_text,
                              fill=True).add_to(folium_map)
          
          if color_a_point(row) == "#007849":
            i += 1
          if color_a_point(row) == "#FFCE00":
            j += 1
          if color_a_point(row) == "#0375B4":
            k += 1
      print("green: %s, orange: %s, blue: %s" % (i, j, k))
      return folium_map
  def surroundingMatrixIndex(arr, idx, deep): # surround an element in array
    indexSurround = []
    if len(arr) == 0 or deep > len(arr)/2:
      return []
    if deep == 0:
      return [idx]
    if deep > 0 and deep <len(arr)/2 +1:
      indexSurround = []
      
      if (idx[0]-deep > 0):
        for j in range(idx[1]-deep,idx[1]+deep+1):
          if (j>=0 and j<len(arr[0])):
            indexSurround.append((idx[0]-deep,j))

      if (idx[0]+deep < len(arr)):
        for j in range(idx[1]-deep,idx[1]+deep+1):
          if (j>=0 and j<len(arr[0])):
            indexSurround.append((idx[0]+deep,j))

      for i in range(idx[1]-deep+1,idx[1]+deep):
        if(i>=0 or i<=len(arr[0])):
          if (idx[1]+deep < len(arr[0])):
            indexSurround.append((i,idx[1]+deep))
          if (idx[1]-deep > 0):
            indexSurround.append((i,idx[1]-deep))
      return [x for x in set(indexSurround) if len(arr[0])>x[0] >=0 and len(arr[1])>x[1]>=0]
    return []

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

  map = np.load('Ver.04/map_GAKSOM.npy', allow_pickle=True)
  mapping = np.load('Ver.04/mapping_GAKSOM.npy', allow_pickle=True)
  label_map = np.load('Ver.04/label_map_new_GAKSOM.npy', allow_pickle=True)
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
  label_map_district = np.load('Ver.04/label_map_district_new_GAKSOM.npy', allow_pickle=True)
  # np.save('Ver.04/label_map_district_GAKSOM.npy',label_map_district)
  arr = []
  LOL = np.array([      [idPost['gglat'], idPost['gglong'], score_pos_street(idPost['position_street'])]      ])
  predict_idx = closest_node(LOL, 0, map, Rows, Cols)
  print("predict:")
  pred = label_map_district[predict_idx]
  for i in range(0, 100):
    lst = []
    for index in surroundingMatrixIndex(label_map_district, predict_idx, i):
      pred_idx = label_map_district[index]
      if (pred_idx != " || "):
        # lst += [int(pred_idx.split(" _ ")[0][4:])]
        lst += [pred_idx]

    arr.append(lst)
  red = Color("#FE0000")
  green = Color ("#008000")
  blue = Color("#0000FF")
  white = Color("#FFFFFF")
  colors = list(red.range_to(green, 100))
  plot_station_counts(data_post)
  mymapp = plot_station_counts(data_post)
  return mymapp


# folium_mapp(539702)