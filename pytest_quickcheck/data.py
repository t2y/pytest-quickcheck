from pytest_quickcheck.generator import Generator, get_int


class listof(Generator):
    def __init__(self, data, **options):
        self.data = data
        self.min_num = options.pop("min_num", 0)
        assert self.min_num >= 0
        self.max_num = options.pop("max_num", 20)
        self.options = options

    def generate(self, **kwargs):
        kwargs.update(self.options)
        k = get_int(self.min_num, self.max_num)
        return [self.generate_data(self.data, **kwargs) for _ in range(k)]


def listof1(data, **options):
    options.setdefault("min_num", 1)
    return listof(data, **options)
