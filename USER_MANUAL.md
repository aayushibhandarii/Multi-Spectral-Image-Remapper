
# Astro Image Colorizer User Manual

## 1. Introduction

Welcome to the Astro Image Colorizer! This application allows you to create stunning composite color images from astronomical FITS files. By combining three separate grayscale images, each representing a different color channel (Red, Green, and Blue), you can generate a full-color representation of celestial objects.

The application consists of a Python-based backend for image processing and a web-based frontend for user interaction.

## 2. Getting Started

To run the application, you need to start both the backend server and the frontend client.

### 2.1. Backend Setup (Python)

The backend is a Flask server that handles the image processing.

1.  **Navigate to the backend directory:**
    ```bash
    cd astro-colorizer/backend
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the backend server:**
    ```bash
    python app.py
    ```

The server will start on `http://127.0.0.1:5000`. Keep this terminal window open.

### 2.2. Frontend Setup (React)

The frontend is a React application that provides the user interface.

1.  **Open a new terminal window.**

2.  **Navigate to the frontend directory:**
    ```bash
    cd astro-colorizer/frontend
    ```

3.  **Install the required Node.js packages:**
    ```bash
    npm install
    ```

4.  **Run the frontend client:**
    ```bash
    npm start
    ```

Your web browser should automatically open to `http://localhost:3000`, displaying the application.

## 3. How to Use the Application

The user interface is designed to be simple and intuitive.

### 3.1. Upload FITS Files

The main screen is divided into a control panel on the left and an image viewer on the right.

1.  In the **"1. Upload Layers"** section, you will find three file input fields:
    -   **Red Channel:** Click "Choose File" and select the FITS file corresponding to the red color channel.
    -   **Green Channel:** Select the FITS file for the green color channel.
    -   **Blue Channel:** Select the FITS file for the blue color channel.

    You must provide a file for all three channels. The application accepts files with `.fits` or `.fit` extensions.

    Sample FITS files for the M51 galaxy are provided in the `data_m51` directory.

### 3.2. Colorize the Image

1.  In the **"2. Colorize Image"** section, you can select a color palette. The default is "Natural".

2.  Click the **"Colorize!"** button.

3.  The application will send the files to the backend for processing. A loading indicator will appear over the image viewer while this is in progress.

### 3.3. View the Result

-   Once processing is complete, the final color image will be displayed in the **Image Viewer** on the right.
-   Below the image, you can find metadata extracted from the FITS files, such as the object name, observation date, and telescope used.

### 3.4. View History

-   The **"3. History"** section on the left panel shows a list of previously generated images from the current session.
-   You can click on any image in the history list to view it again in the main image viewer.

### 3.5. Theme Toggle

-   Click the button in the top-right corner to switch between light and dark mode for a comfortable viewing experience.

## 4. Project Structure

-   `astro-colorizer/`: The main project directory.
    -   `backend/`: Contains the Flask server, image processing logic, and API definitions.
    -   `frontend/`: Contains the React user interface, components, and styling.
    -   `data_m51/`: Contains sample FITS files for testing.
-   `USER_MANUAL.md`: This file.

## 5. Troubleshooting

-   **Error: "Missing one or more channel files"**: This means you did not select a FITS file for each of the Red, Green, and Blue channels before clicking "Colorize!". Please ensure all three file inputs have a file selected.
-   **Application does not load**: Make sure both the backend server and the frontend client are running in separate terminal windows as described in Section 2.
-   **Image looks incorrect**: The quality of the final image depends on the quality and alignment of the input FITS files. Ensure your input files are properly calibrated and aligned.
