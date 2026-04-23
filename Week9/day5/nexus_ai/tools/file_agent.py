import csv


def read_csv(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path, data):
    with open(path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def read_txt(path):
    with open(path) as f:
        return f.read()


def write_txt(path, content):
    with open(path, "w") as f:
        f.write(content)

def write_md(filename, content):
    with open(filename, "w") as f:
        f.write(content)