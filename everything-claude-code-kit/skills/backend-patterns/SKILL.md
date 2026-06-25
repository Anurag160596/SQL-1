---
name: backend-patterns
description: API, database, and caching patterns. Use when designing or reviewing backend services for robust, scalable patterns.
---

# Backend Patterns

Guidance for API, database, and caching layers.

- Validate input at the boundary; never trust client data.
- Use idempotency keys for unsafe retried operations.
- Cache with explicit TTLs and invalidation; avoid unbounded caches.
- Paginate list endpoints; never return unbounded result sets.
- Wrap external calls with timeouts and circuit breakers.
