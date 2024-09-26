CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra
TARGET = socket_client

$(TARGET): client.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) client.cpp

.PHONY: clean
clean:
	rm -f $(TARGET)
