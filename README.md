# Habit-Tracker

A simple command-line habit tracking application.

## Features

- Track daily habits
- Store habit data in a JSON file

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your system.

## Installation

### For Windows:

To get a local copy up and running, follow these simple steps.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/YOUR_USERNAME/Habit-Tracker.git
    cd Habit-Tracker
    ```

2.  **Install dependencies:**
    ```bash
    pip install matplotlib
    python3 -m pip install git+https://github.com/RedFantom/ttkthemes
    ```

### For Linux:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/YOUR_USERNAME/Habit-Tracker.git
    cd Habit-Tracker
    ```

2.  **Install dependencies:**

    -   **Tkinter:**
        -   For Debian/Ubuntu:
            ```bash
            sudo apt-get install python3-tk
            ```
        -   For Fedora:
            ```bash
            sudo dnf install python3-tkinter
            ```
    -   **Matplotlib:**
        ```bash
        python3 -m pip install matplotlib
        ```
    -   **ttkthemes:**
        ```bash
        python3 -m pip install git+https://github.com/RedFantom/ttkthemes
        ```

## Usage

To run the habit tracker, navigate to the project directory and execute the `main.py` script:

```bash
python main.py
```

## File Structure

- `main.py`: The main application script.
- `habits.json`: Stores your habit data.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
