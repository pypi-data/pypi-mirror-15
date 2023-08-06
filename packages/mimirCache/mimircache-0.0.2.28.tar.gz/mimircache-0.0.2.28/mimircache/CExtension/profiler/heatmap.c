

#include "heatmap.h" 


draw_dict* heatmap_LRU(READER* reader, struct_cache* cache, char mode, long time_interval, int plot_type, int num_of_threads);
draw_dict* heatmap_nonLRU(READER* reader, struct_cache* cache, char mode, long time_interval, int plot_type, int num_of_threads);
draw_dict* heatmap_hit_rate_start_time_end_time(READER* reader, struct_cache* cache, char mode, long time_interval, int plot_type, int num_of_threads);


draw_dict* heatmap(READER* reader, struct_cache* cache, char mode, guint64 time_interval, int plot_type, int num_of_threads){

    DEBUG(printf("before break points\n"));
    
    if (mode == 'v')
        gen_breakpoints_virtualtime(reader, time_interval);
    else if (mode == 'r')
        gen_breakpoints_realtime(reader, time_interval);
    else{
        printf("unsupported mode: %c\n", mode);
        exit(1);
    }
    DEBUG(printf("after break points\n"));
    // check cache is LRU or not
    if (cache && cache->core->type == e_LRU){
        return heatmap_LRU(reader, cache, mode, time_interval, plot_type, num_of_threads);
    }
    else{
        return heatmap_nonLRU(reader, cache, mode, time_interval, plot_type, num_of_threads);
    }
}


draw_dict* heatmap_LRU(READER* reader, struct_cache* cache, char mode, long time_interval, int plot_type, int num_of_threads){

    get_reuse_dist_seq(reader, 0, -1);
        
    if (plot_type == hit_rate_start_time_end_time){
        GSList* last_access_gslist = get_last_access_dist_seq(reader, read_one_element);
        reader->last_access = (gint*) malloc(sizeof(gint)*reader->total_num);
        GSList* sl_node = last_access_gslist;
        guint64 counter = reader->total_num-1;
        reader->last_access[counter--] = GPOINTER_TO_INT(sl_node->data);
        while(sl_node->next){
            sl_node = sl_node->next;
            reader->last_access[counter--] = GPOINTER_TO_INT(sl_node->data);
        }
        g_slist_free(last_access_gslist);
        return heatmap_hit_rate_start_time_end_time(reader, cache, mode, time_interval, plot_type, num_of_threads);
    }
    
    
    
    else if (plot_type == hit_rate_start_time_cache_size){
        
        
        
    }
    
    else if (plot_type == avg_rd_start_time_end_time){
        
        
        
    }

    else if (plot_type == cold_miss_count_start_time_end_time){
        
        
        
    }
    else if (plot_type == rd_distribution){
        return heatmap_rd_distribution(reader, mode, time_interval, num_of_threads);
    }
    else if (plot_type == hit_rate_start_time_cache_size){
        
        
        
    }
    else {
        printf("unknown plot type\n");
        exit(1);
    }
    
    return NULL;
}


draw_dict* heatmap_nonLRU(READER* reader, struct_cache* cache, char mode, long time_interval, int plot_type, int num_of_threads){
    if (plot_type == hit_rate_start_time_end_time){
        return heatmap_hit_rate_start_time_end_time(reader, cache, mode, time_interval, plot_type, num_of_threads);
    }
    else if (plot_type == hit_rate_start_time_cache_size){
        
        
        
    }
    
    else if (plot_type == avg_rd_start_time_end_time){
        
        
        
    }
    
    else if (plot_type == cold_miss_count_start_time_end_time){
        
        
        
    }
    else if (plot_type == rd_distribution){
        get_reuse_dist_seq(reader, 0, -1);
        return heatmap_rd_distribution(reader, mode, time_interval, num_of_threads);
    }
    else if (plot_type == future_rd_distribution){
        get_future_reuse_dist(reader, 0, -1);
        draw_dict* dd = heatmap_rd_distribution(reader, mode, time_interval, num_of_threads);
        
        reader->max_reuse_dist = 0;
        free(reader->reuse_dist);
        reader->reuse_dist = NULL;
        
        return dd;
    }

    else if (plot_type == hit_rate_start_time_cache_size){
        
        
        
    }
    else {
        printf("unknown plot type\n");
        exit(1);
    }
    
    return NULL;
}




