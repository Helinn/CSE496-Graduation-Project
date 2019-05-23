"""this python file is used to construct the fake data for the model"""
import random
import json
import numpy as np
import mysql.connector
import Tweet as tweet
from datetime import datetime

from networkx import *
import networkx.algorithms as nxalg

def read_data_from_database():
    mydb = mysql.connector.connect(
        user = "root",
        password = "D12345",
        host = "localhost",
        database = "tweetermysql_2018-07-30"
    )

    my_cursor = mydb.cursor()

    my_cursor.execute(' select ID, MetaData, Date, Section from news_2017_01 where day(Date) = "1" limit 2')

    my_result = my_cursor.fetchall()
    
    data = list()
    
    for item in my_result:
        u, m_data, date, section = item
        t = tweet.Tweet(u,section,m_data,datetime.strptime(date,'%Y-%m-%d'))
        data.append(t)
    
    return data

def create_graph(tweet):
    G1 = nx.Graph()

    #for tweet in tweets:
    G1.add_node(tweet.user)
    tweetFormat = str(tweet.Id)
    G1.add_edge(tweet.user,tweetFormat,weight=1.0)
    #G1.add_edge(YEAR_TAG,tweet.date.year,weight=15.0)
    #G.add_edge(tweet.date.year,YEAR_TAG,weight=1.0)
    for word in tweet.text.split():
        G1.add_edge(word,tweetFormat,weight=1.0)
        #print(word)
    monthFormat = "{month}.{year}".format(month=tweet.date.month,year=tweet.date.year)

    G1.add_edge(str(tweet.date.year),monthFormat,weight=1.0)
    G1.add_edge(monthFormat,str(tweet.date.year),weight=1.0)

    dayFormat = "{day}.{month}.{year}".format(day=tweet.date.day,month=tweet.date.month,year=tweet.date.year)
    G1.add_edge(monthFormat,dayFormat,weight=1.0)
    G1.add_edge(dayFormat,tweetFormat,weight=1.0)
    return G1

def create_random_graph(tweets, filePath, graph_scale):
    """

    :param type: the graph type
    :param filePath: the output file path
    :param numberOfCase: the number of examples
    :return:
    """
    with open(filePath, "w+", encoding='utf-8') as f:
        degree = 0.0
        for i in range(len(tweets)):
            info = {}
            graph_node_size = graph_scale
            edge_prob = 0.3

            while True:
                edge_count = 0.0
                
                graph = create_graph(tweets[i])
                #graph = nx.DiGraph()
                #for i in range(graph_node_size):
                 #   nodes = graph.nodes()
                  #  if len(nodes) == 0:
                   #     graph.add_node(i)
                    #else:
                     #   size = random.randint(1, min(i, 2));
                      #  fathers = random.sample(range(0, i), size)
                       # for father in fathers:
                        #    graph.add_edge(father, i)
                            
                for id in graph.edges:
                    edge_count += len(graph.edges[id])
                start = 0
                nodes = list(graph.nodes)
                end = len(graph.nodes)-1
                nx.draw(graph,with_labels=True,pos=nx.spring_layout(graph),nodecolor='r', edge_color='b')
                path = nx.shortest_path(graph, nodes[0], nodes[len(graph.nodes)-1])
                paths = [p for p in nx.all_shortest_paths(graph, nodes[0], nodes[len(graph.nodes)-1])]
                if len(path) >= 3 and len(paths) == 1:
                    degree += edge_count / len(graph.nodes)
                    break


            adj_list = []
            for adj in graph.adjacency():
                adj_list.append(list(adj[1].keys()))
                
            #print(adj_list[0])

            g_ids = {}
            g_ids_features = {}
            g_adj = {}
            print(graph_node_size,start,end)
            for i in range(end):
                g_ids[nodes[i]] = i
                if i == start:
                    g_ids_features[nodes[i]] = "START"
                elif i == end:
                    g_ids_features[nodes[i]] = "END"
                else:
                     g_ids_features[nodes[i]] = str(i+10)
                    #g_ids_features[nodes[i]] = str(random.randint(1, 15))
                g_adj[i] = adj_list[i]

            # print start, end, path
            text = ""
            for id in range(len(path)):
                text += g_ids_features[nodes[id]] + " "

            info["seq"] = text.strip() +" END"
            info["g_ids"] = g_ids
            info['g_ids_features'] = g_ids_features
            info['g_adj'] = g_adj
            f.write((json.dumps(info,ensure_ascii=False)+"\n"))

        #print("average degree in the graph is :{}".format(degree/numberOfCase))


if __name__ == "__main__":
    tweets = read_data_from_database()
    create_random_graph(tweets, "train.data", graph_scale=10)
    create_random_graph(tweets, "train.data", graph_scale=10)
    create_random_graph(tweets, "train.data", graph_scale=10)


