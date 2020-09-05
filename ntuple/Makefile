COMPILER=$(shell root-config --cxx)
FLAGS=$(shell root-config --cflags --libs)

ntuple: nanoflipper.cxx
		$(COMPILER) -g -O3 -Wall -Wextra -Wpedantic -o nanoflipper nanoflipper.cxx $(FLAGS)

clean:
		rm -rf core nanoflipper *.o
