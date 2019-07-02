all: point
#all: point wrappedPoint line

clean:
	rm *.o *.so

libpoint.so: Point.c
	gcc -shared -fPIC $^ -o $@

libline.so: Point.c Line.c
	gcc -shared -fPIC $^ -o $@

.o: .c
	gcc -c -Wall -Werror -fpic $^

point: libpoint.so
	python ./testPoint.py

wrappedPoint: libpoint.so
	python ./testWrappedPoint.py

line: libline.so
	python ./testLine.py

doc:
	pandoc ctypes2.md > ctypes2.html
	firefox ctypes2.html
