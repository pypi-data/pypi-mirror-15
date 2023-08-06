cimport indexer
cimport libc.stdio


cdef class IndexedFile(object):
    """A file which reads the source_file"""
    cdef FILE* source_file
    cdef FILE* index_file
    cdef int counter
    def __init__(self, source_file_name, index_file_name):
        self.source_file = fopen(source_file_name, "rb")
        self.index_file = fopen(index_file_name, "rb")
        self.counter = 0;

    def __iter__(self):
      return  self

    def __next__(self):
      cdef Py_ssize_t length = 0
      r = read_from_index(self.source_file, self.index_file, self.counter, &length)
      if r :
        self.counter += 1
        return r
        
      else:
        return StopIteration


    def read(self, line_number):
        cdef Py_ssize_t length = 0
        cdef char* c_string = read_from_index(self.source_file, self.index_file, line_number, &length)       
        cdef bytes py_string = c_string
        return py_string.strip()

    def close(self):
        fclose(self.source_file)
        fclose(self.index_file)

class Indexer(object):
    """Loads up indexer"""
    def __init__(self, source_file_name, index_file_name):
        self.source_file_name = source_file_name
        self.index_file_name = index_file_name

    def make_index(self):
        make_index_from_file(self.source_file_name, self.index_file_name, 0)

    def __enter__(self):
        self.if_object = IndexedFile(self.source_file_name, self.index_file_name)
        return self.if_object

    def __exit__(self, type, value, traceback):
        self.if_object.close()