draw_dict* heatmap_hit_rate_start_time_end_time(READER* reader, struct_cache* cache, char mode, long time_interval, int plot_type, int num_of_threads){

    guint i;
    guint64 progress = 0;
    
    GArray* break_points;
    break_points = reader->break_points->array;
        

    // create draw_dict storage
    draw_dict* dd = (draw_dict*) malloc(sizeof(draw_dict));
    dd->xlength = break_points->len;
    dd->ylength = break_points->len;
    dd->matrix = (double**) malloc(break_points->len * sizeof(double*));
    for (i=0; i<break_points->len; i++)
        dd->matrix[i] = (double*) calloc(break_points->len, sizeof(double));
    

    // build parameters
    struct multithreading_params_heatmap* params = malloc(sizeof(struct multithreading_params_heatmap) );
    params->reader = reader;
    params->break_points = break_points;
    params->cache = cache;
    params->dd = dd;
    params->progress = &progress;
    g_mutex_init(&(params->mtx));

    
    // build the thread pool
    GThreadPool * gthread_pool;
    if (cache->core->type == e_LRU)
        gthread_pool = g_thread_pool_new ( (GFunc) heatmap_LRU_hit_rate_start_time_end_time_thread, (gpointer)params, num_of_threads, TRUE, NULL);
    else
        gthread_pool = g_thread_pool_new ( (GFunc) heatmap_nonLRU_hit_rate_start_time_end_time_thread, (gpointer)params, num_of_threads, TRUE, NULL);
    
    if (gthread_pool == NULL)
        g_error("cannot create thread pool in heatmap\n");
    
    
    // send data to thread pool and begin computation
    for (i=0; i<break_points->len; i++){
        if ( g_thread_pool_push (gthread_pool, GINT_TO_POINTER(i+1), NULL) == FALSE)    // +1 otherwise, 0 will be a problem
            g_error("cannot push data into thread in generalprofiler\n");
    }
    
    while ( progress < break_points->len ){
        printf("%.2f%%\n", ((double)progress)/break_points->len*100);
        sleep(1);
        printf("\033[A\033[2K\r");
    }
    
    g_thread_pool_free (gthread_pool, FALSE, TRUE);
    

    g_mutex_clear(&(params->mtx)); 
    free(params);
    // needs to free draw_dict later
    return dd;
}
    

draw_dict* heatmap_rd_distribution(READER* reader, char mode, long time_interval, int num_of_threads){
    /* this one, the result is in the log form */
    
    guint i;
    guint64 progress = 0;
    
    GArray* break_points;
    break_points = reader->break_points->array;
    
    // this is used to make sure length of x and y are approximate same, not different by too much
    double log_base = get_log_base(reader->max_reuse_dist, break_points->len);
    reader->log_base = log_base;
    
    // create draw_dict storage
    draw_dict* dd = (draw_dict*) malloc(sizeof(draw_dict));
    dd->xlength = break_points->len;
    
    // the last one is used for store cold miss; rd=0 and rd=1 are combined at first bin (index=0) 
    dd->ylength = (long) ceil(log(reader->max_reuse_dist)/log(log_base));
    dd->matrix = (double**) malloc(break_points->len * sizeof(double*));
    for (i=0; i<break_points->len; i++)
        dd->matrix[i] = (double*) calloc(dd->ylength, sizeof(double));
    
    
    // build parameters
    struct multithreading_params_heatmap* params = malloc(sizeof(struct multithreading_params_heatmap) );
    params->reader = reader;
    params->break_points = break_points;
    params->dd = dd;
    params->progress = &progress;
    params->log_base = log_base;
    g_mutex_init(&(params->mtx));
    
    
    // build the thread pool
    GThreadPool * gthread_pool;
    gthread_pool = g_thread_pool_new ( (GFunc) heatmap_rd_distribution_thread, (gpointer)params, num_of_threads, TRUE, NULL);
    
    if (gthread_pool == NULL)
        g_error("cannot create thread pool in heatmap rd_distribution\n");
    

    // send data to thread pool and begin computation
    for (i=0; i<break_points->len; i++){
        if ( g_thread_pool_push (gthread_pool, GINT_TO_POINTER(i+1), NULL) == FALSE)    // +1 otherwise, 0 will be a problem
            g_error("cannot push data into thread in generalprofiler\n");
    }

    while ( progress < break_points->len ){
        printf("%.2lf%%\n", ((double)progress)/break_points->len*100);
        sleep(1);
        printf("\033[A\033[2K\r");
    }

    g_thread_pool_free (gthread_pool, FALSE, TRUE);

    
    g_mutex_clear(&(params->mtx));
    free(params);
    
    return dd;
}



