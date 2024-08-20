import os
import re
import yaml

pattern = r'revision="([a-f0-9]{40})"'
pattern2 = r'^tools/run-tests\.py.*$'
pattern3 = r'^SUMMARY: ThreadSanitizer:.*$'
tests = {}

for f in os.listdir("logs"):
    log = open(f"logs/{f}").read()
    match = re.search(pattern, log)
    if match:
        commit = match.group(1)
    else:
        print(f"No commit found when parsing {f}")

    cmds = re.findall(pattern2, log, re.MULTILINE)
    if len(cmds) != 1:
        print(f)
    assert(len(cmds) == 1)
    cmd = cmds[0]

    races = list(set(re.findall(pattern3, log, re.MULTILINE)))
    for race in races:
        if commit not in tests.keys():
            tests[commit] = { cmd: [race] }
        else:
            if cmd not in tests[commit].keys():
                tests[commit][cmd] = [race]
            else:
                tests[commit][cmd].append(race)

# print(tests)
print("Num commits:", len(tests.keys()))
# print(list(tests.keys()))

yaml.dump(tests, open("races.yaml", "w"))