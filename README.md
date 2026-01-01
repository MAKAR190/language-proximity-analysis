# Language Proximity Analysis

**Project Report:** [https://www.overleaf.com/read/cddxvvmjnssh#d44c49](https://www.overleaf.com/read/cddxvvmjnssh#d44c49)

## How to Run Locally Using Docker

### Prerequisites
1.  **Install Docker**: Ensure Docker is installed on your system (Windows, Mac, or Linux).
2.  **Start Docker**: Make sure the Docker Desktop application (or daemon) is running.
3.  **Reboot (if needed)**: If you just installed Docker, you may need to reboot your machine for it to work correctly.

### Steps to Run

1.  **Enter the Project Directory**:
    Open your terminal or command prompt and navigate to the project folder:
    ```bash
    cd language-proximity-analysis
    ```

2.  **Build the Docker Image**:
    Run the following command to build the project:
    ```bash
    docker-compose build
    ```

3.  **Run the Application**:
    Start the container:
    ```bash
    docker-compose up
    ```

4.  **Access the GUI**:
    *   Open your web browser.
    *   Go to the following URL: [http://localhost:6080/vnc.html](http://localhost:6080/vnc.html)
    *   Click the **Connect** button in the center of the screen.

### What is VNC (and why do we need it)?

You might be wondering why we are using **VNC** (Virtual Network Computing) and accessing `vnc.html`.

*   **The Challenge**: This project includes a JavaFX Graphical User Interface (GUI). Docker containers are typically "headless," meaning they don't have a physical monitor or display attached. If we tried to run the GUI directly in Docker, it would crash because it has nowhere to draw the window.
*   **The Solution**: We use a tool called **Xvfb** to create a "virtual" screen inside the container. Then, we use a VNC server to capture that virtual screen and stream it. Finally, **noVNC** (the web page you are visiting) allows you to view and interact with that stream directly in your browser. This lets you see and use the application's GUI as if it were running natively on your computer, regardless of your operating system.