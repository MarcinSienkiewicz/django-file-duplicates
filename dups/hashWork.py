from pathlib import Path
import hashlib


def getHash(path1, path2):
    def getData(givenPath):
        h = hashlib.sha256()
        size = 65536
        h_data = []
        for x in Path(givenPath).rglob("*"):
            if x.is_file():
                h = hashlib.sha256()
                with open(x, 'rb') as file:
                    while part := file.read(size):
                        h.update(part)
                h_data.append([str(x), h.hexdigest()])
        return h_data
    h1 = getData(path1)
    h2 = getData(path2)
    h2_proper = dict()

    for x in h2:
        if x[1] in h2_proper:
            h2_proper[x[1]].append(x[0])
        else:
            h2_proper[x[1]] = []
            h2_proper[x[1]].append(x[0])

    h1_result = dict()
    for x in h1:
        if x[1] not in h2_proper:
            continue
        else:
            h1_result[x[0]] = h2_proper.get(x[1])
    return h1_result
