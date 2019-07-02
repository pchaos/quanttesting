all: foo
#all: point wrappedPoint line

clean:
	rm *.o *.so

libtest.so: test.cpp
	g++ -shared -fPIC $^ -o $@

.o: .cpp
	g++ -c -Wall -Werror -fpic $^

foo: libtest.so
	python ./testSum.py
