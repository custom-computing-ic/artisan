#include <artisan>

// Notes about the macro "ARTISAN_MEM_INIT":
//     => must be inserted after including the <artisan> header
//     => only specified once, for instance, where the main function resides

ARTISAN_MEM_INIT

void print_report(void *x1, void *x2, void *x3, void *x4, void *x5) {
    printf("a (%p) => %ld\n", x1, artisan::Mem::size(x1));
    printf("b (%p) => %ld\n", x2, artisan::Mem::size(x2));
    printf("c (%p) => %ld\n", x3, artisan::Mem::size(x3));
    printf("d (%p) => %ld\n", x4, artisan::Mem::size(x4));
    printf("e (%p) => %ld\n", x5, artisan::Mem::size(x5));

}
int main(int argc, char **argv) {
    // all pointer declarations of interest must be registered with:
    //       artisan::Mem::reg(pointer, size-in-bytes)

    // for static allocations, just use sizeof(var) to get the size
    int a[20];
    artisan::Mem::reg(a, sizeof(a));

    char b[] = {'a', 'b', 'c'};
    artisan::Mem::reg(b, sizeof(b));

    double c[10][20];
    artisan::Mem::reg(c, sizeof(c));

    // dynamic allocation with malloc:
    // use the exact argument expression to register the size
    int *d = (int *) malloc(sizeof(int) * 1500);
    artisan::Mem::reg(d, sizeof(int) * 1500);

    // dynamic allocation with new
    // => restrict to vectors (no multidimensional)
    // requires to check the structure of new:
    //     new <type>[size]   ==> sizeof(type) * size
    double *e = new double[20*30];
    artisan::Mem::reg(e, sizeof(double) * 20*30);

    print_report(a, b, c, d, e);

    return 0;

}