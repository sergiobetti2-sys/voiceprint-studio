"""Deterministic tests for ECAPA preprocessing and comparison helpers."""

from __future__ import annotations

import numpy as np
import pytest

from poc.ecapa_feasibility import (
    MODEL_FILE_SOURCES,
    TARGET_SAMPLE_RATE,
    cosine_similarity,
    l2_normalize,
    prepare_waveform,
    synthetic_waveform,
)


def test_model_label_encoder_uses_repository_source_name() -> None:
    assert MODEL_FILE_SOURCES["label_encoder.ckpt"] == "label_encoder.txt"


def test_prepare_waveform_preserves_mono_16_khz() -> None:
    samples = synthetic_waveform(seconds=1.0)

    prepared = prepare_waveform(samples, TARGET_SAMPLE_RATE)

    assert prepared.dtype == np.float32
    assert prepared.shape == (TARGET_SAMPLE_RATE,)
    assert np.array_equal(prepared, samples)


def test_prepare_waveform_downmixes_stereo() -> None:
    left = np.full(100, 0.4, dtype=np.float32)
    right = np.full(100, 0.2, dtype=np.float32)
    stereo = np.column_stack((left, right))

    prepared = prepare_waveform(stereo, TARGET_SAMPLE_RATE)

    assert prepared == pytest.approx(np.full(100, 0.3, dtype=np.float32))


def test_prepare_waveform_resamples_44100_to_16000() -> None:
    source_rate = 44_100
    timeline = np.arange(source_rate, dtype=np.float32) / source_rate
    samples = np.sin(2.0 * np.pi * 440.0 * timeline).astype(np.float32)

    prepared = prepare_waveform(samples, source_rate)

    assert prepared.dtype == np.float32
    assert prepared.shape == (TARGET_SAMPLE_RATE,)
    assert np.isfinite(prepared).all()


@pytest.mark.parametrize("sample_rate", [0, -1])
def test_prepare_waveform_rejects_invalid_sample_rate(sample_rate: int) -> None:
    with pytest.raises(ValueError, match="sample_rate"):
        prepare_waveform(np.ones(10, dtype=np.float32), sample_rate)


def test_prepare_waveform_rejects_non_finite_audio() -> None:
    samples = np.array([0.0, np.nan], dtype=np.float32)

    with pytest.raises(ValueError, match="NaN"):
        prepare_waveform(samples, TARGET_SAMPLE_RATE)


def test_l2_normalize_produces_unit_vector() -> None:
    normalized = l2_normalize(np.array([3.0, 4.0], dtype=np.float32))

    assert normalized == pytest.approx(np.array([0.6, 0.8], dtype=np.float32))
    assert np.linalg.vector_norm(normalized) == pytest.approx(1.0)


def test_cosine_similarity_reference_values() -> None:
    horizontal = np.array([1.0, 0.0], dtype=np.float32)
    vertical = np.array([0.0, 1.0], dtype=np.float32)

    assert cosine_similarity(horizontal, horizontal) == pytest.approx(1.0)
    assert cosine_similarity(horizontal, vertical) == pytest.approx(0.0)
    assert cosine_similarity(horizontal, -horizontal) == pytest.approx(-1.0)


def test_cosine_similarity_is_bounded_after_float32_rounding() -> None:
    vector = np.array(
        [0.34558418, 0.82161814, 0.33043706],
        dtype=np.float32,
    )

    assert cosine_similarity(vector, vector) == 1.0


def test_cosine_similarity_rejects_different_sizes() -> None:
    with pytest.raises(ValueError, match="stessa dimensione"):
        cosine_similarity(np.ones(2, dtype=np.float32), np.ones(3, dtype=np.float32))
