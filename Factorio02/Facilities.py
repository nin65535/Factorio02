from collections import OrderedDict as od
import numpy as np
import json
import pandas as pd

class Facilities(object):

    instance = None

    @classmethod
    def get(cls):
        if cls.instance is None:
            cls.instance = Facilities()
        return cls.instance

    def __init__(self):
        self.conf = json.load(open('facilities.json','r'))
        self.names = list(self.conf.keys())
        self.names.sort()
        self.names.insert(0,'None')

        self.materials = list(set(sum(self.conf.values(),[])))
        self.materials.sort()

        self.map = np.empty((len(self.names) , len(self.materials)),bool)

        for (f_id,f_name) in enumerate(self.names):
            if f_id:
                conf = self.conf.get(f_name)
                for (m_id,m_name) in enumerate(self.materials):
                    self.map[f_id][m_id] = m_name in conf
            else:
                self.map[f_id] = np.zeros(len(self.materials),bool)

    def print(self):
        df = pd.DataFrame(self.map, index=self.names, columns=self.materials)
        print(df)