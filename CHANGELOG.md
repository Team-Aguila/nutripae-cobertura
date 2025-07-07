# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- New endpoints for beneficiary and coverage CRUD operations.
- Parametric tables.
- Missing models and campus CRUD.
- Institution CRUD.
- Towns CRUD (**towns**).
- Client SDK for exporting types (**client-sdk**).
- Department routes to the main application (**main**).
- Department schemas (**schemas**).
- Department routes (**routes**).
- Department repository (**repositories**).
- Initial database models (**models**).
- Database configuration (**database.py**).
- Core application configuration (**core**).

### Fixed
- Corrected relationships in database models (**models**).
- Corrected database name in `docker-compose.yml` to `pae_cobertura` (**docker-compose.yml**).
- All feat messages that were not correctly classified.
