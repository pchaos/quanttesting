// main.cpp
#include "exported.h"

extern "C"
{
  EXPORTED int add(int a, int b)
  {
      return a + b;
  }
}
