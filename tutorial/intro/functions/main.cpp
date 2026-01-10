#include <iostream>

void f();

int g(int a, int b) {
    return a+b;
}

int main(int argc, char *argv[]) {
    f();
    int c = g(5, 4) + g(2, 1);
    return 0;

}