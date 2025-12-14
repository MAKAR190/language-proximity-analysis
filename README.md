# Language Proximity Analysis

Project Report: https://www.overleaf.com/read/cddxvvmjnssh#d44c49

## Prerequisites

- Docker installed on your machine.
- API Keys for translation (Azure Translator Resource).

## Setup

1.  **Clone the repository** (if you haven't already).
2.  **Create an environment file**:
    Create a `.env` file in the `app` directory (or use `.env.local`) with your API keys:
    ```
    TRANSLATE_API_KEY=your_key_here
    TRANSLATE_LOCATION=your_location_here
    ```
3.  **Build the Docker image**:
    ```bash
    docker build -t language-analysis .
    ```

## Running the Project

To run the pipeline and start the GUI, use the following command.

### Linux (with GUI support)

You need to allow X11 forwarding to see the JavaFX GUI.

```bash
xhost +local:docker
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd)/data:/project/data \
  --env-file app/.env.local \
  language-analysis
```

*Note: Replace `app/.env.local` with the path to your environment file.*

### Other Operating Systems

For Windows or macOS, you might need to set up an X Server (like VcXsrv or XQuartz) and configure the `DISPLAY` environment variable accordingly.

If you only want to run the pipeline without the GUI (or if the GUI fails to start):
```bash
docker run -it --rm \
  -v $(pwd)/data:/project/data \
  --env-file app/.env.local \
  language-analysis python3 app/pipeline.py
```