cdef extern from "stdio.h":
    cdef struct FILE:
        pass

    ctypedef FILE FILE

    FILE *fopen(const char *filename, const char *mode)

    int fclose(FILE *fp)

cdef extern from "indexer/index.h":
  char * read_from_index(FILE *source_file, FILE *index_file, long desired_line, Py_ssize_t* length)
  int make_index_from_file(char *source_file, char *target_file, int visual)
