COMPILER=$(shell root-config --cxx)
FLAGS=$(shell root-config --cflags --libs)

ntuple: flipskim.cxx
		$(COMPILER) -g -O3 -Wall -Wextra -Wpedantic -o flipskim flipskim.cxx $(FLAGS)

clean:
		rm -rf core flipskim *.o
