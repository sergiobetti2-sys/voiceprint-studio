"""Voiceprint Studio - ECAPA feasibility proof of concept.

The command-line PoC validates deterministic preprocessing, ECAPA embedding
extraction, repeatability, and cosine similarity. Model files and real audio
remain outside the Git repository.
"""

from __future__ import annotations

import argparse
import math
import os
import shutil
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np
from scipy.signal import resample_poly

if TYPE_CHECKING:
    from collections.abc import Sequence


MODEL_ID = "speechbrain/spkrec-ecapa-voxceleb"
MODEL_REVISION = "0f99f2d0ebe89ac095bcc5903c4dd8f72b367286"
MODEL_FILE_SOURCES = {
    "classifier.ckpt": "classifier.ckpt",
    "embedding_model.ckpt": "embedding_model.ckpt",
    "hyperparams.yaml": "hyperparams.yaml",
    "label_encoder.ckpt": "label_encoder.txt",
    "mean_var_norm_emb.ckpt": "mean_var_norm_emb.ckpt",
}
MODEL_FILES = tuple(MODEL_FILE_SOURCES)
TARGET_SAMPLE_RATE = 16_000
EMBEDDING_SIZE = 192


def default_model_directory() -> Path:
    """Return the external per-user model directory."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    base = Path(local_app_data) if local_app_data else Path.home() / ".local" / "share"
    return base / "VoiceprintStudio" / "models" / "spkrec-ecapa-voxceleb"


def missing_model_files(model_directory: Path) -> list[str]:
    """Return the required model files that are not available locally."""
    return [name for name in MODEL_FILES if not (model_directory / name).is_file()]


def install_pinned_model(model_directory: Path, *, offline: bool) -> None:
    """Copy the pinned Hugging Face snapshot into the external model directory."""
    from huggingface_hub import snapshot_download

    snapshot = Path(
        snapshot_download(
            repo_id=MODEL_ID,
            revision=MODEL_REVISION,
            local_files_only=offline,
            allow_patterns=list(MODEL_FILE_SOURCES.values()),
        )
    )
    model_directory.mkdir(parents=True, exist_ok=True)
    for destination_name, source_name in MODEL_FILE_SOURCES.items():
        source = snapshot / source_name
        if not source.is_file():
            raise FileNotFoundError(f"File del modello non trovato: {source}")
        shutil.copy2(source, model_directory / destination_name)

    (model_directory / "model-revision.txt").write_text(
        f"{MODEL_ID}\n{MODEL_REVISION}\n",
        encoding="utf-8",
    )


def prepare_waveform(samples: np.ndarray, sample_rate: int) -> np.ndarray:
    """Convert mono/stereo floating-point audio to finite mono 16 kHz samples."""
    if sample_rate <= 0:
        raise ValueError("sample_rate deve essere maggiore di zero")

    waveform = np.asarray(samples, dtype=np.float32)
    if waveform.ndim == 2:
        waveform = np.mean(waveform, axis=1, dtype=np.float32)
    elif waveform.ndim != 1:
        raise ValueError("l'audio deve essere mono o multicanale")

    if waveform.size == 0:
        raise ValueError("l'audio non contiene campioni")
    if not np.isfinite(waveform).all():
        raise ValueError("l'audio contiene NaN o valori infiniti")

    if sample_rate != TARGET_SAMPLE_RATE:
        divisor = math.gcd(sample_rate, TARGET_SAMPLE_RATE)
        waveform = resample_poly(
            waveform,
            TARGET_SAMPLE_RATE // divisor,
            sample_rate // divisor,
        ).astype(np.float32, copy=False)

    return np.ascontiguousarray(np.clip(waveform, -1.0, 1.0), dtype=np.float32)


def l2_normalize(vector: np.ndarray) -> np.ndarray:
    """Return a finite, one-dimensional vector with unit L2 norm."""
    flattened = np.asarray(vector, dtype=np.float32).reshape(-1)
    if flattened.size == 0 or not np.isfinite(flattened).all():
        raise ValueError("il vettore deve contenere valori finiti")
    norm = float(np.linalg.vector_norm(flattened))
    if norm <= 0.0:
        raise ValueError("non e possibile normalizzare un vettore nullo")
    return flattened / norm


def cosine_similarity(first: np.ndarray, second: np.ndarray) -> float:
    """Return cosine similarity for two non-zero vectors of equal size."""
    first_normalized = l2_normalize(first)
    second_normalized = l2_normalize(second)
    if first_normalized.shape != second_normalized.shape:
        raise ValueError("i vettori devono avere la stessa dimensione")
    similarity = float(np.dot(first_normalized, second_normalized))
    return float(np.clip(similarity, -1.0, 1.0))


def load_classifier(model_directory: Path) -> Any:
    """Load SpeechBrain ECAPA strictly from the external local directory."""
    missing = missing_model_files(model_directory)
    if missing:
        missing_text = ", ".join(missing)
        raise FileNotFoundError(
            f"Modello incompleto in {model_directory}. Mancano: {missing_text}"
        )

    from speechbrain.inference.speaker import EncoderClassifier

    return EncoderClassifier.from_hparams(
        source=str(model_directory),
        savedir=str(model_directory),
        run_opts={"device": "cpu"},
    )


def extract_embedding(
    classifier: Any, waveform: np.ndarray
) -> tuple[np.ndarray, float]:
    """Extract and normalize one ECAPA embedding, returning elapsed seconds."""
    import torch

    batch = torch.from_numpy(waveform).unsqueeze(0)
    started = time.perf_counter()
    with torch.inference_mode():
        embedding = classifier.encode_batch(batch).detach().cpu().numpy()
    elapsed = time.perf_counter() - started

    normalized = l2_normalize(embedding)
    if normalized.size != EMBEDDING_SIZE:
        raise ValueError(
            f"dimensione embedding inattesa: {normalized.size}, "
            f"attesa {EMBEDDING_SIZE}"
        )
    return normalized, elapsed


def read_audio(path: Path) -> tuple[np.ndarray, int]:
    """Read an audio file as float32 through libsndfile."""
    import soundfile as sf

    samples, sample_rate = sf.read(path, dtype="float32", always_2d=False)
    return np.asarray(samples, dtype=np.float32), int(sample_rate)


def embedding_from_file(
    classifier: Any, path: Path
) -> tuple[np.ndarray, float, float]:
    """Read, preprocess, and embed an audio file."""
    samples, sample_rate = read_audio(path)
    waveform = prepare_waveform(samples, sample_rate)
    embedding, elapsed = extract_embedding(classifier, waveform)
    return embedding, elapsed, waveform.size / TARGET_SAMPLE_RATE


def synthetic_waveform(seconds: float = 3.0) -> np.ndarray:
    """Generate a deterministic signal that contains no biometric information."""
    sample_count = int(TARGET_SAMPLE_RATE * seconds)
    timeline = np.arange(sample_count, dtype=np.float32) / TARGET_SAMPLE_RATE
    return (
        0.05 * np.sin(2.0 * np.pi * 220.0 * timeline)
        + 0.03 * np.sin(2.0 * np.pi * 440.0 * timeline)
    ).astype(np.float32)


def print_embedding_result(label: str, embedding: np.ndarray, elapsed: float) -> None:
    """Print the stable diagnostics used by the manual checkpoint."""
    print(f"{label} - dimensione: {embedding.size}")
    print(f"{label} - valori finiti: {bool(np.isfinite(embedding).all())}")
    print(f"{label} - norma L2: {np.linalg.vector_norm(embedding):.6f}")
    print(f"{label} - tempo CPU: {elapsed:.3f} s")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=default_model_directory(),
        help="cartella esterna contenente il modello ECAPA",
    )
    parser.add_argument(
        "--install-model",
        action="store_true",
        help="installa nella cartella esterna la revisione fissata del modello",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="durante l'installazione usa esclusivamente la cache Hugging Face",
    )
    parser.add_argument(
        "--audio",
        type=Path,
        help="estrae due volte l'embedding dello stesso file",
    )
    parser.add_argument(
        "--compare",
        nargs=2,
        type=Path,
        metavar=("PRIMO", "SECONDO"),
        help="confronta due file audio tramite similarita coseno",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    model_directory = args.model_dir.resolve()

    print(f"Modello: {MODEL_ID}")
    print(f"Revisione: {MODEL_REVISION}")
    print(f"Cartella locale: {model_directory}")

    if args.install_model:
        install_pinned_model(model_directory, offline=args.offline)
        print("Modello installato correttamente.")

    classifier = load_classifier(model_directory)
    print("Modello caricato correttamente dalla cartella locale.")

    if args.compare:
        first, first_time, first_duration = embedding_from_file(
            classifier, args.compare[0]
        )
        second, second_time, second_duration = embedding_from_file(
            classifier, args.compare[1]
        )
        print_embedding_result("Primo file", first, first_time)
        print(f"Primo file - durata utile: {first_duration:.3f} s")
        print_embedding_result("Secondo file", second, second_time)
        print(f"Secondo file - durata utile: {second_duration:.3f} s")
        print(f"Similarita coseno: {cosine_similarity(first, second):.6f}")
        return 0

    if args.audio:
        first, first_time, duration = embedding_from_file(classifier, args.audio)
        second, second_time, _ = embedding_from_file(classifier, args.audio)
        print_embedding_result("Prima estrazione", first, first_time)
        print_embedding_result("Seconda estrazione", second, second_time)
        print(f"Durata utile: {duration:.3f} s")
        print(f"Ripetibilita coseno: {cosine_similarity(first, second):.9f}")
        print(f"Differenza massima: {np.max(np.abs(first - second)):.9g}")
        return 0

    waveform = synthetic_waveform()
    first, first_time = extract_embedding(classifier, waveform)
    second, second_time = extract_embedding(classifier, waveform)
    print_embedding_result("Prima estrazione sintetica", first, first_time)
    print_embedding_result("Seconda estrazione sintetica", second, second_time)
    print(f"Ripetibilita coseno: {cosine_similarity(first, second):.9f}")
    print(f"Differenza massima: {np.max(np.abs(first - second)):.9g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
