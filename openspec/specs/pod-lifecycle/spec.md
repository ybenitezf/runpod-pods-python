## ADDED Requirements

### Requirement: Create pod with specified GPU and image
The system SHALL create a RunPod pod with the specified GPU type and Docker image, returning the pod ID upon success.

#### Scenario: Successful pod creation
- **WHEN** the user runs the create_pod function with valid GPU type and image
- **THEN** the function returns a pod object containing an ID
- **AND** the pod is created in CREATING or INITIALIZING state

#### Scenario: Invalid GPU type
- **WHEN** the user specifies a GPU type that is not available
- **THEN** the function raises an appropriate error with a clear message

#### Scenario: Invalid API key
- **WHEN** the API key is invalid or missing
- **THEN** the function raises an authentication error

### Requirement: Wait for pod to reach RUNNING state
The system SHALL poll the pod status at regular intervals until it reaches RUNNING state or times out.

#### Scenario: Pod reaches RUNNING state
- **WHEN** the pod's desiredStatus is RUNNING AND runtime is not null
- **THEN** the function returns the pod object indicating it is ready

#### Scenario: Pod fails to start
- **WHEN** the pod status changes to a terminal failure state (not RUNNING)
- **THEN** the function raises an error indicating pod failed to start

#### Scenario: Timeout waiting for pod
- **WHEN** the pod does not reach RUNNING state within the timeout period
- **THEN** the function raises a TimeoutError

#### Implementation Notes
- RunPod API returns `desiredStatus` field (not `status`) to indicate the target state
- The pod is truly ready only when BOTH `desiredStatus == "RUNNING"` AND `runtime` is not null
- When `runtime` is null, the container is still initializing even if desiredStatus is RUNNING

### Requirement: Terminate pod
The system SHALL terminate the specified pod, removing it from the account.

#### Scenario: Successful pod termination
- **WHEN** the user calls terminate_pod with a valid pod ID
- **THEN** the pod is terminated and removed

#### Scenario: Terminate non-existent pod
- **WHEN** the user attempts to terminate a pod that does not exist
- **THEN** the function raises an appropriate error

### Requirement: Full lifecycle orchestration
The system SHALL execute the complete pod lifecycle: create, wait for ready, list pods, and terminate.

#### Scenario: Complete lifecycle succeeds
- **WHEN** the user runs the main lifecycle function
- **THEN** the pod is created
- **AND** the system waits for the pod to reach RUNNING
- **AND** all pods are listed
- **AND** the created pod is terminated
- **AND** the function returns success

#### Scenario: Lifecycle fails at wait step
- **WHEN** the pod creation succeeds but waiting times out
- **THEN** the system terminates the pod to clean up
- **AND** returns an error indicating timeout

#### Scenario: Lifecycle fails at create step
- **WHEN** the pod creation fails
- **THEN** no cleanup is needed
- **AND** the error is propagated to the user
