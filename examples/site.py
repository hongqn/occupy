from occupy import node, modules as M

def basenode():
    yield M.skeleton


@node('dae-dev.intra.douban.com', basenode)
def dae_dev():
    yield M.dae.node.dev_node
