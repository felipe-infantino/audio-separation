import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Run vocal removal on an audio file.")
    parser.add_argument("input_file", help="Path to the input audio file")
    parser.add_argument("output_dir", help="Directory where the output MP3 will be saved")
    parser.add_argument(
        "--device",
        default="cpu",
        help="Compute device: cpu | cuda | mps (default: cpu)",
    )
    args = parser.parse_args()

    from app.inference import run_inference

    try:
        run_inference(args.input_file, args.output_dir, device=args.device)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
