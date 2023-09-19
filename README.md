# litecurrency
A small currency API written in typed Python using FastAPI and the external API CurrencyAPI for rates.

## Usage

### Local test
Execute `./runner` in the command line in a POSIX-compliant shell (default on Linux/Mac. Or using WSL2 on Windows). This will build a Docker image (litecurrency) that runs locally using `uvicorn` server that runs on http://localhost:8000.

To easily use the API afterwards, go to http://localhost:8000/docs -> Authorize with a valid CurrencyAPI key, and use the two endpoints provided.

### Docker CI
Upon pushes to any branch, a Docker CI will run using a Github Actions pipeline (see `.github/workflows/docker-image.yml`). This step requires secrets set on the repository itself; normally, this could be set up using a key vault and strict user control so that only required/leveraged users can run this pipeline.
