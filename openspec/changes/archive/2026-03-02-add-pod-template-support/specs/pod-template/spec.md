## ADDED Requirements

### Requirement: Load pod configuration from .env
The system SHALL load pod configuration from .env file including gpu_type_id, image_name, gpu_count, container_disk_in_gb, volume_in_gb, volume_mount_path, ports, and env variables.

#### Scenario: All configuration provided
- **WHEN** .env contains all pod configuration options
- **THEN** pod is created with all provided values

#### Scenario: Optional configuration not provided
-env omits optional **WHEN** . configuration (volume, ports, env)
- **THEN** pod is created with only required/provided values using defaults

### Requirement: Create pod with full configuration
The system SHALL create a RunPod pod using configuration loaded from .env file.

#### Scenario: Pod created successfully
- **WHEN** create_pod() is called with valid configuration
- **THEN** a new pod is created on RunPod and its ID is returned

#### Scenario: Pod creation fails
- **WHEN** create_pod() is called with invalid configuration or API error
- **THEN** an appropriate error is raised with details

### Requirement: List available GPU types
The system SHALL provide a script to list available GPU types with their details for user evaluation.

#### Scenario: GPU list retrieved
- **WHEN** list_gpus.py script is executed
- **THEN** a table of available GPUs is displayed with id, displayName, and memoryInGb

### Requirement: Pause for user verification
The system SHALL pause execution after the pod is ready, prompting the user to verify the pod in the RunPod console before continuing with cleanup.

#### Scenario: User confirms continuation
- **WHEN** pod is ready and user presses Enter/confirms
- **THEN** script continues with termination and cleanup

#### Scenario: User aborts
- **WHEN** pod is ready and user presses Ctrl+C or aborts
- **THEN** script exits without cleaning up (user can manually terminate later)
