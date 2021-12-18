import os
from collections import deque
import hashlib

gray = 0
black = 1


class Make:
    makefile_parsed = {}
    makefile = ""
    tasks = []

    def __init__(self, path_to_makefile: str):
        with open(path_to_makefile, "r") as f:
            self.makefile = f.read()

    def parse(self):
        b = self.makefile.split('\n')
        b = [b for b in b if b]
        ans = {}
        f = 0
        for x in b:
            if ':' in x:
                g = x.split()

                target = g[0][:-1]

                dependency = g[1:]
                ans[target] = {'depends': dependency, 'doing': []}
            else:
                ans[target]['doing'].append(x.strip())

        self.makefile_parsed = ans

    def sort(self):
        graph = {x: self.makefile_parsed[x]["depends"] for x in self.makefile_parsed}

        order, enter, state = deque(), set(graph), {}

        def dfs(node):
            state[node] = gray
            for k in graph.get(node, ()):
                sk = state.get(k, None)
                if sk == gray:
                    raise ValueError("cycle")
                if sk == black:
                    continue
                enter.discard(k)
                dfs(k)
            order.appendleft(node)
            state[node] = black

        while enter:
            dfs(enter.pop())
        self.tasks = list(order)[::-1]

    def run(self):
        for task in self.tasks:
            cmds = self.makefile_parsed[task]["doing"]

            for cmd in cmds:
                os.system(cmd)


def get_hash(fileName):
    with open(fileName, 'rb') as f:
        hsh = hashlib.sha1()
        while True:
            data = f.read(2048)
            if not data:
                break
            hsh.update(data)
        rez = hsh.hexdigest()
        return rez


def get_saved_data():
    try:
        with open("saved_hash.txt") as file:
            return file.read()
    except:
        pass


def save_data(hash):
    with open("saved_hash.txt", 'w') as file:
        file.write(hash)


a = Make("makefile1")
a.parse()
a.sort()
a.run()

if get_saved_data() != get_hash('civgraph.txt'):
    b = Make("makefile2")
    b.parse()
    b.sort()
    b.run()
save_data(get_hash('civgraph.txt'))
