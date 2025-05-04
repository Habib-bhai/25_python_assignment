import streamlit as st
import time

# Define the binary search function
def binary_search(lst, target, low=None, high=None):
    steps = []  # To store steps for visualization
    
    if low is None:
        low = 0
    if high is None:
        high = len(lst) - 1

    while low <= high:
        mid_point = (low + high) // 2
        decision = ""
        
        if target == lst[mid_point]:
            decision = f"Target {target} equals midpoint value {lst[mid_point]}."
            steps.append((low, mid_point, high, decision))
            return mid_point, steps
        elif target < lst[mid_point]:
            decision = f"Target {target} is less than midpoint value {lst[mid_point]}. Removing upper half."
            steps.append((low, mid_point, high, decision))
            high = mid_point - 1
        else:
            decision = f"Target {target} is greater than midpoint value {lst[mid_point]}. Removing lower half."
            steps.append((low, mid_point, high, decision))
            low = mid_point + 1

    decision = f"Target {target} not found in the list."
    steps.append((low, -1, high, decision))
    return -1, steps

# Streamlit UI
st.title("Binary Search Algorithm Visualization")
st.write("Enter a sorted list of integers and a target value to visualize the Binary Search algorithm.")
st.write(
    "Binary Search is an efficient algorithm for finding a target value within a sorted list. "
    "The algorithm works by repeatedly dividing the search interval in half."
)

# Input list
user_input = st.text_input("Enter a sorted list (comma-separated):", "1,2,3,4,5,6,8,9,10,12,18,20")
lst = list(map(int, user_input.split(',')))

# Input target
target = st.number_input("Enter the target value:", min_value=min(lst), max_value=max(lst), value=5, step=1)

# Start button
if st.button("Start Binary Search"):
    st.write("### Performing Binary Search...")
    index, steps = binary_search(lst, target)
    
    # Visualize steps
    for i, step in enumerate(steps):
        low, mid, high, decision = step
        if mid != -1:
            st.write(f"**Step {i+1}:**")
            st.write(f"Low Index: {low}, Mid Index: {mid} (value: {lst[mid]}), High Index: {high}")
            st.write(f"Current list segment: {lst[low:high+1]}")
            st.write(f"**Decision:** {decision}")
        else:
            st.write(f"**Step {i+1}: {decision}**")
        time.sleep(1.5)  # Add delay for visualization

    # Final Result
    if index != -1:
        st.success(f"🎉 Target value {target} found at index {index}.")
    else:
        st.error(f"❌ Target value {target} not found in the list.")
