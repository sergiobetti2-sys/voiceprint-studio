"""Voiceprint Studio - Audio Diagnostics PoC.

Minimal diagnostic window for microphone capture, dBFS metering and a
real-time spectrum. Real recordings are written only to the operating-system
temporary directory, never inside the Git repository.
"""

from __future__ import annotations

import queue
import sys
import tempfile
from pathlib import Path

import numpy as np
import pyqtgraph as pg
import sounddevice as sd
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from scipy.io import wavfile

DBFS_FLOOR = -120.0
MAX_RECORDING_SECONDS = 20.0
SPECTRUM_SIZE = 4096
UI_INTERVAL_MS = 50


def amplitude_to_dbfs(value: float) -> float:
    """Convert a normalized linear amplitude to dBFS."""
    if value <= 0.0:
        return DBFS_FLOOR
    return max(DBFS_FLOOR, 20.0 * float(np.log10(value)))


def calculate_levels(samples: np.ndarray) -> tuple[float, float, float]:
    """Return RMS dBFS, peak dBFS and clipping percentage."""
    if samples.size == 0:
        return DBFS_FLOOR, DBFS_FLOOR, 0.0

    mono = np.asarray(samples, dtype=np.float32).reshape(-1)
    rms = float(np.sqrt(np.mean(np.square(mono, dtype=np.float64))))
    peak = float(np.max(np.abs(mono)))
    clipping_percent = float(np.mean(np.abs(mono) >= 0.999) * 100.0)
    return amplitude_to_dbfs(rms), amplitude_to_dbfs(peak), clipping_percent


