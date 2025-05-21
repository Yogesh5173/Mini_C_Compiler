#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 10;
    int y = 20;
    int result = add(x, y);

    if (result > 20) {
        printf("Greater\n");
    } else {
        printf("Smaller or equal\n");
    }

    switch (x) {
        case 10: printf("Ten\n"); break;
        case 20: printf("Twenty\n"); break;
        default: printf("Other\n"); break;
    }

    return 0;
}
