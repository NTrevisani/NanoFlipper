# 5x5 eta bin scheme
# parameters : 5
# eta_bin : [ 0. , 0.5  , 1.0  , 1.5  , 2.0 , 2.5 ]
def model_5x5( i , par ):

     if   i == 0:  value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) )
     elif i == 1:  value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) )
     elif i == 2:  value = ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) / ( 1 - ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) )
     elif i == 3:  value = ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) / ( 1 - ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) )
     elif i == 4:  value = ( par[0] * (1-par[ 4]) + (1-par[ 0]) * par[ 4] ) / ( 1 - ( par[0] * (1-par[ 4]) + (1-par[ 0]) * par[ 4] ) )

     elif i == 5:  value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) )
     elif i == 6:  value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) )
     elif i == 7:  value = ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) / ( 1 - ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) )
     elif i == 8:  value = ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) / ( 1 - ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) )
     elif i == 9:  value = ( par[1] * (1-par[ 4]) + (1-par[ 1]) * par[ 4] ) / ( 1 - ( par[1] * (1-par[ 4]) + (1-par[ 1]) * par[ 4] ) )

     elif i == 10: value = ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) / ( 1 - ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) )
     elif i == 11: value = ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) / ( 1 - ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) )
     elif i == 12: value = ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) / ( 1 - ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) )
     elif i == 13: value = ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) / ( 1 - ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) )
     elif i == 14: value = ( par[2] * (1-par[ 4]) + (1-par[ 2]) * par[ 4] ) / ( 1 - ( par[2] * (1-par[ 4]) + (1-par[ 2]) * par[ 4] ) )

     elif i == 15: value = ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) / ( 1 - ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) )
     elif i == 16: value = ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) / ( 1 - ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) )
     elif i == 17: value = ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) / ( 1 - ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) )
     elif i == 18: value = ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) / ( 1 - ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) )
     elif i == 19: value = ( par[3] * (1-par[ 4]) + (1-par[ 3]) * par[ 4] ) / ( 1 - ( par[3] * (1-par[ 4]) + (1-par[ 3]) * par[ 4] ) )

     elif i == 20: value = ( par[4] * (1-par[ 0]) + (1-par[ 4]) * par[ 0] ) / ( 1 - ( par[4] * (1-par[ 0]) + (1-par[ 4]) * par[ 0] ) )
     elif i == 21: value = ( par[4] * (1-par[ 1]) + (1-par[ 4]) * par[ 1] ) / ( 1 - ( par[4] * (1-par[ 1]) + (1-par[ 4]) * par[ 1] ) )
     elif i == 22: value = ( par[4] * (1-par[ 2]) + (1-par[ 4]) * par[ 2] ) / ( 1 - ( par[4] * (1-par[ 2]) + (1-par[ 4]) * par[ 2] ) )
     elif i == 23: value = ( par[4] * (1-par[ 3]) + (1-par[ 4]) * par[ 3] ) / ( 1 - ( par[4] * (1-par[ 3]) + (1-par[ 4]) * par[ 3] ) )
     elif i == 24: value = ( par[4] * (1-par[ 4]) + (1-par[ 4]) * par[ 4] ) / ( 1 - ( par[4] * (1-par[ 4]) + (1-par[ 4]) * par[ 4] ) )

     return value
pass

# 4x4 eta bin scheme
# parameters : 4
#eta_bin = [ 0. , 1.0  , 1.5 , 2.0 , 2.5 ]
def model_4x4( i , par ):

     if   i == 0:  value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) )
     elif i == 1:  value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) )
     elif i == 2:  value = ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) / ( 1 - ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) )
     elif i == 3:  value = ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) / ( 1 - ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) )

     elif i == 4:  value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) )
     elif i == 5:  value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) )
     elif i == 6:  value = ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) / ( 1 - ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) )
     elif i == 7:  value = ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) / ( 1 - ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) )

     elif i == 8: value = ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) / ( 1 - ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) )
     elif i == 9: value = ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) / ( 1 - ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) )
     elif i == 10: value = ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) / ( 1 - ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) )
     elif i == 11: value = ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) / ( 1 - ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) )

     elif i == 12: value = ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) / ( 1 - ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) )
     elif i == 13: value = ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) / ( 1 - ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) )
     elif i == 14: value = ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) / ( 1 - ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) )
     elif i == 15: value = ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) / ( 1 - ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) )

     return value
pass

# 3x3 eta bin scheme
# parameters : 3
#eta_bin = [ ]
def model_3x3( i , par ):

     if   i == 0:  value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) )
     elif i == 1:  value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) )
     elif i == 2:  value = ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) / ( 1 - ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) )

     elif i == 3:  value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) )
     elif i == 4:  value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) )
     elif i == 5:  value = ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) / ( 1 - ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) )

     elif i == 6: value = ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) / ( 1 - ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) )
     elif i == 7: value = ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) / ( 1 - ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) )
     elif i == 8: value = ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) / ( 1 - ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) )

     return value
pass

# 2x2 eta bin scheme
# parameters : 2
#eta_bin = [ 0., 1.5 , 2.5 ]
def model_2x2( i , par ):

     if   i == 0:  value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) )
     elif i == 1:  value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) )

     elif i == 2:  value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) )
     elif i == 3:  value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) )

     return value
pass
