def clamp(n, smallest, largest):
    """Clamp a value within [smallest] and [largest] inclusive"""
    return max(smallest, min(n, largest))


class Curry:
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs

        print(
            "Applying. F:{}. Args:{}, Kwargs:{}".format(
                self.fun,
                self.pending + args,
                kw,
            )
        )
        return self.fun(*(self.pending + args), **kw)
