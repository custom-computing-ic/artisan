
#pragma artisan fn (a: 2, b: 3)

int foo(int a, int b, int c) {
   int k = 0;

   #pragma artisan loop (c: 3, d: test)
   for (int i=0; i < a; i++)
       for (int l = 0; l < b; l++)
            for (int m = 0; m < c; m++)
                k++;
   return k;
}

#pragma artisan another pragma


#pragma artisan fn (c: 3, d: test)

int bar(int a, int b, int c) {
   int k = 0;
   for (int i=0; i < a; i++)
       for (int l = 0; l < b; l++)
            for (int m = 0; m < c; m++)
                k=k+2;

   return k;
}



