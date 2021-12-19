import os
from collections import deque
import hashlib

gray = 0
black = 1


class Make:
    makefile_parsed = {}
    makefile = ""
    tasks = []

    def get_hash(self, fileName):
        with open(fileName.strip(), 'rb') as f:
            hsh = hashlib.sha1()
            while True:
                data = f.read(2048)
                if not data:
                    break
                hsh.update(data)
            rez = hsh.hexdigest()
            return rez

    def get_saved_data(self):
        try:
            hashs = []
            with open("saved_hash.txt") as file:
                for line in file:
                    hashs.append(line.strip())
                return hashs
        except:
            pass

    def save_data(self, hash):
        hashs = self.get_saved_data()
        if hashs and hash not in hashs:
            hashs.append(hash)
        with open("saved_hash.txt", 'w') as file:
            if not hashs:
                file.write(hash + "\n")
                return
            for s in hashs:
                file.write(s + "\n")

    def __init__(self, path_to_makefile: str):

        with open(path_to_makefile, "r") as f:
            self.makefile = f.read()

    def parse(self):
        lines = self.makefile.split('\n')
        lines = [i for i in lines if i]  # removing empty items
        ans = {}
        for x in lines:
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
                tmp = cmd.split('cat')
                if len(tmp) > 1:
                    file_name = tmp[1].strip().split(' ', 1)[0]
                    if self.get_saved_data() and self.get_hash(file_name) in self.get_saved_data():
                        return
                    self.save_data(self.get_hash(file_name))
                os.system(cmd)


a = Make("text")
a.parse()
a.sort()
a.run()

b = Make("makefile2")
b.parse()
b.sort()
b.run()
