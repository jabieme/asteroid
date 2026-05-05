This repository is a small PyGame-based asteroid demo. The goal of these instructions is to help an AI coding agent be productive quickly by describing the project structure, runtime flow, conventions, and useful edit guidance.

Key files
- `main.py` — game entrypoint and loop. Creates three sprite groups: `updatable`, `drawable`, and `asteroids`. It wires sprite classes by assigning `Class.containers = (...)` before instantiation. See how `Player`, `Asteroid`, and `AsteroidField` are registered.
- `player.py` — player ship (triangle) implemented as `Player(CircleShape)`. Movement and rotation are driven by direct keyboard checks in `update()`.
- `asteroid.py` — `Asteroid(CircleShape)` draws a circle and updates position by velocity.
- `asteroidfield.py` — spawns asteroids from screen edges on a timer. Uses constants for spawn rates and sizes; calls `Asteroid(...)` and assigns `velocity` after creation.
- `circleshape.py` — lightweight base `CircleShape(pygame.sprite.Sprite)` providing `position`, `velocity`, `radius`, and `collides_with()` helper. Subclasses are expected to override `draw()` and `update()`.
- `constants.py` — single place for screen size, player/asteroid tuning values and rates.
- `logger.py` — lightweight runtime state logger writing `game_state.jsonl` and `game_events.jsonl`. `main.py` calls `log_state()` once per frame; the logger samples groups and local variables to produce JSONL snapshots.

Architecture & data flow (short)
- main loop (`main.py`) holds three groups: sprites are split by responsibility: `updatable` (update each tick), `drawable` (draw each frame), and `asteroids` (asteroid-specific group used by `logger` and for counting). Classes opt-in by setting `Class.containers` before instantiation.
- `AsteroidField` is a manager/sprite that lives in `updatable` and periodically spawns `Asteroid` instances at screen edges. Asteroids update their `position` using `velocity * dt` each tick.
- `Player` reads keyboard state inside `update()` and mutates `position` and an internal `__rotation` value. Rendering uses `triangle()` helper.

Conventions & patterns to follow
- Use pygame's sprite groups and the `Class.containers` pattern for auto-registration on construction (see `main.py` order of assignment). When adding new sprite classes, ensure they call `super().__init__(self.containers)` or set `containers` before creating instances.
- Keep numeric tuning in `constants.py` (speeds, radii, spawn rates). Prefer adding new knobs there rather than hardcoding numbers in business logic.
- `update(self, dt)` methods expect delta seconds (float). Use `dt` for all time-based motion and rotation.
- `draw(self, screen)` should only render; avoid heavy logic or I/O in draw.
- Use `logger.log_state()` and `logger.log_event()` for new instrumentation; entries are JSONL files in repo root. Avoid changing their schema unless updating `logger.py` too.

Developer workflows
- Run the game locally: Ensure you have a Python environment with `pygame` installed (pyproject references README but no explicit env here). Typical steps:
  - Create and activate a venv (python -m venv .venv; source .venv/bin/activate)
  - Install pygame (pip install pygame)
  - Run: `python main.py`
- There are no automated tests or CI configured in the repo. Changes should be validated by running the game and observing console/log outputs.

Quick examples (in-repo references)
- To add a new projectile sprite:
  - Create `Projectile(CircleShape)` in a new file or `circleshape.py`.
  - Set `Projectile.containers = (updatable, drawable)` in `main.py` before constructing.
  - Implement `update(self, dt)` to move by `self.velocity * dt` and `draw(self, screen)` to render.

Edge cases & pitfalls
- The `logger` samples only up to `_SPRITE_SAMPLE_LIMIT` sprites per group; tests that rely on full dumps should not assume complete lists.
- `Player.__rotation` is private and not exposed as `rotation` attribute — logging tries to access `rotation` and will not record it for `Player` unless you add a `rotation` property.
- `CircleShape.__init__` will call `super().__init__(self.containers)` only if `containers` attribute exists on the class; ensure `Class.containers` is assigned before instantiation to avoid missing group membership.

What to change cautiously
- Changing sprite group names, the `Class.containers` pattern, or the `logger` output schema will require updates across `main.py`, `logger.py`, and any code that relies on group membership.

If something is unclear or you want me to expand on any area (examples, tests, or adding CI), tell me which part to deepen and I'll iterate.
