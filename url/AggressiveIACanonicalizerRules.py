from .CanonicalizeRules import CanonicalizeRules
from .CanonicalizerConstants import CanonicalizerConstants as consts

class AggressiveIACanonicalizerRules(CanonicalizeRules):
    def __init__(self, strip_splash = True):
        self.set_rule(consts.SCHEME_SETTINGS, consts.SCHEME_LOWERCASE)
        self.set_rule(consts.HOST_SETTINGS, consts.HOST_LOWERCASE|consts.HOST_MASSAGE)
        self.set_rule(consts.PORT_SETTINGS, consts.PORT_STRIP_DEFAULT)

        path_settings = consts.PATH_LOWERCASE | consts.PATH_STRIP_SESSION_ID

        if strip_splash:
            path_settings |= consts.PATH_STRIP_TRAILING_SLASH_UNLESS_EMPTY

        self.set_rule(consts.PATH_SETTINGS, path_settings)
        self.set_rule(consts.QUERY_SETTINGS, consts.QUERY_LOWERCASE| consts.QUERY_STRIP_SESSION_ID| consts.QUERY_STRIP_EMPTY| consts.QUERY_ALPHA_REORDER)
        self.set_rule(consts.HASH_SETTINGS, consts.HASH_STRIP)
        self.set_rule(consts.AUTH_SETTINGS, consts.AUTH_STRIP_PASS | consts.AUTH_STRIP_USER)
        