## ADDED Requirements

### Requirement: List official RunPod images
The system SHALL allow users to programmatically retrieve a list of official RunPod Docker images from templates via the REST API.

#### Scenario: Successful API call with valid credentials
- **WHEN** user runs the script with a valid RUNPOD_API_KEY
- **THEN** the script SHALL display a table of official images with Template Name and Docker Image URI
- **AND** the table SHALL only include templates where `isRunpod` is `True`

#### Scenario: API key missing
- **WHEN** RUNPOD_API_KEY is not set in .env
- **THEN** the script SHALL print an error message to stderr
- **AND** return exit code 1

#### Scenario: API connection failure
- **WHEN** the RunPod API is unreachable or returns an error
- **THEN** the script SHALL catch the exception
- **AND** print an error message to stderr
- **AND** return exit code 1

#### Scenario: API returns empty list
- **WHEN** the API call succeeds but returns no templates
- **THEN** the script SHALL print "No official images found."
