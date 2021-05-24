from flask import Flask, render_template, url_for, request, redirect, Response
import os
os.system('pip install -r requirements.txt')
os.system('pip install pymongo[srv]')
# pymongo[srv]==3.11.3
from gen_dataset import gen_dataset
# import folium
import datetime
import pymongo
import pandas as pd
import random
from folium_mapp import folium_mapp
from folium_map_new import folium_mapp_new
from flask_caching import Cache
config = {
    "DEBUG": True,          # some Flask specific configs
    # "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": 'localhost',
    "CACHE_REDIS_PORT": '6379',
    "CACHE_REDIS_URL": 'redis://localhost:6379',
    # "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
# tell Flask to use the above defined config
# app.config.from_mapping(config)
cache = Cache(app,config=config)
# cache.set
def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))
def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)
@app.route('/', methods=["GET","POST"])
def mainpage():

  if request.method == "POST":
      longitude = request.form["longitude"]
      latitude = request.form["latitude"]
      return lredirect(url_for("form", longitude=longitude, latitude=latitude))

  return render_template("main.html")
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
        ".csv": "text/csv",
        ".png":"image/png"
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)
@app.route('/getmethod/<jsdata>')
def get_javascript_data(jsdata):
    return jsdata

@app.route('/form')
def form():
    id = request.args.get('id', type=float)
    print(int(id))
    # return folium_mapp(int(id))._repr_html_()
    return False
    # return render_template("form.html", longitude=id, latitude=id)
some_list = []
@cache.cached(timeout=50)
@app.route('/labelKsomNew', methods=["GET", "POST"])
def labelKsomNew():
    # if request.method == 'POST':
    #     data = request.form['gglat']
    #     idPost = data
    #     print(data)
    #     return folium_mapp_new(data)._repr_html_()
    idPost = {}
    
    idPost['id']=-1
    idPost['position_street'] = request.args.get('position_street', type=float)
    idPost['gglat']=request.args.get('gglat', type=float)
    idPost['gglong']=request.args.get('gglong', type=float)
    # price_m2 = request.args.get('price_m2', type=float)
    price_new = request.args.get('price_new', type=float)
    limit = request.args.get('limit', type=int)
    distance_type = request.args.get('distance_type', type=str)
    if(distance_type):
        if not distance_type in ['physical','logical']:
            distance_type = 'physical'
    return folium_mapp_new(idPostt=idPost,distance_type=distance_type,limit=limit,price_new = price_new)._repr_html_()
    # return folium_mapp_new(idPostt=idPost)._repr_html_()

@cache.cached(timeout=50)
@app.route('/labelKsom', methods=["GET", "POST"])
def labelKsom():
    if request.method == 'POST':
        pass
        # data = request.form['gglat']
        # idPost = data
        # print(data)

        # return folium_mapp_new(data)._repr_html_()
    # idPost = {}
    # print(idPost)
    # idPost['id']=-1
    # idPost['position_street'] = request.args.get('position_street', type=float)
    # idPost['gglat']=request.args.get('gglat', type=float)
    # idPost['gglong']=request.args.get('gglong', type=float)
    # else:
    else:
        id = request.args.get('id', type=int)
        limit = request.args.get('limit', type=int)
        price_m2 = request.args.get('price', type=float)
        price_new = request.args.get('price_new', type=float)
        if(price_m2 == 0.0):
            price_m2 = price_new
        price_ratio = float(price_new)/float(price_m2) -1.0
        if (not limit):
            limit = 0
        if(not id):
            id = 539702
        print(id)
        html = cache.get(str(id)+str(limit)+str(price_ratio))
        if(cache.get(str(id)+str(limit)+str(price_ratio))):
            return html
        else:
            print('cache not found id:'+str(id)+str(limit))
            html = folium_mapp(id,price_ratio=price_ratio,limit=limit)._repr_html_()
            cache.set(str(id)+str(limit)+str(price_ratio),html)
            return html
    
    # if(id and idPost['position_street'] is None):
    #     return folium_mapp(id)._repr_html_()
    # elif(idPost['position_street'] is not None):
    #     return folium_mapp_new(id,idPost)._repr_html_()
    # else:
    #     return folium_mapp(id)._repr_html_()

    # if(idPost['position_street']):
    #     return folium_mapp_new(idPostt=idPost)._repr_html_()
    # elif(id):
    #     return folium_mapp(int(id),idPost=idPost)._repr_html_()
    # else:
    #     return folium_mapp_new(-1,idPostt=idPost)._repr_html_()
