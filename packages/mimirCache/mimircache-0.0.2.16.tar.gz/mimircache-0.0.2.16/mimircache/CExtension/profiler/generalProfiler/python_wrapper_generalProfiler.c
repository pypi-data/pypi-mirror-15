//
//  python_wrapper.c
//  LRUAnalyzer
//
//  Created by Juncheng on 5/26/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//

#include <Python.h>
#include "generalProfiler.h"

#define NPY_NO_DEPRECATED_API 11
#include <numpy/arrayobject.h>
#include "FIFO.h"
#include "Optimal.h"


/* TODO:
 not urgent, not necessary: change this profiler module into a pyhton object,
 this is not necessary for now because we are not going to expose this level API
 to user, instead we wrap it with our python API, so these C functions are only
 called inside mimircache
 */


static PyObject* generalProfiler_get_hit_rate(PyObject* self, PyObject* args, PyObject* keywds)
{
    PyObject* po;
    READER* reader;
    int num_of_threads = 4;
    long cache_size;
    int bin_size = -1;
    char* name;
    struct_cache* cache;
    
    long begin=0, end=-1;
    static char *kwlist[] = {"reader", "cache_size", "cache_type", "bin_size", "num_of_threads", NULL};
    
    // parse arguments
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "Ols|iill", kwlist, &po, &cache_size, &name, &bin_size, &num_of_threads, &begin, &end)) {
        printf("parsing argument failed in generalProfiler_get_hit_rate\n");
        return NULL;
    }
//    printf("bin size: %ld, threads: %d\n", bin_size, num_of_threads);
    
    if (!(reader = (READER*) PyCapsule_GetPointer(po, NULL))) {
        return NULL;
    }
    if (bin_size == -1)
        bin_size = (int)(cache_size/100);
    
    // build cache
    char data_type = reader->type;
    
    if (strcmp(name, "FIFO") == 0){
        cache = fifo_init(cache_size, data_type, NULL);

    }
    else if (strcmp(name, "Optimal") == 0){
        struct optimal_init_params init_params = {.reader=reader, .next_access=NULL};
        cache = optimal_init(cache_size, data_type, (void*)&init_params);
    }
    else {
        printf("does not support given cache replacement algorithm: %s\n", name);
        exit(1);
    }
    
    // get hit rate
    return_res** results = profiler(reader, cache, num_of_threads, bin_size, (gint64)begin, (gint64)end);

    // create numpy array
    long num_of_bins = cache_size/bin_size;
    
    if (num_of_bins * bin_size < cache_size)
        num_of_bins ++;                         // this happens when size is not a multiple of bin_size

    if (cache_size == -1)
        cache_size = reader->total_num;
    
//    npy_intp dims[2] = { 2, num_of_bins };
//    PyObject* ret_array = PyArray_SimpleNew(2, dims, NPY_FLOAT);
//    int* array = (float*) PyArray_GETPTR1((PyArrayObject *)ret_array, 0);
//    int* array = (float*) PyArray_GETPTR1((PyArrayObject *)ret_array, 0);

    
    PyObject *d = PyDict_New();
    
    
    int i;
    for (i=0; i<num_of_bins; i++){
        PyDict_SetItem(d, Py_BuildValue("l", (i+1)*bin_size), Py_BuildValue("f", results[i]->hit_rate));
        free(results[i]);
    }
    
    free(results);
    cache->destroy(cache);
    return d;
}





static PyMethodDef c_generalProfiler_funcs[] = {
    {"get_hit_rate", (PyCFunction)generalProfiler_get_hit_rate,
        METH_VARARGS | METH_KEYWORDS, "get hit rate dict"},
//    {"get_hit_rate_seq", (PyCFunction)LRUProfiler_get_hit_rate_seq,
//        METH_VARARGS | METH_KEYWORDS, "get hit rate array in the form of numpy array, \
//        the last one is cold miss, the second to last is out of cache_size"},
//    {"get_miss_rate_seq", (PyCFunction)LRUProfiler_get_miss_rate_seq,
//        METH_VARARGS | METH_KEYWORDS, "get miss rate array in the form of numpy array, \
//        the last one is cold miss, the second to last is out of cache_size"},
//    {"get_reversed_reuse_dist", (PyCFunction)LRUProfiler_get_reversed_reuse_dist,
//        METH_VARARGS | METH_KEYWORDS, "get reuse distance array of the reversed trace file in the form of numpy array"},
//    {"get_reuse_dist_seq", (PyCFunction)LRUProfiler_get_reuse_dist_seq,
//        METH_VARARGS | METH_KEYWORDS, "get reuse distance array in the form of numpy array"},
//    
//    {"get_rd_distribution_seq", (PyCFunction)LRUProfiler_get_rd_distribution_seq,
//        METH_VARARGS | METH_KEYWORDS, "get reuse distance distribution in the form of numpy array"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef c_generalProfiler_definition = {
    PyModuleDef_HEAD_INIT,
    "c_generalProfiler",
    "A Python module that doing profiling with regards to all kinds of caches",
    -1,
    c_generalProfiler_funcs
};



PyMODINIT_FUNC PyInit_c_generalProfiler(void)
{
    Py_Initialize();
    import_array();
    return PyModule_Create(&c_generalProfiler_definition);
}

