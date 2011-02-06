#!/usr/bin/env python
# eval.py
# -------
# the clustering evaluation script that use multiplicity B-cubed for overlapping clusters.
# 
# Usage:
# 	./eval.py gold_standard test_set
# 		gold_standard and test_set are both cluster files.
# 		The B-cubed scores are evaluated for test_set against gold_standard.
# 		The scores are commutative, which means you will get the same scores
# 		if you exchange the test set and the gold standard.
# 
# Input:
# 	cluster files has the following format.
# 
# 	The title of an article is listed per line, and each cluster is divided by a blank line.
# 	The first article of each cluster may be the centroid article of the cluster.
# 	Comments followed by a hash (#) sign are allowed either at the beginning or end of a line.
# 
# 	An example cluster file follows:
# 	# Excitement about the upcoming superbowl.  Played on February 1, 2009.
# 	Super_Bowl_XLIII
# 	Super_Bowl
# 	Arizona_Cardinals
# 	Kurt_Warner
# 
# 	# The US airways flight that ditched into the Hudson, with no casualties 
# 	US_Airways_Flight_1549
# 	Chesley_Sullenberger
# 	Hudson_River
# 	Airbus_A320_family

import sys

gold_file = "/Users/bahn/work/wikitopics/data/clustering/clusters-ccb/pick0127.clusters-ccb"
clustering = "/Users/bahn/work/wikitopics/data/clustering/clusters-bahn/cluster0127.txt"

if sys.argv > 1:
    if len(sys.argv) == 3:
        gold_file = sys.argv[1]
        clustering = sys.argv[2]
    else:
        print 'Invalid arguments:', sys.argv
        sys.exit(1)

label = {}
cluster = {}

def read_clusters(filename, bag):
    f = open(filename, 'r')
    numClusters = 0
    numInstances = 0
    for line in f:
        if (line.find('#') != -1): # eliminates comments
            line = line[:line.find('#')].strip()
        tokens = line.split(None, 1)
        if len(tokens) == 0:
            if numInstances:
                numClusters += 1
                numInstances = 0
        else:
            topic = tokens[0].strip()
            if not topic in bag:
                bag[topic] = set()
            bag[topic].add(numClusters)
            numInstances += 1
    if numInstances:
        numClusters += 1
        numInstances = 0
    return numClusters
    
print "gold standard:", gold_file
print "clustering:", clustering
ret = read_clusters(gold_file, label)
print "clusters of gold standard:", ret
ret = read_clusters(clustering, cluster)
print "clusters of test set:", ret
del ret

keys = label.keys()
for key in keys:
    if not key in cluster:
        print key, 'is missing in cluster'
        sys.exit(0)

for key in cluster.keys():
    if not key in label:
        print key, 'is missing in label'
        sys.exit(0)

precision = 0.0
recall = 0.0
noprecision = 0
norecall = 0

for i, e in enumerate(keys):
    mulprec = 0.0
    mulrec = 0.0
    nomulprec = 0
    nomulrec = 0
    for i2, e2 in enumerate(keys):
        if i == i2:
            continue
        labelintersection = len(label[e] & label[e2])
        clusterintersection = len(cluster[e] & cluster[e2])
        less = min(labelintersection, clusterintersection)
        if clusterintersection > 0:
            mulprec += float(less) / float(clusterintersection)
            nomulprec += 1
        if labelintersection > 0:
            mulrec += float(less) / float(labelintersection)
            nomulrec += 1
    if nomulprec > 0:
        precision += mulprec / float(nomulprec)
        noprecision += 1
    if nomulrec > 0:
        recall += mulrec / float(nomulrec)
        norecall += 1
if noprecision > 0:
    precision /= float(noprecision)
if norecall > 0:
    recall /= float(norecall)

fscore = 2*precision*recall / (precision + recall)
print "Multiplicity BCubed precision: %.4f" % (precision)
print "Multiplicity BCubed recall:    %.4f" % (recall)
print "Multiplicity BCubed F-score:   %.4f" % (fscore)