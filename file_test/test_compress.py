import pyminizip
compression_level = 5
pyminizip.compress("total.pickle", "test.zip", "123456", compression_level)
pyminizip.compress("test.zip", "final.zip", "123456", compression_level)
