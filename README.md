## Build Dockerfile
```sudo docker build . -t chimerax```
## Run docker
```sudo docker run --rm -v $(pwd)/data:/data -v $(pwd):/app --workdir /app chimerax /app/run.py```