def calculate_spectrum(
    samples: np.ndarray, sample_rate: int
) -> tuple[np.ndarray, np.ndarray]:
    """Return frequency and dBFS arrays for the visible 0-8 kHz spectrum."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be greater than zero")

    mono = np.asarray(samples, dtype=np.float32).reshape(-1)
    buffer = np.zeros(SPECTRUM_SIZE, dtype=np.float32)
    if mono.size >= SPECTRUM_SIZE:
        buffer[:] = mono[-SPECTRUM_SIZE:]
    elif mono.size:
        buffer[-mono.size :] = mono

    window = np.hanning(SPECTRUM_SIZE)
    spectrum = np.fft.rfft(buffer * window)
    scale = max(float(np.sum(window)) / 2.0, 1.0)
    magnitude = np.abs(spectrum) / scale
    dbfs = np.maximum(DBFS_FLOOR, 20.0 * np.log10(np.maximum(magnitude, 1e-12)))
    frequencies = np.fft.rfftfreq(SPECTRUM_SIZE, d=1.0 / sample_rate)
    visible = frequencies <= 8_000
    return frequencies[visible], dbfs[visible]


class AudioDiagnostics(QWidget):
    """Small, disposable GUI used to validate the audio stack."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Voiceprint Studio - Audio Diagnostics PoC")
        self.resize(900, 620)

        self.stream: sd.InputStream | None = None
        self.sample_rate = 44_100
        self.audio_queue: queue.Queue[np.ndarray] = queue.Queue(maxsize=64)
        self.recorded_chunks: list[np.ndarray] = []
        self.spectrum_buffer = np.zeros(SPECTRUM_SIZE, dtype=np.float32)
        self.total_frames = 0
        self.overflow_count = 0
        self.queue_drop_count = 0

        self._build_ui()
        self._load_input_devices()

        self.ui_timer = QTimer(self)
        self.ui_timer.setInterval(UI_INTERVAL_MS)
        self.ui_timer.timeout.connect(self._update_from_audio)

    def _build_ui(self) -> None:
        title = QLabel("Diagnostica audio - massimo 20 secondi")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 600;")

        self.device_combo = QComboBox()
        self.start_button = QPushButton("Avvia registrazione")
        self.stop_button = QPushButton("Ferma e salva WAV temporaneo")
        self.stop_button.setEnabled(False)

        self.timer_label = QLabel("0.00 s")
        self.rms_label = QLabel("-120.00 dBFS")
        self.peak_label = QLabel("-120.00 dBFS")
        self.clip_label = QLabel("0.0000%")
        self.overflow_label = QLabel("0")
        self.status_label = QLabel("In attesa")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setMinimumHeight(46)
        self.file_label = QLabel("Nessun file creato")
        self.file_label.setWordWrap(True)

        grid = QGridLayout()
        grid.addWidget(QLabel("Microfono:"), 0, 0)
        grid.addWidget(self.device_combo, 0, 1, 1, 3)
        grid.addWidget(QLabel("Timer:"), 1, 0)
        grid.addWidget(self.timer_label, 1, 1)
        grid.addWidget(QLabel("RMS:"), 1, 2)
        grid.addWidget(self.rms_label, 1, 3)
        grid.addWidget(QLabel("Picco:"), 2, 0)
        grid.addWidget(self.peak_label, 2, 1)
        grid.addWidget(QLabel("Clipping:"), 2, 2)
        grid.addWidget(self.clip_label, 2, 3)
        grid.addWidget(QLabel("Overflow/drop:"), 3, 0)
        grid.addWidget(self.overflow_label, 3, 1)

        self.plot = pg.PlotWidget(title="Spettro in tempo reale")
        self.plot.setLabel("bottom", "Frequenza", units="Hz")
        self.plot.setLabel("left", "Ampiezza", units="dBFS")
        self.plot.setXRange(0, 8_000, padding=0)
        self.plot.setYRange(DBFS_FLOOR, 0, padding=0)
        self.plot.showGrid(x=True, y=True, alpha=0.25)
        self.spectrum_curve = self.plot.plot(pen=pg.mkPen("#26a7e0", width=1))

        controls = QGridLayout()
        controls.addWidget(self.start_button, 0, 0)
        controls.addWidget(self.stop_button, 0, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(grid)
        layout.addWidget(self.status_label)
        layout.addWidget(self.plot, stretch=1)
        layout.addLayout(controls)
        layout.addWidget(self.file_label)

        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

    def _load_input_devices(self) -> None:
        default_input = sd.default.device[0]
        host_apis = sd.query_hostapis()

        for index, device in enumerate(sd.query_devices()):
            if int(device["max_input_channels"]) < 1:
                continue
            api_name = host_apis[int(device["hostapi"])]["name"]
            label = f"{index}: {device['name']} [{api_name}]"
            self.device_combo.addItem(
                label,
                {"index": index, "sample_rate": int(device["default_samplerate"])},
            )
            if index == default_input:
                self.device_combo.setCurrentIndex(self.device_combo.count() - 1)

    def _audio_callback(
        self,
        indata: np.ndarray,
        frames: int,
        time_info: object,
        status: sd.CallbackFlags,
    ) -> None:
        del frames, time_info
        if status.input_overflow:
            self.overflow_count += 1
        try:
            self.audio_queue.put_nowait(indata[:, 0].copy())
        except queue.Full:
            self.queue_drop_count += 1

    def start_recording(self) -> None:
        device_data = self.device_combo.currentData()
        if not device_data:
            QMessageBox.critical(self, "Errore", "Nessun microfono disponibile.")
            return

        self.sample_rate = int(device_data["sample_rate"])
        self.recorded_chunks.clear()
        self.spectrum_buffer.fill(0.0)
        self.total_frames = 0
        self.overflow_count = 0
        self.queue_drop_count = 0
        self._clear_audio_queue()

        try:
            self.stream = sd.InputStream(
                device=int(device_data["index"]),
                channels=1,
                samplerate=self.sample_rate,
                dtype="float32",
                blocksize=0,
                latency="high",
                callback=self._audio_callback,
            )
            self.stream.start()
        except sd.PortAudioError as exc:
            self.stream = None
            QMessageBox.critical(self, "Errore microfono", str(exc))
            return

        self.device_combo.setEnabled(False)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.file_label.setText(
            "Registrazione in corso; il file sara salvato fuori dal repository."
        )
        self.ui_timer.start()

    def _update_from_audio(self) -> None:
        latest: np.ndarray | None = None

        while True:
            try:
                chunk = self.audio_queue.get_nowait()
            except queue.Empty:
                break
            self.recorded_chunks.append(chunk)
            self.total_frames += chunk.size
            latest = chunk
            combined = np.concatenate((self.spectrum_buffer, chunk))
            self.spectrum_buffer = combined[-SPECTRUM_SIZE:]

        if latest is None:
            return

        rms_dbfs, peak_dbfs, clipping_percent = calculate_levels(latest)
        self.rms_label.setText(f"{rms_dbfs:.2f} dBFS")
        self.peak_label.setText(f"{peak_dbfs:.2f} dBFS")
        self.clip_label.setText(f"{clipping_percent:.4f}%")
        self.overflow_label.setText(f"{self.overflow_count}/{self.queue_drop_count}")

        duration = self.total_frames / self.sample_rate
        self.timer_label.setText(f"{duration:.2f} s")
        self._set_level_status(rms_dbfs, peak_dbfs, clipping_percent)
        self._update_spectrum()

        if duration >= MAX_RECORDING_SECONDS:
            self.stop_recording()

    def _set_level_status(
        self, rms_dbfs: float, peak_dbfs: float, clipping_percent: float
    ) -> None:
        if clipping_percent > 0.0 or peak_dbfs >= -3.0:
            text = "ROSSO - livello eccessivo / rischio clipping"
            color = "#c62828"
        elif rms_dbfs < -35.0:
            text = "BLU - segnale troppo basso"
            color = "#1565c0"
        else:
            text = "VERDE - livello utilizzabile"
            color = "#2e7d32"

        self.status_label.setText(text)
        self.status_label.setStyleSheet(
            f"background: {color}; color: white; font-size: 16px; font-weight: 600;"
        )

    def _update_spectrum(self) -> None:
        frequencies, dbfs = calculate_spectrum(self.spectrum_buffer, self.sample_rate)
        self.spectrum_curve.setData(frequencies, dbfs)

    def stop_recording(self) -> None:
        if self.stream is None:
            return

        self.ui_timer.stop()
        self.stream.stop()
        self.stream.close()
        self.stream = None
        self._update_from_audio()

        self.device_combo.setEnabled(True)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        if not self.recorded_chunks:
            self.file_label.setText("Nessun campione audio acquisito.")
            return

        audio = np.concatenate(self.recorded_chunks)
        pcm16 = np.int16(np.clip(audio, -1.0, 1.0) * 32_767)
        output_directory = Path(tempfile.gettempdir()) / "VoiceprintStudioPoC"
        output_directory.mkdir(parents=True, exist_ok=True)
        output_path = output_directory / "audio_diagnostic.wav"
        wavfile.write(output_path, self.sample_rate, pcm16)

        rms_dbfs, peak_dbfs, clipping_percent = calculate_levels(audio)
        self.file_label.setText(
            "Salvato: "
            f"{output_path} | RMS complessivo {rms_dbfs:.2f} dBFS | "
            f"picco {peak_dbfs:.2f} dBFS | clipping {clipping_percent:.4f}%"
        )

    def _clear_audio_queue(self) -> None:
        while True:
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                return

    def closeEvent(self, event: object) -> None:
        if self.stream is not None:
            self.stream.abort()
            self.stream.close()
            self.stream = None
        event.accept()


def main() -> int:
    app = QApplication(sys.argv)
    pg.setConfigOptions(antialias=False)
    window = AudioDiagnostics()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
