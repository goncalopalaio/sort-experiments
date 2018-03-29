import random
import time

def timing(f):
	def wrap(*args):
		time1 = time.time()
		ret = f(*args)
		time2 = time.time()
		print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
		return ret
	return wrap


def generate_unsorted(n, min_val = 0, max_val = 1000):
	return [random.randint(min_val, max_val) for _ in range(n)]

@timing
def baseline_sort(arr, reverse_order = False):
	return sorted(arr, reverse = reverse_order)

def baseline_compare(a, b):
	if len(a) != len(b):
		raise ValueError("ERROR:: LEN DIFFERS: a: ", a, " b: ", b)
		return False
	for i, v in enumerate(a):
		if v != b[i]:
			raise ValueError("ERROR:: VALUE IDX : ", i, " DIFFERS a: ", a, " b: ", b)
			return False
	print("::ALL GOOD::")
	return True


def baseline_test(fn_a, fn_b, n_values, min_val = 0, max_val = 100):
	arr = generate_unsorted(n_values, min_val, max_val)
	print("DATA_LEN: ", len(arr))

	return baseline_compare(fn_a(arr), fn_b(arr))

# --- Bubblesort
@timing
def bubble_sort(input):
	l = len(input)
	while True:
		swapped = False
		for i in range(1, l):
			if input[i-1] > input[i]:
				input[i-1], input[i] = input[i], input[i-1]
				swapped = True
		if not swapped:
			break
	return input

# --- Mergesort
def mergesort_sort(input):
	l = len(input)
	
	if l <= 1:
		return input

	half_point = int(l / 2)
	left = input[:half_point]
	right = input[half_point:]
	
	left = mergesort_sort(left)
	right = mergesort_sort(right)
	return mergesort_merge(input, left, right)

def mergesort_merge(input, a, b):
	# pop() would make this shorter
	idx = 0
	idx_a = 0
	idx_b = 0
	l_a = len(a)
	l_b = len(b)

	if l_a == 0:
		return b
	if l_b == 0:
		return a

	remaining = l_a + l_b
	while idx < remaining:
		if idx_a >= l_a:
			input[idx] = b[idx_b]
			idx_b += 1
		elif idx_b >= l_b:
			input[idx] = a[idx_a]
			idx_a += 1
		elif a[idx_a] < b[idx_b]:
			input[idx] = a[idx_a]
			idx_a += 1
		else:
			input[idx] = b[idx_b]
			idx_b += 1
		idx += 1
	return input

@timing
def quicksort_sort(input):
	return _quicksort_sort(input, 0, len(input)-1)

def _quicksort_partition(input, pivot_idx, left_idx, right_idx):
	pivot_value = input[pivot_idx]
	input[pivot_idx], input[right_idx] = input[right_idx], input[pivot_idx]
	
	center_idx = left_idx
	for i in range(left_idx, right_idx):
		if input[i] <= pivot_value:
			input[i], input[center_idx] = input[center_idx], input[i]
			center_idx += 1

	# put the pivot at the center
	# we will now have all the values below the pivot in one side and the others on the other
	input[center_idx], input[right_idx] = input[right_idx], input[center_idx]	
	
	return center_idx

	
def _quicksort_sort(input, left_idx, right_idx):
	if left_idx >= right_idx:
		return input
	# let's keep it simple and choose the pivot without any heuristic
	pivot_idx = left_idx + int((right_idx - left_idx - 1) / 2)

	# the pivot now changed places to divide the numbers in two sections
	pivot_idx = _quicksort_partition(input, pivot_idx, left_idx, right_idx)


	# pivot is already in the sorted position
	_quicksort_sort(input, left_idx, pivot_idx - 1)
	_quicksort_sort(input, pivot_idx + 1, right_idx)

	return input

def main():
	#baseline_test(baseline_sort, bubble_sort, 5, -100, 100)
	#baseline_test(baseline_sort, bubble_sort, 1, -100, 100)
	
	#baseline_test(baseline_sort, mergesort_sort, 5, -100, 100)
	#baseline_test(baseline_sort, mergesort_sort, 1, -100, 100)
	print(quicksort_sort([0,20,0, 4, 100]))
	baseline_test(baseline_sort, quicksort_sort, 5, 0, 100)
	baseline_test(baseline_sort, quicksort_sort, 1, -100, 100)
	
	for i in range(100):
		#baseline_test(baseline_sort, bubble_sort, random.randint(1, 1000), random.randint(-1000, 500), 1000)
		#baseline_test(baseline_sort, mergesort_sort, random.randint(1, 1000), random.randint(-1000, 500), 1000)
		baseline_test(baseline_sort, quicksort_sort, random.randint(1, 1000), random.randint(-1000, 500), 1000)

	


if __name__ == '__main__':
	main()