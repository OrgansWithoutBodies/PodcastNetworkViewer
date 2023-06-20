import holoviews as hv
from holoviews import opts 
import pandas as pd
import networkx as nx
import itertools
#https://examples.pyviz.org/network_packets/network_packets.html
#https://www.python-course.eu/networkx.php

hv.extension('bokeh')
def catnetwork(nodes,edges,hvopts=dict()):
	allcats=list(itertools.chain.from_iterable([[n,*list(nodes[n])] for n in nodes.keys()]))
	print(allcats)
	catdict={value:c for c,value in enumerate(allcats)}
	edges=list(itertools.chain.from_iterable([[[catdict[n],catdict[m]] for m in nodes[n]] for n in nodes.keys()]))
	print(edges)
	G=nx.Graph()
	G.add_nodes_from(catdict.values())
	G.add_edges_from(edges)
	#circular_layout,spring_layout,planar_layout,random_layout,spectral_layout

def podappearancenetwork(nodes,edges,hvopts=dict()):
	#[0].content [1].ep.cont
	appdict=nodes
	pods=[p.name for p in appdict.keys()]
	# edges=[]
	# edgedict=dict()
	# for p in appdict.keys():
	# 	print(len(appdict[p][0]))
	# 	print(appdict[p][0][0])


# @TODO - able to handle pods where someone is both a guest & a host (ie on-boarded as host)
	G=nx.Graph()
	G.add_nodes_from(pods)
	for e in edges:
		G.add_edges_from(e[0],label=e[1]['color'])
	return G
def personappearancenetwork(appdict,hvopts=dict()):
	pass#if person__

def networkView(nodes,edges,genfn):
	G=genfn(nodes,edges)
	# [print(len(n)) for n in nodes]
	hvgraph=hv.Graph.from_networkx(G,nx.spring_layout)
	# hvgraph.opts(tools=['hover'])

	# setattr(hvgraph,'default_tools',['pan'])
	setattr(hvgraph,'directed',True)
	labels=hv.Labels(hvgraph.nodes,['x','y'],'index')

	# labels.opts
	# print(edges)
	renderer=hv.renderer('bokeh')
	
	return renderer.static_html(hvgraph*labels)

"""
vizes:
	nodes - pods, edges - {share a host,share a guest, share an appearance}
	nodes - people, edges - {have appeared on same pod, have appeared on same ep}
	# nodes - 
"""
