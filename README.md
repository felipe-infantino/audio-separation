[![PyPI version](https://badge.fury.io/py/audio-separation.svg)](https://badge.fury.io/py/audio-separation)
# audio-separation

Local audio source separation. Drums, Bass, Vocal and other. 

## Requirements

- Python 3.11–3.14
- FFmpeg (`brew install ffmpeg` / `apt install ffmpeg`)

## Install

```bash
pip install audio-separation
```

## Usage

```bash
audio-separation "track.mp3" ./outputs/
audio-separation "track.mp3" ./outputs/ --device cuda
audio-separation "track.mp3" ./outputs/ --device mps
```

Output files are saved as `<track>_<stem>.mp3` in the specified directory.

## Arguments

| Argument | Description |
|---|---|
| `input_file` | Path to the input audio file |
| `output_dir` | Directory where the output MP3 will be saved |

## Options

| Flag | Default | Description |
|---|---|---|
| `--device` | `cpu` | Inference device: `cpu`, `cuda`, `mps` |


## Development

```bash
git clone https://github.com/felipeinfantino/audio-separation
cd audio-separation
poetry install
poetry run audio-separation "inputs/Alucinados.mp3" "outputs"
```

### Extending with a new package

```bash
poetry add [packagename]

# Check the CLI is still working
poetry run audio-separation "inputs/Alucinados.mp3" "outputs"

# Verify lockfile is clean
poetry lock

# Bump version
poetry version patch   # or minor / major
```

### Git build versioning

Let x.y.z be the new bumped version:

```bash
git tag v[x.y.z]
git push origin main --tags
```

## License

MIT
