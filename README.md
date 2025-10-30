# Astro Image Colorizer

This project is a web application that allows users to colorize astronomical FITS images. It consists of a Python Flask backend for image processing and a React frontend for the user interface.

## Features

*   Upload FITS files for Red, Green, and Blue channels.
*   Select from predefined color palettes (e.g., Natural Color, Hubble Palette).
*   Process images to generate a colorized RGB PNG.
*   View processed images and their metadata.
*   Toggle between light and dark themes.

## Project Structure

The project is divided into two main parts:

*   **`backend/`**: Contains the Flask application, image processing logic, and API endpoints.
*   **`frontend/`**: Contains the React application for the user interface.

## Setup and Installation

To set up and run the project, follow these steps:

### 1. Clone the Repository

```bash
git clone <repository_url>
cd astro-colorizer
```

### 2. Backend Setup

Navigate to the `backend` directory:

```bash
cd backend
```

**Create and Activate a Virtual Environment (Recommended):**

```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate # On macOS/Linux
```

**Install Python Dependencies:**

```bash
pip install -r requirements.txt
```

### 3. Frontend Setup

Open a *new* terminal and navigate to the `frontend` directory:

```bash
cd frontend
```

**Install Node.js Dependencies:**

```bash
npm install
```

## Running the Application

### 1. Start the Backend Server

In your backend terminal (where you activated the virtual environment):

```bash
python app.py
```

The backend server will start on `http://127.0.0.1:5000`.

### 2. Start the Frontend Development Server

In your frontend terminal:

```bash
npm start
```

The frontend application will open in your browser, usually at `http://localhost:3000`.

## Usage

1.  **Upload FITS Layers**: In the "Upload Layers" section, select your FITS files for the Red, Green, and Blue channels.
2.  **Select Color Palette**: Choose a desired color palette from the dropdown menu.
3.  **Colorize Image**: Click the "Colorize Image" button.
4.  **View Result**: The processed RGB image will appear in the "Visualize & Export" section.

## Contributing

(Optional: Add guidelines for contributions if this were an open-source project.)

## License

(Optional: Add license information.)