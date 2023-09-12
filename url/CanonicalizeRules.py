from CanonicalizerConstants import CanonicalizerConstants


class CanonicalizeRules:
    def __init__(self):
        self.settings = [0] * CanonicalizerConstants.NUM_SETTINGS

    def set_rule(self, rule, value):
        self.settings[rule] = value

    def get_rule(self, rule):
        return self.settings[rule]

    def is_set(self, rule, value):
        return (self.settings[rule] & value) == value