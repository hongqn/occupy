from occupy import include, modules as M

def dev_node():
    yield M.portage.add_keywords(file="dae_dev_node")
    yield M.dae.node
