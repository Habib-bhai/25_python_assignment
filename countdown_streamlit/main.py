import streamlit as st
import time

# Custom styling
st.markdown(
    """
    <style>
    .digital-clock {
        font-size: 48px;
        font-family: 'Courier New', monospace;
        color: #FFFFFF;
        background-color: #333333;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .input-container {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title
st.title("⏳ NEXT LEVEL Countdown Timer")

# Input Section
st.markdown('<div class="input-container">', unsafe_allow_html=True)
t = st.number_input("Enter time in seconds:", min_value=1, step=1, key="timer_input")
st.markdown('</div>', unsafe_allow_html=True)

# Button to Start Timer
if st.button("Start Countdown"):
    placeholder = st.empty()  # Placeholder to display the digital clock

    # Countdown logic
    for remaining_time in range(t, -1, -1):
        mins, secs = divmod(remaining_time, 60)
        timer = f"{mins:02d}:{secs:02d}"

        # Update the clock in the placeholder
        placeholder.markdown(
            f'<div class="digital-clock">{timer}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(1)

    # Final Message
    placeholder.markdown(
        '<div class="digital-clock" style="color: #4CAF50;">Timer Complete!</div>',
        unsafe_allow_html=True,
    )
