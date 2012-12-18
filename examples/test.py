from occupy import Command, File

def collection(path1, path2):
    yield File(path1)
    yield File(path2)


def main():
    yield Command("echo hi")
    yield File("/tmp/asdf")
    yield collection(path1="/tmp/file1", path2="/tmp/file2")
