"""Run from any working directory: python /path/to/run.py --config config/real.json."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from screentime.pipeline import run_pipeline
from screentime.simulate import save_simulation


def main():
    parser = argparse.ArgumentParser(description="Screen-time EDA/CDA with explicit data provenance.")
    parser.add_argument("--config", default="config/simulated.json")
    parser.add_argument("--generate-simulated", action="store_true")
    args = parser.parse_args()
    if args.generate_simulated:
        save_simulation(ROOT / "data/simulated/screen_time_simulated.csv")
    config = Path(args.config)
    if not config.is_absolute():
        config = ROOT / config
    try:
        result = run_pipeline(config)
    except (ValueError, FileNotFoundError) as error:
        parser.exit(2, f"Input error: {error}\n")
    print(f"{result['config']['data_kind']}: {result['manifest']['included']} / {result['manifest']['submitted']} included")
    print(f"Outputs: {result['output_dir']}")
    if result["config"]["data_kind"] == "SIMULATED":
        print("Demonstration only. These are not collected student findings.")


if __name__ == "__main__":
    main()
