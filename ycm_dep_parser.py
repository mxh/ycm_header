import os
import sys
import re

def parse_dep_file(filename):
    f = open(filename, 'r')
    lines = [line.rstrip() for line in f.readlines()]
    lines = "".join(lines)
    lines = lines.replace(" \\ ", " ")
    cpp_file = re.search(r"cpp.o: (.*?) ", lines).group(1)
    dependencies = lines.split(" ")[2:]

    return (cpp_file, dependencies)

def find_d_files(directory):
    d_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if os.path.splitext(filename)[1] == ".d":
                d_files.append(os.path.join(root, filename))
    return d_files

def convert_deps_to_queue(deps):
    queue = {}
    for dep in deps:
        cpp = dep[0]
        cpp_deps = dep[1]
        for cpp_dep in cpp_deps:
            queue[cpp_dep] = queue.get(cpp_dep, []) + [((cpp, len(cpp_deps)))]

    # sort by number of dependencies
    sorted_queue = {}
    for dep, cpp_list in queue.iteritems():
        sorted_cpp_list = sorted(cpp_list, key=lambda cpp: cpp[1])
        sorted_queue[dep] = sorted_cpp_list[0][0]
        
    return sorted_queue

if __name__=="__main__":
    directory = sys.argv[1]
    out_file = sys.argv[2]
    d_files = find_d_files(directory)

    deps = [parse_dep_file(f) for f in d_files]
    queue = convert_deps_to_queue(deps)

    f = open(out_file, 'w')
    for file, dep in queue.iteritems():
        f.write("{0} {1}\n".format(file, dep))
