# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Analysis of project requirements: RFID card reading, push button, servo-driven gate, known-card validation, and BLE / XBee communication.
- Repository hierarchy:
  - `pi_b/hardware/` – drivers for the button, RFID reader and servo.
  - `pi_b/logic/` – gate control and known-card lookup.
  - `pi_b/transport/` – BLE and XBee communication.
  - `pi_b/__main__.py` – entry point (`python -m pi_b`).
  - `tests/` – test suite.
- `pi_b/config.py` – loads settings from `.env` at the repo root and exposes `CARDS_FILE`.
- `.env.example` and `cards.example.json` templates.
- `requirements.txt` with `python-dotenv`.
- `.gitignore` covering secrets (`.env`, `cards.json`), Python caches and virtual environments.