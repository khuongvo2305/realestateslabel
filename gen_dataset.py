import pandas as pd
import random
import argparse
def gen_dataset(limit=100,file='dataset/all'):
    try:
        f = open(file+str(limit)+'.csv')
    except IOError:
        df_post2 = pd.read_csv(file+'.csv')
        lst = []
        for i in range(1,25):
            dis_len = len(df_post2[df_post2['address_district']==i])
            try:
                ids = random.sample(range(dis_len), limit)
                lst.append(df_post2[df_post2['address_district']==i].iloc[ids])
            except:
                lst.append(df_post2[df_post2['address_district']==i])
        df = pd.concat(lst)
        df.to_csv(file+str(limit)+'.csv')
    # finally:
        # f.close()

parser = argparse.ArgumentParser()
parser.add_argument('--limit', help='Limit')
args = parser.parse_args()
gen_dataset(limit = args.limit)