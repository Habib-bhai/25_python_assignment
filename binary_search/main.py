import streamlit as st
import time

# Predefined list
data = list(range(1, 1000001))  # A list from 1 to 1,000,000

# Naive search implementation
def naive_search(lst, target):
    for i in range(len(lst)):
        if lst[i] == target:
            return i
    return -1

# Binary search implementation
def binary_search(lst, target):
    steps = []  # To store steps for visualization

    low = 0
    high = len(lst) - 1

    while low <= high:
        mid_point = (low + high) // 2
        decision = ""

        if target == lst[mid_point]:
            decision = f"Target {target} equals midpoint value {lst[mid_point]}."
            steps.append((low, mid_point, high, decision))
            return mid_point
        elif target < lst[mid_point]:
            decision = f"Target {target} is less than midpoint value {lst[mid_point]}. Removing upper half."
            steps.append((low, mid_point, high, decision))
            high = mid_point - 1
        else:
            decision = f"Target {target} is greater than midpoint value {lst[mid_point]}. Removing lower half."
            steps.append((low, mid_point, high, decision))
            low = mid_point + 1

    return -1

# Streamlit App
st.title("🔍 Binary Search vs Naive Search")
st.write("Compare the performance of Binary Search and Naive Search on a large dataset.")

# Input target value
user_input = st.number_input("Enter the value to search for:", min_value=1, max_value=1000000, value=500000, step=1)

# Run search algorithms when button is clicked
if st.button("Compare Searches"):
    target = int(user_input)

    # Naive search timing
    start_time = time.time()
    naive_result = naive_search(data, target)
    naive_time = time.time() - start_time

    # Binary search timing
    start_time = time.time()
    binary_result = binary_search(data, target)
    binary_time = time.time() - start_time

    # Results
    st.write("### Results")
    st.write(f"**Naive Search** found the target at index: {naive_result}")
    st.write(f"Time taken: {naive_time:.6f} seconds")

    st.write(f"**Binary Search** found the target at index: {binary_result}")
    st.write(f"Time taken: {binary_time:.6f} seconds")

    # Comparison
    st.write("### Performance Comparison")
    if naive_time > binary_time:
        st.success(f"Binary Search was faster by {naive_time - binary_time:.6f} seconds.")
    elif binary_time > naive_time:
        st.warning(f"Naive Search was faster by {binary_time - naive_time:.6f} seconds. (Unexpected!)")
    else:
        st.info("Both searches took the same amount of time.")
