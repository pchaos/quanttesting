//test.cpp
#define DLLEXPORT extern "C"

DLLEXPORT int sum(int a, int b) {
    return a + b;
}