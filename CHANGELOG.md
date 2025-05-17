# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- [Feature] New student dashboard UI components
- [API] Endpoint for bulk exercise submissions

### Changed
- [Refactor] Authentication service to use JWT claims
- [Perf] Optimized database queries in StudentService

### Fixed
- [Security] Patched XSS vulnerability in news comments
- [Bug] File uploads failing >2MB

## [1.0.0] - 2023-11-15
### Initial Release
- Core university management features
- Student/lecturer portals
- Exercise submission system
- News announcement system