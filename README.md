# litecurrency
A small currency API written in typed Python using FastAPI and the external API CurrencyAPI for rates.

## Usage

### Endpoints

The `server.py` app exposes the GET endpoints: 
- `/currencies`
- `/convert?source=[code]&target=[code]`

The first can be called as-is without query parameters. Convert expects at least `source` and `target` that should point to a valid *currency code* (EUR, DKK, SEK, ...). Optionally, `convert` also receives the amount that should be converted (defaults to 1).

### Local Python server

With Python installed in a shell environment, run:

`pip install -r requirements.txt && uvicorn server:app --reload`

This should start a `uvicorn` server on http://localhost:8000

### Local Docker build
With [Docker](https://docs.docker.com/get-docker/) installed and running, execute `./docker-run` in the command line in a POSIX-compliant shell (default on Linux/Mac. Or using WSL2 on Windows). This will build a Docker image (litecurrency) that runs locally using `uvicorn` server that runs on http://localhost:8000.

To easily use the API afterwards, go to http://localhost:8000/docs -> Authorize with a valid CurrencyAPI key, and use the two endpoints provided.

### Docker CI
Upon pushes to any branch, a Docker CI will run using a Github Actions pipeline (see `.github/workflows/docker-image.yml`). This step requires secrets set on the repository itself; normally, this could be set up using a key vault and strict user control so that only required/leveraged users can run this pipeline.

The Docker repository and images built can be found here:
https://hub.docker.com/repository/docker/johanirvall/litecurrency/general
