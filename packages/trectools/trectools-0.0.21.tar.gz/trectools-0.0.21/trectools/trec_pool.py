from trectools import TrecRun

# TODO: use logging properly
import logging
import os

# External libraries
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


'''
'''
class TrecPool:

    def __init__(self, pool):
        self.pool = pool

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Pool with %d topics. Total of %d unique documents."  % (len(self.pool), self.get_total_pool_size())

    def get_size_per_topic(self):
	return [len(k) for k in self.pool.values()]

    def get_total_pool_size(self):
	return np.sum(self.get_size_per_topic())

    def get_mean_pool_size(self):
	return np.mean(self.get_size_per_topic())

    def operate_pools(self, another_pool, operation, inplace=False):
	if self.pool.keys() != another_pool.pool.keys():
	    print "Error: Key set is different"
	    return None

	presult = {}
	for k in self.pool.keys():
	    sa = self.pool[k]
	    sb = another_pool.pool[k]
	    if operation == "minus":
		presult[k] = sa - sb
	    elif operation == "sum":
		presult[k] = sa.union(sb)
	    elif operation == "exclusive":
		presult[k] = sa ^ sb
	    else:
		print "Operation %s is not supported" % (str(operation))
	if inplace:
	    self.pool = presult
        else:
            return TrecPool(presult)

    def minus(self, another_pool, inplace=False):
        if inplace:
            self.operate_pools(self, another_pool, "minus", inplace)
        return self.operate_pools(self, another_pool, "minus", inplace)

    def plus(self, inplace=False):
	if inplace:
            self.operate_pools(self, another_pool, "sum", inplace)
        return self.operate_pools(self, another_pool, "sum", inplace)

    def check_size_minus(self, another_pool):
        return self.get_pool_size(self.minus(another_pool))

    def export_document_list(self, filename, with_format="relevation"):
        if with_format == "relevation":
            with open(filename, "w") as fout:
                for query, documents in sorted(self.pool.iteritems(), key=lambda x:x[0]):
                    for doc in sorted(documents):
                        fout.write("%s\tQ0\t%s\t0\t0\ttrectools\n" % (str(query), str(doc)))
        elif with_format == "filelist":
            documents = set([])
            for docs in self.pool.values():
                documents = documents.union(docs)

            with open(filename, "w") as fout:
                for doc in sorted(documents):
                    fout.write(doc + "\n")
        print "Created %s" % (filename)
