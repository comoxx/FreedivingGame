from code.constants import *

def convert_to_depth(y, plongeur):
    diff_top_bottom = DEPTH_BOTTOM_INIT  / ( 1 - HEIGHT_POSITION ) #in meters
    if plongeur.profondeur <= MAX_DEPTH_PARRALAX:
    #Less deep point on the screen
        LESS_DEEP = plongeur.profondeur - DEPTH_BOTTOM_INIT * HEIGHT_POSITION / ( 1 - HEIGHT_POSITION) 
        #Current depth
        DEEPEST = LESS_DEEP + diff_top_bottom
        depth = (y / screen_height()) * (DEEPEST- LESS_DEEP) + LESS_DEEP  
        return depth
    else:
        LESS_DEEP = MAX_DEPTH_PARRALAX - DEPTH_BOTTOM_INIT * HEIGHT_POSITION / ( 1 - HEIGHT_POSITION)
        DEEPEST = LESS_DEEP + diff_top_bottom 
        depth = LESS_DEEP + (DEEPEST - LESS_DEEP) * (y/screen_height())
        return depth

def convert_to_y(depth, plongeur):
    diff_top_bottom = DEPTH_BOTTOM_INIT  / ( 1 - HEIGHT_POSITION ) #in meters
    if plongeur.profondeur <= MAX_DEPTH_PARRALAX:
        LESS_DEEP = plongeur.profondeur - DEPTH_BOTTOM_INIT * HEIGHT_POSITION / ( 1 - HEIGHT_POSITION) 
        y = (depth - LESS_DEEP) / (diff_top_bottom) * screen_height()
        return y
    else:
        LESS_DEEP = MAX_DEPTH_PARRALAX - DEPTH_BOTTOM_INIT * HEIGHT_POSITION / ( 1 - HEIGHT_POSITION) 
        y = (depth - LESS_DEEP) / (diff_top_bottom)  * screen_height()
        return y