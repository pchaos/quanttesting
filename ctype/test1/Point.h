/* Point.h */

extern void show_point(Point point);
extern void move_point(Point point);
extern void move_point_by_ref(Point *point);

/* Simple structure for ctypes example */
typedef struct {
    int x;
    int y;
} Point;
