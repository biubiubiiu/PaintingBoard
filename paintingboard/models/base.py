import copy


class BaseState(object):

    def copy(self, **kwargs):
        ret = copy.deepcopy(self)
        for k, v in kwargs.items():
            ret.__setattr__(k, v)
        return ret
