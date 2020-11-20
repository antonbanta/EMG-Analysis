import random
import math
import time

random.seed(1)  # Setting random number generator seed for repeatability
NUM_NEURONS = 10000
NERVE_SIZE = 128000  # nanometers
CONFLICT_RADIUS = 500  # nanometers


def check_for_conflicts(nerves, conflict_radius, num_neurons, method):
    # Simple check all combinations
    # O(N^2)
    # Takes around 100 seconds
    if method == 1:
        neurons = []
        for i in range(num_neurons):
            for j in range(num_neurons):
                if i == j:
                    # Ignore distance between same neuron
                    dist = 10000
                else:
                    dist = math.sqrt((nerves[i][0] - nerves[j][0])**2 + (nerves[i][1] - nerves[j][1])**2)
                if dist <= conflict_radius:
                    neurons.append(i)
                    neurons.append(j)
        return len(set(neurons))

    # Again check combinations but notice that distance is symmetric so we only need to calculate i j not j i or i i
    # This makes it O((N^2-N)/2) and time is about 50 seconds
    elif method == 2:
        neurons = []
        for i in range(0, num_neurons - 1):
            for j in range(i + 1, num_neurons):
                dist = math.sqrt((nerves[i][0] - nerves[j][0]) ** 2 + (nerves[i][1] - nerves[j][1]) ** 2)
                if dist <= conflict_radius:
                    neurons.append(i)
                    neurons.append(j)
        return len(set(neurons))

    # Same as method 2 except I removed the sqrt operation and squared the conflict_radius to reduce number of operations
    # Still ~ O((N^2-N)/2) with time about 40 seconds
    elif method == 3:
        conflict = conflict_radius ** 2
        neurons = []
        for i in range(0, num_neurons - 1):
            for j in range(i + 1, num_neurons):
                dist = (nerves[i][0] - nerves[j][0]) ** 2 + (nerves[i][1] - nerves[j][1]) ** 2
                if dist <= conflict:
                    neurons.append(i)
                    neurons.append(j)
        return len(set(neurons))

    # Fastest method. This involves finding candidate neuron pairs in the x dimension and then the y dimension
    # to greatly reduce the number of iterations.
    # Average time is 1 second and complexity should be O(Nlog(N))
    # This should scale very well and I don't think you can do significantly better than this
    # unless you used special data structures.
    elif method == 4:
        conflict = conflict_radius ** 2
        # Get x coordinates
        x = [coord[0] for coord in nerves]
        # Get indices of sorted x
        x_idx = sorted(range(len(x)), key=lambda c: x[c])
        # Sort x in ascending order
        x = sorted(x)
        candidates_x = []
        for idx, center in enumerate(x):
            # Find max distance from current point for it to interfere
            x_lim = center + conflict_radius
            for idx2 in range(idx+1, num_neurons):
                # Check if subsequent points are within this max distance
                if x[idx2] <= x_lim:
                    candidates_x.append([x_idx[idx], x_idx[idx2]])
                else:
                    break
        # Same for y dimension
        y = [coord[1] for coord in nerves]
        y_idx = sorted(range(len(y)), key=lambda c: y[c])
        y = sorted(y)
        candidates_y = []
        for idx, center in enumerate(y):
            y_lim = center + conflict_radius
            for idx2 in range(idx + 1, num_neurons):
                if y[idx2] <= y_lim:
                    candidates_y.append([y_idx[idx], y_idx[idx2]])
                else:
                    break
        # Now calculate the euclidean distance to get the conflicting neurons
        candidates = candidates_x + candidates_y
        neurons = []
        for pair in candidates:
            dist = (nerves[pair[0]][0] - nerves[pair[1]][0]) ** 2 + (nerves[pair[0]][1] - nerves[pair[1]][1]) ** 2
            if dist <= conflict:
                neurons.append(pair[0])
                neurons.append(pair[1])
        return len(set(neurons))



def gen_coord():
    return int(random.random() * NERVE_SIZE)


if __name__ == "__main__":
    # Get all neuron locations
    neuron_positions = []
    for n in range(NUM_NEURONS):
        neuron_positions.append([gen_coord(), gen_coord()])
    # Call all methods and print timings
    for method in range(1, 5):
        start_time = time.time()
        n_conflicts = check_for_conflicts(neuron_positions, CONFLICT_RADIUS, NUM_NEURONS, method)
        print("--- method: " + str(method) + " ---")
        print("--- %s seconds ---" % (time.time() - start_time))
        print(" Neurons in conflict : {}".format(n_conflicts))




