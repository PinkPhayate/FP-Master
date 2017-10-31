class EXP_MODEL(object):
    sw_name = None
    final_version = None
    bug_versions = None
    pre_version = None
    curr_version = None
    dir_name = None

    def __init__(self, sw, fv, bvs, pv, cv, dn):
        self.sw_name = sw
        self.final_version = fv
        self.bug_versions = bvs
        self.pre_version = pv
        self.curr_version = cv
        self.dir_name = dn
