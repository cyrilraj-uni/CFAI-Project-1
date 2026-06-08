import random

from flask import Flask, render_template, request, jsonify

import time


app = Flask(__name__)


# --- BUBBLE SORT ALGORITHM ---

def bubble_sort(arr):

    n = len(arr)

    for i in range(n):

        for j in range(0, n - i - 1):

            if arr[j] > arr[j + 1]:

                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


# --- MERGE SORT ALGORITHM ---

def merge(left, right):

    result = []

    i = j = 0

    while i < len(left) and j < len(right):

        if left[i] < right[j]:

            result.append(left[i])

            i += 1

        else:

            result.append(right[j])

            j += 1

    result.extend(left[i:])

    result.extend(right[j:])

    return result


def merge_sort(arr):

    if len(arr) <= 1:

        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])

    right = merge_sort(arr[mid:])

    return merge(left, right)


# --- LINEAR SEARCH ALGORITHM ---

# Returns the index of `target` in `arr` if found, otherwise -1.

# Time complexity: O(n) — checks every element one-by-one.

def linear_search(arr, target):

    for i in range(len(arr)):

        if arr[i] == target:

            return i

    return -1


# --- ROUTES ---


@app.route('/')

def index():

    return render_template('index.html')


@app.route('/generate/<int:count>')

def generate_data(count):

    # Generates a string of 'count' random numbers separated by commas

    random_list = [str(random.randint(1, 10000)) for _ in range(count)]

    return ",".join(random_list)


@app.route('/sort', methods=['POST'])

def sort():

    # Get user input from frontend

    user_input = request.form.get('numbers')

    target_input = request.form.get('target', '').strip()


    # Clean input: convert string "1, 2, 3" to list [1, 2, 3]

    data = [int(x.strip()) for x in user_input.split(',') if x.strip()]


    # Parse the search target (optional). If missing or invalid, skip search.

    target = None

    if target_input:

        try:

            target = int(target_input)

        except ValueError:

            target = None


    # Benchmark Bubble Sort

    start_b = time.perf_counter()

    bubble_sort(data.copy())

    end_b = time.perf_counter()

    bubble_time = end_b - start_b


    # Benchmark Merge Sort

    start_m = time.perf_counter()

    merge_sort(data.copy())

    end_m = time.perf_counter()

    merge_time = end_m - start_m


    # Benchmark Linear Search (only if a valid target was provided)

    linear_time = 0.0

    linear_found = False

    linear_index = -1

    if target is not None:

        start_l = time.perf_counter()

        linear_index = linear_search(data, target)

        end_l = time.perf_counter()

        linear_time = end_l - start_l

        linear_found = linear_index != -1


    # Send results back to frontend as JSON

    return jsonify({

        'bubble_time': f"{bubble_time:.8f}",

        'merge_time': f"{merge_time:.8f}",

        'linear_time': f"{linear_time:.8f}",

        'linear_found': linear_found,

        'linear_index': linear_index,

        'target': target

    })


if __name__ == '__main__':

    app.run(debug=True)

