//
//  python_wrapper.c
//  LRUAnalyzer
//
//  Created by Juncheng on 5/26/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//

#include <Python.h>
#include "heatmap.h"
#include "cache.h"
//#include "FIFO.h" 
//#include "Optimal.h"


#define NPY_NO_DEPRECATED_API 11
#include <numpy/arrayobject.h>


/* TODO: 
not urgent, not necessary: change this profiler module into a python object,
    this is not necessary for now because we are not going to expose this level API 
    to user, instead we wrap it with our python API, so these C functions are only 
    called inside mimircache  
*/


static PyObject* LRUProfiler_get_last_access_dist_seq(PyObject* self, PyObject* args, PyObject* keywds)
{   
    PyObject* po;
    READER* reader; 
    long begin=-1, end=-1; 
    static char *kwlist[] = {"reader", "begin", "end", NULL};

    // parse arguments
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "O|ll", kwlist, 
                                &po, &begin, &end)) {
        // currently specifying begin and ending position is not supported 
        return NULL;
    }
    if (!(reader = (READER*) PyCapsule_GetPointer(po, NULL))) {
        return NULL;
    }

    // get last access dist list  
    GSList* list = get_last_access_dist_seq(reader, read_one_element);

    // create numpy array 
    if (reader->total_num == -1)
        get_num_of_cache_lines(reader);
    long long size = reader->total_num;

    npy_intp dims[1] = { size };
    PyObject* ret_array = PyArray_SimpleNew(1, dims, NPY_INT); 
    GSList* gsl;
    long long counter = size-1;
    int* array = (int*) PyArray_GETPTR1((PyArrayObject *)ret_array, 0); 
    for (gsl=list; gsl!=NULL; gsl=gsl->next){
        array[counter--] = GPOINTER_TO_INT(gsl->data);
    }

    // memcpy(PyArray_DATA((PyArrayObject*)ret_array), hit_count, sizeof(long long)*(cache_size+3));
    g_slist_free(list); 

    return ret_array;
}


static PyObject* LRUProfiler_get_next_access_dist_seq(PyObject* self, PyObject* args, PyObject* keywds)
{
    PyObject* po;
    READER* reader;
    long begin=-1, end=-1;
    static char *kwlist[] = {"reader", "begin", "end", NULL};
    
    // parse arguments
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "O|ll", kwlist,
                                     &po, &begin, &end)) {
        // currently specifying begin and ending position is not supported
        return NULL;
    }
    if (!(reader = (READER*) PyCapsule_GetPointer(po, NULL))) {
        return NULL;
    }
    
    // get reversed last access dist list
    GSList* list = get_last_access_dist_seq(reader, read_one_element_above);
    
    // create numpy array
    if (reader->total_num == -1)
        get_num_of_cache_lines(reader);
    long long size = reader->total_num;
    
    npy_intp dims[1] = { size };
    PyObject* ret_array = PyArray_SimpleNew(1, dims, NPY_INT);
    GSList* gsl;
    long long counter = 0;
    int* array = (int*) PyArray_GETPTR1((PyArrayObject *)ret_array, 0);
    for (gsl=list; gsl!=NULL; gsl=gsl->next){
        array[counter++] = GPOINTER_TO_INT(gsl->data);
    }
        g_slist_free(list);
    
    return ret_array;
}

/*
static PyObject* generalProfiler_get_hit_rate_over_time(PyObject* self, PyObject* args, PyObject* keywds)
{
    PyObject* po;
    READER* reader;
    int num_of_threads = 4;
    long cache_size;
    int bin_size = -1;
    char* name;
    struct_cache* cache;
    
    //    long begin=-1, end=-1;
    static char *kwlist[] = {"reader", "cache_size", "cache_type", "bin_size", "num_of_threads", NULL};
    
    // parse arguments
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "Ols|ii", kwlist, &po, &cache_size, &name, &bin_size, &num_of_threads)) {
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
    return_res** results = profiler(reader, cache, num_of_threads, bin_size);
    
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

*/




static PyMethodDef c_heatmap_funcs[] = {
    {"get_last_access_dist", (PyCFunction)LRUProfiler_get_last_access_dist_seq,
        METH_VARARGS | METH_KEYWORDS, "get the distance to the last access time for each \
        request in the form of numpy array, -1 if haven't seen before"},
    {"get_next_access_dist", (PyCFunction)LRUProfiler_get_next_access_dist_seq,
        METH_VARARGS | METH_KEYWORDS, "get the distance to the next access time for each \
        request in the form of numpy array, -1 if it won't be accessed any more"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef c_heatmap_definition = { 
    PyModuleDef_HEAD_INIT,
    "c_heatmap",
    "A Python module that doing heatmap related computation",
    -1, 
    c_heatmap_funcs
};



PyMODINIT_FUNC PyInit_c_heatmap(void)
{
    Py_Initialize();
    import_array();
    return PyModule_Create(&c_heatmap_definition);
}

