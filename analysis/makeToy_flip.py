from utils.mkflipsf import *
from utils.flipModel import model_2x2 as model

etabin = [ 0. , 1.4 , 2.5 ]
dim = (len(etabin)-1)*(len(etabin)-1)
mkToy( dim , etabin  )
