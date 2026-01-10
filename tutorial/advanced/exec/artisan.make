CXX = g++
CXXFLAGS = -O2 -g -std=c++14 -pthread $(ARTISAN_CXXFLAGS)
LDFLAGS = $(ARTISAN_LDFLAGS)

EXE_NAME = kmeans
SOURCES = main.cpp
ARGS=262144

run: $(EXE_NAME)
	./$(EXE_NAME) $(ARGS)


$(EXE_NAME): main.cpp
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $(EXE_NAME) $(SOURCES)

clean:
	rm -f $(EXE_NAME) profiler.version

