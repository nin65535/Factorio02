# coding: utf-8
import json
import numpy as np
import random
import pandas as pd
from Facilities import Facilities as FC

class Field(object):

    @classmethod
    def init(cls):
        cls.conf = json.load(open('fields.json','r'))
        cls.size = cls.conf['size']
        cls.rand_area_max = [int((cls.size[0] + 1) / 2),int((cls.size[1] + 1) / 2)]

    def __init__(self,cells=None):
        if cells is None:
            cells = Field.random()
        self.cells = cells
        self._score = None

    @classmethod 
    def random(cls):
        fc = FC.get()

        cells = np.zeros(cls.size , np.int8)
        for y in range(cls.size[1]):
            f_name = cls.conf['fix'].get(str(y))
            if f_name:
                cells[0][y] = fc.names.index(f_name)

        for f_name,count in cls.conf['free'].items():
            samples = random.sample(list(np.transpose(np.where(cells[1:] == 0))) , count)
            for x,y in samples:
                cells[x + 1][y] = fc.names.index(f_name)

        return cells

    def print(self):
        names = FC.get().names
        named_cells = np.vectorize(lambda f_id: names[f_id])(self.cells)
        df = pd.DataFrame(named_cells)
        print(df)
        print(self.score)

    @property
    def score(self):
        if(self._score):
            return self._score

        self._score = 0

        fc = FC.get()
        lines = np.zeros(len(fc.materials),np.int8)

        for m_id in range(len(fc.materials)):
            map = fc.map[:,m_id]
            points = np.where(np.vectorize(lambda f_id:map[f_id])(self.cells))
            lines[m_id] = max(points[0]) - min(points[0]) + max(points[1]) - min(points[1])

        self._score -= sum(lines)

        ADJOIN_POINT = 0.1

        for l in self.cells:
            self._score += Field.count_adjoin(l) * ADJOIN_POINT

        for r in np.transpose(self.cells):
            self._score += Field.count_adjoin(r) * ADJOIN_POINT

        return self._score

    #0以外の値が連続していたら＋１
    @staticmethod
    def count_adjoin(l):
        l3 = ((l[1:] - l[:-1]) == 0)
        l2 = (l[1:] != 0)
        return sum(l2 * l3)

    def swap(self,a,b):
        temp = self.cells[a]
        self.cells[a] = self.cells[b]
        self.cells[b] = temp

    def find(self,f_id):
        pos = random.choice(np.transpose(np.where(self.cells[1:] == f_id)))
        pos += [1,0]
        return tuple(pos)

    def mutate(self):
        m = random.choice([Field.slide_up , Field.slide_down , Field.slide_left , Field.slide_right])
        self.cells[1:] = m(self.cells[1:])    
    
    @staticmethod
    def slide_up(cells):
        return np.roll(cells, -Field.size[1])

    @staticmethod
    def slide_down(cells):
        return np.roll(cells, Field.size[1])

    @staticmethod
    def slide_right(cells):
        cells = np.roll(cells,1)
        cells[:,0] = np.roll(cells[:,0] , -1)
        return cells

    @staticmethod
    def slide_left(cells):
        cells = np.roll(cells,-1)
        cells[:,-1] = np.roll(cells[:,-1] , 1)
        return cells

    @classmethod
    def get_random_area(cls):
        size = (random.randint(1,cls.rand_area_max[0]),random.randint(1,cls.rand_area_max[1]))
        pos = [random.randint(0,cls.size[0] - size[0]),random.randint(0,cls.size[1] - size[1])]

        area = [(x,y) for x in range(pos[0] , pos[0] + size[0]) for y in range(pos[1] , pos[1] + size[1])]

        return area
    @classmethod
    def cross(cls,p1,p2,area):
        cells = p1.cells.copy()
        
        child = Field(cells)

        for pos1 in area:
            value = p2.cells[pos1]
            if value != child.cells[pos1]:
                pos2 = child.find(value)
                child.swap(pos1,pos2)

        return child
