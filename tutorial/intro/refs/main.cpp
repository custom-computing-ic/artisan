struct Structure {
    int a;
    float b;
    struct X {
        int c[20];
        int *d;
    } x;
};

int a;

int main(int argc, char *argv[]) {
    int b;
    int c;
    int x;
    int *y;
    int z[20];
    Structure s[10];

    a = 0;
    b = 10;
    c = 16;

    x = 10 + a + b + c;
    s[0].a = 20;
    s[0].x.c[0] += 15 + x++;
    s[0].x.d = nullptr;


}