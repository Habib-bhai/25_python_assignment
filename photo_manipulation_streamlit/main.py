import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import io

# Title
st.title("📷 Photo Transformer Web App")
st.write("Upload an image and apply various transformations interactively.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

# Sidebar options
st.sidebar.header("Transformation Settings")

if uploaded_file:
    # Read image
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Original Image", use_column_width=True)

    # Transformation selection
    option = st.sidebar.selectbox(
        "Select transformation:",
        [
            "Brighten / Darken",
            "Adjust Contrast",
            "Blur",
            "Sobel Edge Detection (X)",
            "Sobel Edge Detection (Y)",
            "Combine Sobel (XY)"
        ]
    )

    # Parameters
    if option == "Brighten / Darken":
        factor = st.sidebar.slider("Factor ( <1 darkens, >1 brightens )", 0.1, 3.0, 1.0, 0.1)
    elif option == "Adjust Contrast":
        factor = st.sidebar.slider("Contrast Factor", 0.1, 3.0, 1.0, 0.1)
    elif option == "Blur":
        kernel = st.sidebar.slider("Kernel Size", 1, 31, 3, 2)
    # No extra for sobel

    # Transform button
    if st.sidebar.button("TRANSFORM"):
        # Convert to numpy for custom kernels
        arr = np.array(img).astype(float) / 255.0
        h, w, c = arr.shape

        def apply_kernel_np(image_np, kernel):
            nr = kernel.shape[0] // 2
            out = np.zeros_like(image_np)
            for x in range(h):
                for y in range(w):
                    for ch in range(c):
                        total = 0.0
                        for i in range(-nr, nr+1):
                            for j in range(-nr, nr+1):
                                xi = min(max(x+i, 0), h-1)
                                yj = min(max(y+j, 0), w-1)
                                kval = kernel[i+nr, j+nr]
                                total += image_np[xi, yj, ch] * kval
                        out[x, y, ch] = total
            return np.clip(out, 0, 1)

        if option == "Brighten / Darken":
            enhancer = ImageEnhance.Brightness(img)
            result = enhancer.enhance(factor)
        elif option == "Adjust Contrast":
            enhancer = ImageEnhance.Contrast(img)
            result = enhancer.enhance(factor)
        elif option == "Blur":
            # PIL blur approximate with Gaussian
            result = img.filter(ImageFilter.GaussianBlur(radius=(kernel-1)/2))
        elif option in ["Sobel Edge Detection (X)", "Sobel Edge Detection (Y)"]:
            # Define kernels
            sobel_x = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
            sobel_y = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
            kernel = sobel_x if option.endswith("(X)") else sobel_y
            out_np = apply_kernel_np(arr, kernel)
            result = Image.fromarray((out_np*255).astype(np.uint8))
        else:
            # combine XY
            sobel_x = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
            sobel_y = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
            gx = apply_kernel_np(arr, sobel_x)
            gy = apply_kernel_np(arr, sobel_y)
            mag = np.sqrt(gx**2 + gy**2)
            result = Image.fromarray((np.clip(mag,0,1)*255).astype(np.uint8))

        # Display result
        st.image(result, caption="Transformed Image", use_column_width=True)

        # Download button
        buf = io.BytesIO()
        result.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download image",
            data=byte_im,
            file_name="transformed.png",
            mime="image/png"
        )
