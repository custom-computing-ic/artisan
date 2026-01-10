#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <sys/time.h>
#define DIM 16
#define CLASSES	1024

int main(int argc, char **argv) {

	int points = atoi(argv[1]);
	srand(100);

	float *classes = (float *)malloc(DIM*CLASSES*sizeof(float));
	float *data = (float *)malloc(points*DIM*sizeof(float));
	float *radii2 = (float *)malloc(CLASSES*sizeof(float));
	int *out = (int *)malloc(points*CLASSES*sizeof(int));

	for(int i = 0; i < CLASSES*DIM; i++) {
		classes[i] = (float) rand();
	}

	for(int i = 0; i < DIM*points; i++){
		data[i] = (float) rand();
	}

	for(int i = 0; i < CLASSES; i++) {
		radii2[i] = (float) rand();
		radii2[i] = radii2[i] * radii2[i];
	}

	for(int i = 0 ; i < CLASSES*points; i++) {
		out[i] = 0;
	}

	for(int i = 0; i < points; i++) {
		for(int j = 0; j < CLASSES; j++) {
			float dist2 = 0.0;
			for(int k = 0 ; k < DIM; k++) {
				dist2 += (classes[k+DIM*j]-data[DIM*i+k]) * (classes[k+DIM*j]-data[DIM*i+k]);
			}
			out[CLASSES*i+j] = (dist2 < radii2[j])? j : -1;
		}
	}

	/* PROCESS RESULTS */
	for (int i = 0; i < CLASSES*points; i += CLASSES*points/10) {
		if (out[i] != -1)
			data[i] = 0;
	}
	free(classes);
	free(data);
	free(radii2);
	free(out);

	return 0;
}

