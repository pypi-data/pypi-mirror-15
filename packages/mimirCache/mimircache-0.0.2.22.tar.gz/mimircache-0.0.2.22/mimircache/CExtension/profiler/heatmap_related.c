#include "heatmap.h"

static inline int process_one_element_last_access(cache_line* cp, GHashTable* hash_table, long long ts);


GSList* get_last_access_dist_seq(READER* reader, void (*funcPtr)(READER*, cache_line*)){
    /*
    !!!!!! the list returned from this function is in reversed order!!!!!!
    */

    /* this function currently using int, may cause some problem when the 
    trace file is tooooooo large 
    */

    GSList* list= NULL; 

    if (reader->total_num == -1)
        get_num_of_cache_lines(reader);

    // create cache lize struct and initializa
    cache_line* cp = (cache_line*)malloc(sizeof(cache_line));
    cp->op = -1;
    cp->size = -1;
    cp->valid = TRUE;
            
    // create hashtable
    GHashTable * hash_table; 
    if (reader->type == 'v'){
        cp->type = 'l'; 
        hash_table = g_hash_table_new_full(g_int64_hash, g_int64_equal, \
                                            (GDestroyNotify)simple_key_value_destroyed, \
                                            (GDestroyNotify)simple_key_value_destroyed);
    }
    else{
        cp->type = 'c';
        hash_table = g_hash_table_new_full(g_str_hash, g_str_equal, \
                                            (GDestroyNotify)simple_key_value_destroyed, \
                                            (GDestroyNotify)simple_key_value_destroyed);
    }
    
    long long ts = 0;
    int dist; 

    if (funcPtr == read_one_element){
        read_one_element(reader, cp);
    }
    else if (funcPtr == read_one_element_above){
        reader_set_read_pos(reader, 1.0);
        go_back_one_line(reader);
        read_one_element(reader, cp);
    }
    else{
        fprintf(stderr, "unknown function pointer received in heatmap: get_last_access_dist_seq\n");
        exit(1);
    }
//    DEBUG(printf("after first reading\n");)
    while (cp->valid){
//        DEBUG(printf("read in %lld\n", ts);)
        dist = process_one_element_last_access(cp, hash_table, ts);
        list = g_slist_prepend(list, GINT_TO_POINTER(dist));
        funcPtr(reader, cp);
        ts++;
    }


    // clean up
    free(cp);
    g_hash_table_destroy(hash_table);
    reset_reader(reader);
    return list;
}




static inline int process_one_element_last_access(cache_line* cp, GHashTable* hash_table, long long ts){ 
    gpointer gp;
    if (cp->type == 'c') 
        gp = g_hash_table_lookup(hash_table, (gconstpointer)(cp->str_content));
    else if (cp->type == 'i')
        gp = g_hash_table_lookup(hash_table, (gconstpointer)(&(cp->int_content)));
    else if (cp->type == 'l')
        gp = g_hash_table_lookup(hash_table, (gconstpointer)(&(cp->long_content)));
    else{
        gp = NULL; 
        printf("unknown cache line type: %c\n", cp->type);
        exit(1);
    }
    int ret; 
    if (gp == NULL){
        // first time access
        ret = -1;
        long long *value = (long long*)malloc(sizeof(long long));
        if (value == NULL){
            printf("not enough memory\n");
            exit(1);
        }
        *value = ts;
        if (cp->type == 'c') 
            g_hash_table_insert(hash_table, g_strdup((gchar*)(cp->str_content)), (gpointer)value);
        
        else if (cp->type == 'l'){
            gint64* key = g_new(gint64, 1);
            // long *key = (long* )malloc(sizeof(uint64_t));
            if (key == NULL){
                printf("not enough memory\n");
                exit(1);
            }            
            *key = cp->long_content;
            g_hash_table_insert(hash_table, (gpointer)(key), (gpointer)value);            
        }
        else if (cp->type == 'i'){
            int *key = (int* )malloc(sizeof(int));
            if (key == NULL){
                printf("not enough memory\n");
                exit(1);
            }  
            *key = cp->int_content;
            g_hash_table_insert(hash_table, (gpointer)(key), (gpointer)value);            
        }
        else{
            printf("unknown cache line content type: %c\n", cp->type);
            exit(1);
        }
    }
    else{
        // not first time access
        long long old_ts = *(long long*)gp;
        ret = (int) (ts - old_ts); 
        *(long long*)gp = cp->ts;
    }
    return ret;
}


