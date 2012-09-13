from occupy import File

class skeleton(object):
    File("/log",
         ensure='directory',
         mode=0755,
         replace=False)
