class AerospikePredicatesMock(object):
    def between(self, bin, min, max):
        def filt(results):
            return list(filter(lambda x: min < x[2][bin] < max, results))

        return filt

    def equals(self, bin, val):
        def filt(results):
            return list(filter(lambda x: x[2][bin] == val, results))

        return filt

    def contains(self, bin, index_type, val):
        def filt(results):
            return list(filter(lambda x: val in x[2][bin], results))

        return filt

    def range(self, bin, index_type, min, max):
        def filt(results):
            return list(
                filter(lambda x: [y for y in x[2][bin] if min < y < max],
                       results))

        return filt