GArray* gen_breakpoints_virtualtime(READER* reader, int time_interval){
    /* 
     return a GArray of break points, not including the last break points 
     */
    
    if (reader->total_num == -1)
        get_num_of_cache_lines(reader);
    long i;
    guint array_size = (guint) (reader->total_num/time_interval) ;
    if ( reader->total_num % time_interval )
        array_size ++ ;
    GArray* break_points = g_array_sized_new(FALSE, FALSE, sizeof(guint64), array_size);
    for (i=0; i<array_size; i++){
        long long value = i * time_interval;
        g_array_append_val(break_points, value);
    }
    
    if (break_points->len > 10000)
        printf("%snumber of pixels in one dimension are more than 10000, exact size: %d, it may take a very long time, if you didn't intend to do it, please try with a larger time stamp", KRED, break_points->len);
    else if (break_points->len < 20)
        printf("%snumber of pixels in one dimension are less than 20, exact size: %d, each pixel will be very large, if you didn't intend to do it, please try with a smaller time stamp", KRED, break_points->len);

    reader->break_points_v = break_points; 
    return break_points;
}


GArray* gen_breakpoints_realtime(READER* reader, int time_interval){
    /*
     currently this only works for vscsi reader !!!
     return a GArray of break points, not including the last break points
     */
    
    if (reader->type != 'v'){
        printf("gen_breakpoints_realtime currently only support vscsi reader, program exit\n");
        exit(1);
    }
    
    guint64 previous_time = 0;
    GArray* break_points = g_array_new(FALSE, FALSE, sizeof(guint64));

    // create cache lize struct and initialization
    cache_line* cp = (cache_line*)malloc(sizeof(cache_line));
    cp->op = -1;
    cp->size = -1;
    cp->valid = TRUE;
    
    guint64 num = 0;
    
    read_one_element(reader, cp);
    previous_time = cp->real_time;
    g_array_append_val(break_points, num);
    
    while (cp->valid){
        if (cp->real_time - previous_time > time_interval){
            g_array_append_val(break_points, num);
            previous_time = cp->real_time;
        }
        read_one_element(reader, cp);
        num++;
    }
    
    if (break_points->len > 10000)
        printf("%snumber of pixels in one dimension are more than 10000, exact size: %d, it may take a very long time, if you didn't intend to do it, please try with a larger time stamp", KRED, break_points->len);
    else if (break_points->len < 20)
        printf("%snumber of pixels in one dimension are less than 20, exact size: %d, each pixel will be very large, if you didn't intend to do it, please try with a smaller time stamp", KRED, break_points->len);

    reader->break_points_r = break_points;
    return break_points;
}



//#include "reader.h"
//#include "FIFO.h"
//#include "Optimal.h"
//
//int main(int argc, char* argv[]){
//# define CACHESIZE 2000
//# define BIN_SIZE 200
//    int i;
//
//    printf("test_begin!\n");
//
//    READER* reader = setup_reader(argv[1], 'v');
//
////    struct_cache* cache = fifo_init(CACHESIZE, 'v', NULL);
//
//    struct optimal_init_params init_params = {.reader=reader, .next_access=NULL};
//
//    struct_cache* cache = optimal_init(CACHESIZE, 'v', (void*)&init_params);
//
//
//
//    printf("after initialization, begin profiling\n");
//    
//    GArray* break_points = gen_breakpoints_realtime(reader, 10000000);
//    for (i=0; i<break_points->len; i++)
//        printf("%lu\n", g_array_index(break_points, guint64, i));
//    
//
//    printf("test_finished!\n");
//    return 0;
//}
//
//
