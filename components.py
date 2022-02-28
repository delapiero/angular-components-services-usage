import os
import string

services = {}
components = {}
selectors = {}

def find(file, prefix, suffix):
    with open(file, encoding="utf8") as f:
        for line in f.readlines():
            if (prefix in line):
                start = line.find(prefix) + len(prefix)
                end = line.find(suffix, start)
                name = line[start:end]
                return name.strip()

for path, dirs, files in os.walk("./src/app"):
    for file in files:
        fullpath = os.path.join(path, file)
        if file.endswith("service.ts"):
            serviceName = find(fullpath, 'export class ',' ')
            services[serviceName] = fullpath
        if file.endswith("component.ts"):
            componentName = find(fullpath, 'export class ',' ')
            components[componentName] = fullpath
            selectorName = find (fullpath, 'selector:',',')
            selectorName.strip('\'')
            selectors[componentName] = selectorName

usage = {}

def test_usage(file, content, dict):
    items = dict.items()
    for item in items:
        if item[0] in content:
            if item[1] != file:
                add_usage(item[0], 1)
            else:
                add_usage(item[0], 0)

def add_usage(item, count):
    if item in usage:
        usage[item] = usage[item] + count
    else:
        usage[item] = count

for path, dirs, files in os.walk("./src/app"):
    for file in files:
        fullpath = os.path.join(path, file)
        if file.endswith('.ts'):
            with open(fullpath, encoding="utf8") as f:
                content = f.read()
                test_usage(fullpath, content, services)
                test_usage(fullpath, content, components)
        elif file.endswith('.html'):
            with open(fullpath, encoding="utf8") as f:
                content = f.read()
                selectors_items = selectors.items()
                for item in selectors_items:
                    if item[1] in content:
                        selector_file = components[item[0]]
                        if selector_file != fullpath:
                            add_usage(item[0])

print('ALL:')
usage_items = usage.items()
for item in usage_items:
    print(item)

unused = 0
print('UNUSED:')
for item in usage_items:
    if item[1] < 1:
        unused = unused + 1
        print(item)
if unused == 0:
    print("NONE")
input("Press Enter to continue...")
