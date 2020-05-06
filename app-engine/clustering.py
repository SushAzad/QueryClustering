import numpy as np 
import sklearn 
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn import metrics

import mongo_operations as m
import json



'''
  How to use: 
    import clustering as cl;
    features = cl.Features();
      # defaults--db='Queries', emb_type='embedding'
    myjson=features.cluster();
      # defaults--name='agglomerative', n_clusters=6, dist=0.35, link='ward', 
    q_type='original', printing=False, emb_type='embedding'

'''

class Features:

  # Creates initial DB connection
  def __init__(self, db='Queries', emb_type='embedding'):

    # connect to mongo 
    self.mongo = m.MongoDB(db)
    self.queries={}
    self.emb={}
    self.parsed_queries={}

    # mongodb keys: 
    # dict_keys(['_id', 'queryNum', 'questionId', 'variantId', 
    # 'rawQueryContent', 'test', 'parsedRemovedQuery', 'embedding'])
  

    # get queries from Mongo 'Queries'
    # get embeddings 
    # queryNum-->[variantID, queryText]
    # queryNum--> emb 
    for i in self.mongo.read_queries({}):
      self.emb[i['queryNum']]=i[emb_type]
      self.queries[i['queryNum']]=[i['variantId'], i['rawQueryContent']]
      self.parsed_queries[i['queryNum']]=[i['variantId'], i['parsedRemovedQuery']]


  '''
    Clustering algorithms from scikit-learn:
      - kmeans 
          num_clusters (k): number of centroids to draw clusters around. (default: 6)
      - mean_shift 
      - agglomerative 
          distance_threshold: difference in which to split a cluster (default: 0.35)
          linkage: how to join new data to existing clusters (default: 'ward')

      Input: 
        Data (embeddings)
        Clustering algo parameters 
      Output
        Cluster assignments (in same order as data )
  '''


  def kmeans(self, data, NUM_CLUSTERS):
    km = KMeans(n_clusters=NUM_CLUSTERS)
    km.fit(data)

    clusters = km.labels_.tolist()
    x = np.asarray(clusters)
    nc=self.get_num_clusters(x)
    print("Distribution of clusters: " + str(len(nc)))
    print(nc)

    return x


  def mean_shift(self, data):
    clustering = MeanShift().fit(data)

    x=clustering.labels_
    nc=self.get_num_clusters(x)
    print("Distribution of clusters: " + str(len(nc)))
    print(nc)

    return x

  def agglom(self, data, dist, link):
    clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=dist, linkage=link).fit(data)
    x=clustering.labels_
    nc=self.get_num_clusters(x)
    print("Distribution of clusters: " + str(len(nc)))
    print(nc)

    return x



  '''
    Utils 
  '''

  def get_num_clusters(self, clusters):
    counter={}
    for i in clusters:
      if i in counter: 
        counter[i]+=1
      else:
        counter[i] = 1
    return counter


  def get_all_question_queries(self):

    queries=self.queries
    emb=self.emb

    data={}
    labels={}
    
    emb_length=len(emb[list(emb.keys())[0]])
    
    for q in queries:
      variant=queries[q][0]
      if variant in labels:
        labels[variant].append(q)
        # try except to catch instances where there are no embeddings for a query...
        # then, we just append zeros
        try:
          data[variant].append(np.asarray(emb[q]))
        except:
          print("Err: queryNum " + str(q) + " embeddings not found")
          data[variant].append(np.zeros(emb_length))
      else:
        labels[variant] = [q]
        try:
          data[variant] = [np.asarray(emb[q])]
        except:
          print("Err: queryNum " + str(q) + " embeddings not found")
          data[variant] = [np.zeros(emb_length)]
          
    return data, labels
        

  '''
    example of input: 
    - kmeans (default: n_clusters=6)
    - mean_shift (no parameters)
    - agglomerative (default: dist=0.35, link='ward')
      ex: get_all_clusters(queries, emb, 'agglomerative', dist=0.25, link='complete')
  '''


  def get_all_clusters(self, name, n_clusters, dist, link):

    queries=self.queries
    emb=self.emb

    # variant --> [query]
    all_data, all_labels= self.get_all_question_queries()
    
    # variant --> [cluster assignments]
    all_clusters={}
    
    
    for v in all_labels: 
      data=all_data[v]
      qids=all_labels[v]

      print("Question: " + str(v) +", "+str(len(qids)) + " queries.")
      
      clustering=""
      if len(data) > 1: 
        if name =="kmeans": 
          # need to make sure queries are > n_clusters; otherwise, assign all to one cluster
          if len(data) > n_clusters:
            clustering=self.kmeans(data, n_clusters)
          else:
            clustering=np.asarray(np.zeros(len(data)))
        elif name=="mean_shift":
          clustering=self.mean_shift(data)
        elif name=="agglomerative":
          clustering=self.agglom(data, dist, link)
      else:
        clustering = np.asarray([0])
      
      try:
        score = silhouette_score(data, clustering)
        print("Silhouette score: %0.3f" %score)
      except: 
        print("Silhouette score: N/A. Only one cluster predicted")
      
      print("\n")
      all_clusters[v] = clustering
      
    return all_labels, all_clusters




  def to_JSON(self, all_labels, all_clusters, q_type):
    

    queries=self.queries
    if q_type=='parsed':
      queries=self.parsed_queries

    json_queries={}
    for idx, v in enumerate(all_labels):
      qids=all_labels[v]
      clusters=all_clusters[v]
      v_str=str(v)
      json_queries[v_str]={}

      for jdx, qid in enumerate(qids):
        cluster=str(clusters[jdx])
        if cluster not in json_queries[v_str]:
          json_queries[v_str][cluster] = [{
            'queryNum': str(qid),
            'query': queries[qid][1]
          }]
        else:
          json_queries[v_str][cluster].append({
            'queryNum': str(qid),
            'query': queries[qid][1]
          })

    return json.dumps(json_queries)  



  '''
    Main function 
    Input: 
      - name = string, type of algo (agglomerative, kmeans, or mean_shift)
      - n_clusters = numeric. used for kmeans...will automatically exclude 
        the questions with fewer queries than n_clusters
      - dist = float, used for agglomerative clustering.
      - link = string (ward, complete, minimum, average)
      - emb_type = string (representing the embeddingcolumn in MongoDB)
      - q_type = string (original or parsed). type of queries to return in JSON
      - printing= boolean, for debug statements



  '''

  def getEmbeddings(self, emb_type):
    for i in self.mongo.read_queries({}):
      self.emb[i['queryNum']]=i[emb_type]
    

  def cluster(self, name='agglomerative', n_clusters=6, dist=0.35, link='ward', 
    q_type='original', emb_type='embedding', printing=False): 


    # queries=self.queries


    getEmbeddings(emb_type)
    all_labels, all_clusters=self.get_all_clusters(name, n_clusters, dist, link, emb_type)

    my_json = self.to_JSON(all_labels, all_clusters, q_type)

    return my_json


    