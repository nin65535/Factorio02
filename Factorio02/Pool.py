import random
import sys
from Field import Field as fl

class Pool(object):

    def __init__(self):
        self.gen = 0
        self.pool = []
        self.results = [0,0,0,0]

    def generate(self):
        self.gen += 1

        while len(self.pool) < 2:
            self.pool.append(fl())

        parents = random.sample(self.pool , 2)

        self.pool.remove(parents[0])
        self.pool.remove(parents[1])

        area = fl.get_random_area()
        children = [fl.cross(parents[0] , parents[1] , area),fl.cross(parents[1] , parents[0] , area)]

        children[1].mutate()

        parents.sort(key=lambda x:x.score)
        children.sort(key=lambda x:x.score)

        if parents[1].score < children[0].score:
            self.results[0] +=1
            self.pool.append(parents[1])
            self.pool.append(children[0])
            self.pool.append(children[1])
            return

        if children[1].score < parents[0].score:
            self.results[1] +=1
            self.pool.append(parents[1])
            return

        if children[1].score < parents[1].score:
            self.results[2] +=1
            self.pool.append(parents[1])
            self.pool.append(children[1])
            return

        self.results[3] +=1
        self.pool.append(children[1])
        self.pool.append(fl())



    def run(self,goal):
        while self.gen < goal:
            self.generate()
            sys.stdout.write("gen: %04d    \r" % (self.gen) )
            sys.stdout.flush()

            if self.gen % 1000 == 0 :
                self.print()
        
        self.print()

    def print(self):
        self.pool.sort(key=lambda x:x.score)
        for f in self.pool:
            f.print()

        print(self.results)
