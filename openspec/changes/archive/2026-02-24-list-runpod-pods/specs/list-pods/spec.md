## ADDED Requirements

### Requirement: List pods displays all RunPod pods
The system SHALL display all RunPod pods in a formatted table showing name, ID, status, uptime, and GPU type.

#### Scenario: Successful pod listing
- **WHEN** the user runs the list-pods script with valid API key
- **THEN** the script displays a table with all pods

#### Scenario: No pods exist
- **WHEN** the user has no pods in their account
- **THEN** the script displays an empty table or appropriate message

### Requirement: API key loaded from .env file
The system SHALL load the RunPod API key from a .env file using python-dotenv.

#### Scenario: .env file exists with valid key
- **WHEN** the .env file contains RUNPOD_API_KEY
- **THEN** the script uses that key to authenticate

#### Scenario: .env file missing
- **WHEN** the .env file does not exist
- **THEN** the script displays an error message and exits

#### Scenario: API key missing from .env
- **WHEN** the .env file exists but RUNPOD_API_KEY is not set
- **THEN** the script displays an error message and exits

### Requirement: Invalid API key handled gracefully
The system SHALL display a clear error when the API key is invalid.

#### Scenario: Invalid API key
- **WHEN** the API key is incorrect
- **THEN** the script displays an authentication error message
