import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

# Custom styling for the app
st.markdown(
    """
    <style>
    .qr-container {
        text-align: center;
    }
    .qr-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .qr-button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title of the app
st.title("📸 QR Code Generator")

# Input for the QR Code
data = st.text_input("Enter the text or URL to generate a QR code:", key="qr_input")

# Button to generate the QR code
if st.button("Generate QR Code"):
    if data.strip():
        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image of the QR code
        img = qr.make_image(fill="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        # Display the QR code in the app
        st.markdown('<div class="qr-container">', unsafe_allow_html=True)
        st.image(img_bytes, caption="Your QR Code", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Provide a download button
        st.download_button(
            label="Download QR Code",
            data=img_bytes,
            file_name="qr_code.png",
            mime="image/png",
            key="qr_download",
        )
    else:
        st.error("Please enter some text or URL to generate a QR code.")
