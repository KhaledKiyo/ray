# PDA Voice Monitor - Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-07-05

### Added
- Initial release
- Configuration system with JSON and environment variable support
- VoiceEngine class for Piper TTS synthesis with error handling
- PowerMonitor class for real-time power event detection (Linux only)
- Comprehensive logging with configurable levels
- CLI with argument parsing (--once, --verbose, --config options)
- Config validation with helpful error messages
- Basic test coverage for config and voice engine
- Systemd service setup documentation
- Threading for non-blocking audio playback
- State tracking to prevent duplicate power event announcements
- Error handling in file operations and hardware access

### Documentation
- Comprehensive README with usage examples
- Setup and installation instructions
- Troubleshooting guide
- Systemd service configuration guide
- API documentation in docstrings
- Contributing guidelines
- Quick start guide

### Known Limitations
- Linux only (requires pyudev for power monitoring)
- May require elevated privileges for power supply access
- Audio synthesis performance depends on system resources
- Test suite covers configuration and initialization; hardware integration tests require Linux environment with udev/audio access

## Future Roadmap

### Planned for v1.1.0
- [ ] Support for custom audio output devices
- [ ] Configuration GUI for easier setup
- [ ] More voice model options
- [ ] Performance metrics in debug mode

### Planned for v2.0.0
- [ ] Cross-platform support (macOS, Windows)
- [ ] Web-based dashboard
- [ ] Integration with system power profiles
- [ ] Plugin system for custom announcements
