"""Deterministic tests for the Audio Diagnostics proof of concept."""

from __future__ import annotations

import numpy as np
import pytest

from poc.audio_diagnostics import (
    DBFS_FLOOR,
    SPECTRUM_SIZE,
    amplitude_to_dbfs,
    calculate_levels,
    calculate_spectrum,
)


def test_amplitude_to_dbfs_reference_values() -> None:
    assert amplitude_to_dbfs(0.0) == DBFS_FLOOR
    assert amplitude_to_dbfs(1.0) == pytest.approx(0.0, abs=1e-12)
    assert amplitude_to_dbfs(0.5) == pytest.approx(-6.0206, abs=1e-4)


def test_full_scale_sine_has_expected_rms_and_peak() -> None:
    sample_rate = 16_000
    time = np.arange(sample_rate, dtype=np.float64) / sample_rate
    samples = np.sin(2.0 * np.pi * 1_000.0 * time).astype(np.float32)

    rms_dbfs, peak_dbfs, clipping_percent = calculate_levels(samples)

    assert rms_dbfs == pytest.approx(-3.0103, abs=1e-3)
    assert peak_dbfs == pytest.approx(0.0, abs=1e-6)
    assert clipping_percent > 0.0


def test_half_scale_sine_has_expected_levels() -> None:
    sample_rate = 16_000
    time = np.arange(sample_rate, dtype=np.float64) / sample_rate
    samples = (0.5 * np.sin(2.0 * np.pi * 1_000.0 * time)).astype(np.float32)

    rms_dbfs, peak_dbfs, clipping_percent = calculate_levels(samples)

    assert rms_dbfs == pytest.approx(-9.0309, abs=1e-3)
    assert peak_dbfs == pytest.approx(-6.0206, abs=1e-4)
    assert clipping_percent == 0.0


def test_clipping_percentage_uses_defined_threshold() -> None:
    samples = np.array([0.0, 0.998, 0.999, -0.999, 1.0], dtype=np.float32)

    _, _, clipping_percent = calculate_levels(samples)

    assert clipping_percent == pytest.approx(60.0)


def test_spectrum_detects_one_kilohertz_tone() -> None:
    sample_rate = 16_000
    time = np.arange(SPECTRUM_SIZE, dtype=np.float64) / sample_rate
    samples = (0.5 * np.sin(2.0 * np.pi * 1_000.0 * time)).astype(np.float32)

    frequencies, spectrum_dbfs = calculate_spectrum(samples, sample_rate)
    dominant_frequency = float(frequencies[int(np.argmax(spectrum_dbfs))])
    fft_bin_width = sample_rate / SPECTRUM_SIZE

    assert dominant_frequency == pytest.approx(1_000.0, abs=fft_bin_width)
    assert frequencies[0] == 0.0
    assert frequencies[-1] == 8_000.0


def test_spectrum_rejects_invalid_sample_rate() -> None:
    with pytest.raises(ValueError, match="sample_rate"):
        calculate_spectrum(np.zeros(SPECTRUM_SIZE, dtype=np.float32), 0)
