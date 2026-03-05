import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import torchaudio.functional as F
from demucs.apply import apply_model
from demucs.pretrained import get_model

DEMUCS_MODEL = "htdemucs"

_model = None


def _load_demucs(device: str) -> torch.nn.Module:
    """Load htdemucs once and cache it for the process lifetime."""
    global _model
    if _model is None:
        print(f"Loading {DEMUCS_MODEL} (downloading once if not cached)...")
        _model = get_model(DEMUCS_MODEL)
        _model.eval()
    return _model.to(device)


def run_inference(input_file: str, output_dir: str, device: str = "cpu") -> dict[str, str]:
    """Separate *input_file* into drums / bass / other / vocals.

    Returns a dict mapping stem name → output file path.
    """
    start = time.perf_counter()

    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # ── 1. Load model ────────────────────────────────────────────────────────
    model = _load_demucs(device)

    # ── 2. Load audio ────────────────────────────────────────────────────────
    data, sr = sf.read(str(input_path), always_2d=True)  # [T, C] float64
    wav = torch.from_numpy(data.T.astype(np.float32))    # [C, T]

    if sr != model.samplerate:
        wav = F.resample(wav, sr, model.samplerate)

    if wav.shape[0] == 1:
        wav = wav.repeat(2, 1)                           # mono → stereo

    wav = wav.unsqueeze(0)                              # [1, C, T]  (batch dim)

    # ── 3. Separate ──────────────────────────────────────────────────────────
    with torch.no_grad():
        sources = apply_model(model, wav, device=device)  # [1, stems, C, T]

    sources = sources.squeeze(0)                        # [stems, C, T]

    # ── 4. Save one MP3 per stem ─────────────────────────────────────────────
    basename = input_path.stem
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    output_paths: dict[str, str] = {}
    for stem_name, stem_wav in zip(model.sources, sources):
        out_path = out_dir / f"{basename}_{stem_name}.mp3"
        audio_np = stem_wav.cpu().numpy().T          # [T, C]
        sf.write(str(out_path), audio_np, model.samplerate, format="MP3")
        output_paths[stem_name] = str(out_path)
        print(f"  {stem_name:8s} → {out_path}")

    elapsed = time.perf_counter() - start
    print(f"Done in {elapsed:.2f}s")
    return output_paths
