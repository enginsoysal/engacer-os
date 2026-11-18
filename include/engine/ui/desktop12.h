/* Shared bounded desktop geometry. Coordinates are logical pixels. */
#ifndef ENGINE_UI_DESKTOP12_H
#define ENGINE_UI_DESKTOP12_H
typedef struct { int x,y,width,height; } ui12_desktop_cell;
enum { UI12_DESKTOP_BUILTINS=4, UI12_DESKTOP_PITCH_X=128, UI12_DESKTOP_PITCH_Y=120 };
static inline unsigned ui12_desktop_rows(unsigned height) {
    #ifdef ENGINE_M13
    unsigned rows=height>164?(height-164)/UI12_DESKTOP_PITCH_Y:0;
#else
    unsigned rows=height>218?(height-218)/UI12_DESKTOP_PITCH_Y:0;
#endif
    return rows?rows:1;
}
static inline unsigned ui12_desktop_reserved(unsigned height) {
    unsigned rows=ui12_desktop_rows(height);
    return (UI12_DESKTOP_BUILTINS+rows-1)/rows;
}
static inline unsigned ui12_desktop_capacity(unsigned width,unsigned height) {
    unsigned columns=width>=188?(width-60)/UI12_DESKTOP_PITCH_X:1;
    unsigned reserved=ui12_desktop_reserved(height);
    columns=columns>reserved?columns-reserved:1;
    unsigned count=columns*ui12_desktop_rows(height);
    return count>128?128:count;
}
static inline ui12_desktop_cell ui12_desktop_position(unsigned height,unsigned index,unsigned builtin) {
    unsigned rows=ui12_desktop_rows(height);
    unsigned column=index/rows+(builtin?0:ui12_desktop_reserved(height));
    return (ui12_desktop_cell){30+(int)column*UI12_DESKTOP_PITCH_X,
#ifdef ENGINE_M13
        24+(int)(index%rows)*UI12_DESKTOP_PITCH_Y,120,112};
#else
        110+(int)(index%rows)*UI12_DESKTOP_PITCH_Y,120,112};
#endif
}
/* Find the next real object on the same row or column, skipping reserved gaps. */
static inline unsigned ui12_desktop_neighbor_visible(unsigned height,unsigned index,unsigned total,unsigned key,unsigned visible) {
    if(index>=total||total>1028)return index;
    ui12_desktop_cell from=ui12_desktop_position(height,index<4?index:index-4,index<4);
    unsigned best=index;int distance=0x7fffffff;
    for(unsigned i=0;i<total;++i){
        if(i<4&&!(visible&(1u<<i)))continue;
        ui12_desktop_cell to=ui12_desktop_position(height,i<4?i:i-4,i<4);
        int dx=to.x-from.x,dy=to.y-from.y;
        int delta=key==128?-dx:key==129?dx:key==133?-dy:dy;
        if(delta<=0||((key==128||key==129)?dy:dx))continue;
        if(delta<distance){best=i;distance=delta;}
    }
    return best;
}
static inline unsigned ui12_desktop_neighbor(unsigned height,unsigned index,unsigned total,unsigned key){return ui12_desktop_neighbor_visible(height,index,total,key,15);}
#endif
