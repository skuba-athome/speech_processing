__author__ = 'Frank'
import csv
from graphviz import Digraph
import sys, os

class Node:

    def __init__(self, parent, item):
        # print item
        self.parent = parent
        self.item =item
        self.children = []
        # self.id = "%s"%item
        self.id = "%s[%d]"%(item, items.count(item))
        items.append(item)
        self.command = ""


    def add(self, list):
        if len(list) is 0:
            return
        checking = True
        for child in self.children:
            if child.item == list[0]:
                child.add(list[1:])
                checking = False
                break
        if checking:
            new_node = Node(self,list[0])
            self.children.append(new_node)
            new_node.add(list[1:])

    def draw(self, graph):
        for child in self.children:
            graph.edge("%s [%d]"%(self.id,len(self.children)), "%s [%d]"%(child.id,len(child.children)))
            child.draw(graph)
            # print  data
    def generator_command(self):
        if len(self.children) > 1:
            public_command.append("(")
            level.append(0)
        else:
            level[-1] += 1
        for child in self.children:
            public_command.append(child.command)
            # encode_public_command.append(generator_name())
            if len(child.children) == 0 and len(self.children) > 1:
                public_command.append("|")
                # encode_public_command.append(generator_name())
                # if len(level) == 2:
                #     public_command.append("\n                    ")
            if len(child.children) > 0:
                child.generator_command()
            if len(child.children) > 1:
                public_command.append("|")
                # print level
                # if len(level) == 2:
                #     public_command.append("\n                    ")
            if len(self.children) > 1 and self.children.index(child) == len(self.children) - 1 and public_command[-1] == "|":
                public_command.pop()
        if len(self.children) > 1:
            public_command.append(")")
            level.pop()

    def encode_command(self):
        command = ""
        # for child in self.children:
        #     if len(child.children) == 0:
        #         return child.item
        #     command += child.encode_command() + " "
        # return command
        for child in self.children:
            command += child.encode_command() + " "
        # print self.item
        if len(self.children) <= 1:
            command = self.item + " " +command
        if len(self.children) > 1:
            return ""
            # variables[generator_name()] = command
        # elif len(self.children) == 1:
        #     command = self.item + " " + command
        print command
        return command

    def upgrade(self):
        if self.parent != None and len(self.children) == 1:
            del_list = [self.children[0]]
            add_list = []
            for child in del_list:
                add_list += child.children
            for i in del_list:
                self.item += " " + i.item
                self.id = self.item + self.id[self.id.index("["):]
                self.children.remove(i)
            for i in add_list:
                self.children.append(i)
            self.upgrade()
        for child in self.children:
            child.upgrade()

    def upgrade2(self):
        # print self.children
        if self.parent != None and len(self.children) > 1:
            if all([len(child.children) == 0 for child in self.children]):
                del_list = self.children[1:]
                self.children[0].item = "( " + self.children[0].item
                for child in del_list:
                    self.children[0].item += " | " + child.item
                    self.children[0].id = self.children[0].item + self.children[0].id[self.children[0].id.index("["):]
                    self.children.remove(child)
                self.children[0].item += " )"
        for child in self.children:
            # print child.item
            child.upgrade2()


    def generator_command_name(self):
        count.append(0)
        for child in self.children:
            child.command = generator_name()
            variables[child.command] = child.item
            child.generator_command_name()
        count.pop()



items = []
def create_tree(file_path):
    data =  csv.reader(open(file_path))
    # print data
    # items = []
    root = Node(None, 'root')
    for line in data:
        root.add(line)
    return root

def create_graph(root, path, name):
    graph = Digraph('fq_tree', filename= os.path.join(path,name),format='jpg')
    root.draw(graph)
    graph.render()

public_command = []
encode_public_command = []
variables = {}
level = [0]
def create_command(root, path, name):
    output_command = open(os.path.join(path,name), 'w')
    root.generator_command()
    print "public <commands> = ", " ".join(public_command), ';'

    public_command_output = filter(lambda i: i != "\n                    ", public_command)
    output_command.write("#JSGF V1.0;\n")
    output_command.write("grammar TEST;\n")
    output_command.write("public <commands> = " + " ".join(public_command_output)+";\n\n")
    # order = []
    for name in sorted(list(map(lambda i:map(int,i[9:-1].split("_")),variables))):
        # print "_".join(map(str,name))
        name = "<command_%s>"%("_".join(map(str,name)))
        output_command.write(name +" = "+ variables[name] + ";\n")


    # for name in sorted(variables):
    #     output_command.write(name +" = "+ variables[name] + ";\n")

    output_command.write("\n\n")
    output_command.write("/**\n")
    reader = csv.reader(open(sys.argv[1]))
    output_command.write("  * SENTENCES -- %d\n"%len(open(sys.argv[1]).readlines()))
    for line in reader:
        output_command.write("  * %5d %s\n"%(reader.line_num," ".join(line)))
    output_command.write("  */")
    output_command.close()


count = []
def generator_name():
    # name = "<command"
    # for i in level:
    #     name += "_" + str(i)
    # name += ">"
    # return name
    count[-1] += 1
    return  "<command_%s>"%("_".join(map(str,count)))


if __name__ == '__main__':

    root = create_tree(sys.argv[1])
    create_graph(root, sys.argv[2], "tree_before")


    root.upgrade()
    root.upgrade2()
    root.upgrade()
    root.generator_command_name()
    create_command(root, sys.argv[2], "command.jsgf")
    create_graph(root, sys.argv[2], "tree_after")

