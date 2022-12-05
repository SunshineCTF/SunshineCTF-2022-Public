# Timely

Timing attack against authentication system.

## Walkthrough

- Open page
- Visit /robots.txt
- Visit /dev
- Visit /dev/users
- Visit /login
- Attempt to login with the active user `anri`
- Realize that the HTTP Response has a `Debug-Lag-Fix` header with a time
- Realize that Timely -> Timing attack for the response
- Begin building up the SHA-1 hash as the lag goes up
- Flag
