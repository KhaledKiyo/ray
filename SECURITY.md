# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by opening a confidential security advisory on GitHub (select "Report a vulnerability" when creating an issue).

**Do not publicly disclose the vulnerability until a fix is available.**

### What to include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge your report and provide updates on progress toward a fix.

## Security Best Practices

When using PDA Voice Monitor:

1. **File Permissions**: Protect your `config.json` as it may contain sensitive paths
2. **Model Files**: Keep ONNX models in a secure location
3. **Logging**: Be cautious with debug logs in shared environments
4. **System Access**: Running with sudo may be required for power monitoring

## Dependencies

We regularly monitor our dependencies for security updates:
- numpy
- sounddevice
- pyudev
- onnxruntime
- piper-tts

Security updates are applied promptly.
