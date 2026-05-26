## Authentication & identity

## What to build

Implement authentication for all four roles — Student, Teacher, CenterAdmin, PlatformAdmin — using mobile number as the sole identity. No separate username. Two auth methods: mobile number + password, and mobile number + OTP.

Use fastapi-users as the auth framework. All roles share the same identity model; role is a field on the user record. JWT tokens are issued on successful login and validated on all protected endpoints.

## Acceptance criteria

- [ ] Mobile number is the identity field across all roles; no username field exists
- [ ] Mobile + password login returns a JWT
- [ ] Mobile + OTP login flow: request OTP endpoint sends OTP (stubbed in dev), verify OTP endpoint returns JWT
- [ ] Role field (Student / Teacher / CenterAdmin / PlatformAdmin) is present on the user record
- [ ] Protected endpoints return 401 when no token is provided and 403 when the role is insufficient
- [ ] Passwords are hashed; plaintext passwords are never stored

## Blocked by

- #1 Local dev environment
