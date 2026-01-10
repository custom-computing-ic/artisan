
int foo(int a, int b, int c) {
   int k = 0;
   for (int i=0; i < a; i++)
       for (int l = 0; l < b; l++)
            for (int m = 0; m < c; m++)
                k++;

   return k;
}

int bar(int a, int b, int c) {
   int k = 0;
   for (int i=0; i < a; i++)
       for (int l = 0; l < b; l++)
            for (int m = 0; m < c; m++)
                k=k+2;

   return k;
}