draw_dict* differential_heatmap(READER* reader, struct_cache* cache1, struct_cache* cache2, char mode, guint64 time_interval, int plot_type, int num_of_threads){
    
    if (mode == 'v')
        gen_breakpoints_virtualtime(reader, time_interval);
    else if (mode == 'r')
        gen_breakpoints_realtime(reader, time_interval);
    else{
        printf("unsupported mode: %c\n", mode);
        exit(1);
    }

    draw_dict *draw_dict1, *draw_dict2;
    // check cache is LRU or not
    if (cache1->core->type == e_LRU){
        draw_dict1 = heatmap_LRU(reader, cache1, mode, time_interval, plot_type, num_of_threads);
    }
    else{
        draw_dict1 = heatmap_nonLRU(reader, cache1, mode, time_interval, plot_type, num_of_threads);
    }

    if (cache2->core->type == e_LRU){
        draw_dict2 = heatmap_LRU(reader, cache2, mode, time_interval, plot_type, num_of_threads);
    }
    else{
        draw_dict2 = heatmap_nonLRU(reader, cache2, mode, time_interval, plot_type, num_of_threads);
    }

    
    guint64 i, j;
    for (i=0; i<draw_dict1->xlength; i++)
        for (j=0; j<draw_dict1->ylength; j++){
//            if (draw_dict1->matrix[i][j] > 1 || draw_dict1->matrix[i][j] < 0)
//                printf("ERROR -1 %ld, %ld: %f\n", i, j, draw_dict1->matrix[i][j]);
//            if (draw_dict2->matrix[i][j] > 1 || draw_dict2->matrix[i][j] < 0)
//                printf("ERROR -2 %ld, %ld: %f\n", i, j, draw_dict2->matrix[i][j]);
            draw_dict2->matrix[i][j] = draw_dict2->matrix[i][j] - draw_dict1->matrix[i][j];
        }
    free_draw_dict(draw_dict1);
    return draw_dict2;
}


void free_draw_dict(draw_dict* dd){
    guint64 i;
    for (i=0; i<dd->xlength; i++){
        free(dd->matrix[i]);
    }
    free(dd->matrix);
    free(dd);
}


#include "reader.h"
#include "FIFO.h"
#include "Optimal.h"

int main(int argc, char* argv[]){
# define CACHESIZE 2000
# define BIN_SIZE 200
# define TIME_INTERVAL 10000000


    printf("test_begin!\n");

    READER* reader = setup_reader(argv[1], 'v');

//    struct_cache* cache = fifo_init(CACHESIZE, 'v', NULL);

    struct optimal_init_params init_params = {.reader=reader, .next_access=NULL, .ts=0};
    struct_cache* optimal = optimal_init(CACHESIZE, 'v', (void*)&init_params);
    
    
    struct_cache* cache = cache_init(CACHESIZE, reader->type);
    cache->core->type = e_LRU;

    
//    struct_cache* cache = (struct_cache*) malloc(sizeof(struct_cache));
//    cache->size = CACHESIZE;

    draw_dict* dd ;
    
    printf("after initialization, begin profiling\n");
    dd = differential_heatmap(reader, cache, optimal, 'r', 1000000, hit_rate_start_time_end_time, 8);
//    draw_dict* dd = heatmap(reader, NULL, 'r', 10000000, rd_distribution, 8);
//    draw_dict* dd = heatmap_rd_distribution(reader, 'r', 1000000, 8);
    dd = heatmap(reader, NULL, 'r', TIME_INTERVAL, rd_distribution, 8);

    printf("cache init params: %p\n", optimal->core->cache_init_params);

    long long count;
    guint64 i, j;
    for (i=0; i<dd->xlength; i++){
        for (j=0; j<dd->ylength; j++)
            count = (long long) dd->matrix[i][j];
//            printf("%llu, %llu: %f\n", i, j, dd->matrix[i][j]);
            ;
    }
    free_draw_dict(dd);
    dd = heatmap(reader, NULL, 'r', TIME_INTERVAL, future_rd_distribution, 8);

    printf("computation finished\n");
    free_draw_dict(dd);
//    cache->destroy(cache);
    cache_destroy(cache);
    optimal->core->destroy(optimal);
    close_reader(reader);
    
    printf("test_finished!\n");

    return 0;
}



