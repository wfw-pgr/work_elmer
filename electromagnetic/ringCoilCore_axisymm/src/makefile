target  = ../calculate__magnetization.dylib
object  = \
  calculate__magnetization.f90

FC      = elmerf90

FFLAGS  =
LDFLAGS =


.SUFFIXES: .o .f90

$(target): $(object)
	$(FC) -o $@ $(object) $(FFLAGS) $(LDFLAGS)


.PHONY:clean all

clean:
	$(RM) -r $(target) *.dylib.dSYM

all: clean $(target)
