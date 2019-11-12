from numba import jit
import random
import csv
import numpy as np
import time

def main():

    # for each point we do 100 iterations to calculate whether it is in the set or not
    max_iters = 2000

    # coordinates
    real_min, real_max = -2, 1
    im_min, im_max = -1.25, 1.25

    # amount of points for integration
    # total_points = np.arange(1000, 1000000, 1000)

    # for points in total_points:
    points = 50000

    max_iterations = np.arange(100, 2000, 100)

    for max_iters in max_iterations:
        print("iters: ", max_iters)

        for test in range(5000):
            starttime = time.time()

            area = mandelbrot_area_mc(real_min, real_max, im_min, im_max, max_iters, points)

            endtime = time.time()

            with open("../data/mc_iters.csv", 'a') as resultsfile:
                writer = csv.writer(resultsfile, delimiter=',')
                writer.writerow([max_iters, points, area, endtime - starttime])


@jit(nopython=True, parallel=True)
def mandelbrot_area_mc(real_min, real_max, im_min, im_max, maxiter, N):
    """ Calculates the area of the Mandelbrot Set using Monte Carlo integration.
        Does this using N points. In theory we found that the area has to be
        somewhere around sqrt(6*pi - 1) - e = 1.506591... (see report for details) """

    total_points = N
    points_in_set = 0

    # loop over each point in the plane and count the number of points in the set
    for n in range(N):
        c = complex(random.uniform(real_min, real_max), random.uniform(im_min, im_max))

        if in_mandelbrot(c, maxiter):
            points_in_set += 1

    total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

    return points_in_set * total_area / total_points



@jit(nopython=True, parallel=True)
def in_mandelbrot(c, maxiter):
    """ Calculates whether a given complex number (c) is in the Mandelbrot Set
        or not. """

    z = 0 + 0j

    for n in range(maxiter):

        # if abs(z) > 2, it is in the set
        if abs(z) > 2:
            return False

        # update z using the Mandelbrot formula.
        z = c + z * z

    # if not in the set, return False
    return True

if __name__ == '__main__':
    main()
