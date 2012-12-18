from occupy import Command, File

def main():
    yield Command("echo hi")
    yield File("asdf")
