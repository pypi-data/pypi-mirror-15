//
//  heatmap.h
//  heatmap
//
//  Created by Juncheng on 5/24/16.
//  Copyright © 2016 Juncheng. All rights reserved.
//

#ifndef heatmap_h
#define heatmap_h

#include <stdio.h>
#include <stdlib.h>
#include <glib.h>
#include "reader.h"
#include "glib_related.h" 
#include "cache.h" 
#include "LRUProfiler.h"
//#include "generalProfiler.h" 




typedef struct {
    guint64 xlength;
    guint64 ylength;
    double** matrix;
    
}draw_dict;

void free_draw_dict(draw_dict* dd);




GSList* get_last_access_dist_seq(READER* reader, void (*funcPtr)(READER*, cache_line*));

GArray* gen_breakpoints_virtualtime(READER* reader, int time_interval);
GArray* gen_breakpoints_realtime(READER* reader, int time_interval);


#endif /* heatmap_h */