@app.route('/label', methods=["GET", "POST"])
def label():
    id = request.args.get('id', type=int)
    extend = request.args.get('extend', type=int)
    print(id)
    if(extend):
        lst = []
        df_post2 = pd.read_csv('dataset/all.csv')
        id_post = df_post2[df_post2['id']==int(str(id))]
        id_district = id_post['address_district'].values[0]
        dis_len = len(df_post2[df_post2['address_district']==id_district])
        try:
            ids = random.sample(range(dis_len), extend)
            lst.append(df_post2[df_post2['address_district']==id_district].iloc[ids])
        except:
            lst.append(df_post2[df_post2['address_district']==id_district])
        df = pd.concat(lst)
        df.to_csv('dataset/temp/'+str(int(id_district))+str(extend)+'.csv')
    if request.method == 'POST':
        passdata = request.form
        print('post')
    #     some_list.append(passdata)

    #     print('data submitted successfuly')
        print(passdata)
        return redirect(request.url)
        # return redirect(url_for('label'),id=id)
    # print(int(id))
    # return folium_mapp(int(id))._repr_html_()
    
    return render_template("label.html", id=float(str(id)),extend=str(extend))
@cache.cached(timeout=50)
@app.route('/pickapoint', methods=["GET", "POST"])
def pickapoint():
    id = request.args.get('id', type=int) if request.args.get('id', type=int) else -1
    extend = request.args.get('extend', type=int) if request.args.get('extend', type=int) else -1
    print(id)
    if(extend):
        lst = []
        df_post2 = pd.read_csv('dataset/all.csv')
        if(id != -1):
            try:
                id_post = df_post2[df_post2['id']==int(str(id))]
                id_district = id_post['address_district'].values[0]
                dis_len = len(df_post2[df_post2['address_district']==id_district])
                try:
                    ids = random.sample(range(dis_len), extend)
                    lst.append(df_post2[df_post2['address_district']==id_district].iloc[ids])
                except:
                    lst.append(df_post2[df_post2['address_district']==id_district])
                df = pd.concat(lst)
                df.to_csv('dataset/temp/'+str(int(id_district))+str(extend)+'.csv')
            except:
                id = -1
    if request.method == 'POST':
        passdata = request.form
        print('post')
    #     some_list.append(passdata)

    #     print('data submitted successfuly')
        print(passdata)
        return redirect(request.url)
        # return redirect(url_for('label'),id=id)
    # print(int(id))
    # return folium_mapp(int(id))._repr_html_()
    html = cache.get('pickapoint')
    if(cache.get('pickapoint')):
        return html
    else:
        print('cache not found')
        html = render_template("pickapoint.html", id=float(str(id)),extend=str(extend))
        cache.set('pickapoint',html)
        return html

    # return render_template("pickapoint.html", id=float(str(id)),extend=str(extend))
# os.system('python -m pip install pymongo[srv]')
# import pymongo
client = pymongo.MongoClient("mongodb+srv://thuan:thuan@cluster0.4a1w9.mongodb.net/atomic?authSource=admin&replicaSet=atlas-1i0fgy-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true")
db = client.atomic
col = db.labelpost
col2 = db.pickedpost
@app.route('/receivedata', methods=['POST'])
def receive_data():
    print({'id1':request.form['id1'],'id2':request.form['id2'],'class':request.form['class'],"date": datetime.datetime.utcnow()})
    col.insert_one({'id1':request.form['id1'],'id2':request.form['id2'],'class':request.form['class'],"date": datetime.datetime.utcnow()})
    return 'OK'

@app.route('/pickdata', methods=['POST'])
def pick_data():
    print({'id2':request.form['id2'],'district':request.form['district']})
    
    col2.insert_one({'id':request.form['id2'],'district':request.form['district']})
    return 'OK'

@app.route('/dataset', methods=["GET"])
def dataset():
    limit = request.args.get('limit', type=int)
    gen_dataset(limit=limit)
    return 'Dataset with limit = ' + str(limit) +' created!'

if __name__ == "__main__":
  app.run(debug=False) 