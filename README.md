# Relay Performer

Relay Performer is an interactive music performance system based on FastAPI & online time warping (OLTW) algorithm

Tested on Python 3.10 (conda)

## Setting a new conda environment

```bash
$ pyenv install miniforge3 && pyenv activate miniforge3
$ conda env create -f environment.yml
$ conda activate rpf
```

if there's portaudio installation issue on Mac M1, please refer to [here](https://stackoverflow.com/a/68822818)

## Rebuild DB & Start App

```bash
# rebuild db
$ sqlite3 ./sql_app.db < initial_data.sql

# start app
$ uvicorn app.main:app --reload
```

- To test APIs, go to `127.0.0.1:8000`, which redirects to `127.0.0.1:8000/docs`.
- To manage admin dashboard, go to `127.0.0.1:8000/admin`.
