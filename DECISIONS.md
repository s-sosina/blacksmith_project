# Architectural Decisions

## Sprint 1: Runtime and Stack Selection

### The Question
The language was never the decision. The decision was: **how many runtimes do we operate for one HTTP endpoint, and who has to be able to fix it at 2am?**

### The Axis
We are building a single-endpoint ML scoring service. The scoring libraries (biomechanics, signal processing, ML inference) are Python-native. The question is whether we:
- (A) Run one Python runtime that handles both HTTP and scoring
- (B) Split into two runtimes (e.g., Go for HTTP, Python for scoring)

### The Decision
**One Python runtime (FastAPI).** We operate one deployable, one runtime, one team fixes it at 2am.

### Rejected Alternatives (with concrete costs)

**Go for HTTP + Python sidecar for scoring:**
- *Gains:* Static binary, trivial deploys, better cold start, lower memory per instance.
- *Costs:* Two deployables, two runtimes, a new failure mode between them (network/serialization overhead), two codebases to maintain, two sets of dependencies to patch.
- *Verdict:* We'd pay operational complexity to avoid Python's cold start. Not worth it for one endpoint.

**Node.js for HTTP + Python sidecar:**
- *Gains:* Same as Go (static binary, fast cold start).
- *Costs:* Same as Go (two runtimes, two deployables). Plus, Node's ML ecosystem is weaker than Python's, so we'd still need the Python sidecar.
- *Verdict:* Same tradeoff as Go, no additional benefit.

**Django instead of FastAPI:**
- *Gains:* Built-in admin panel, ORM, templating.
- *Costs:* Heavy framework for a pure API service. We don't need a database ORM, admin panel, or HTML templates. We'd be shipping and maintaining code we don't use.
- *Verdict:* Over-engineered for this use case.

**Flask instead of FastAPI:**
- *Gains:* Simpler, more mature.
- *Costs:* Lacks native async. Wearable telemetry ingestion will need async throughput as we scale. Flask would block on I/O.
- *Verdict:* Would require re-architecture when we hit scale.

### What This Choice Cost Us
The Python mono-stack buys us one runtime and one deployable. It costs us:
- **Slower cold start** (Python is slower to boot than Go/Node)
- **Higher memory per instance** (Python's runtime is heavier)
- **API and model code share the same deploy cadence** (if the model code breaks, the API goes down too)

### What Flips the Call
This is right **while scoring is one endpoint owned by one team.** The moment:
- A second model needs a different runtime (e.g., Rust for ultra-low-latency inference)
- Scoring latency starts competing with API latency under load (e.g., model inference takes 500ms and blocks the HTTP thread)
- The API team and ML team become separate teams with different deploy cadences

...the mono-stack stops being right and we split the service.

### How We'll Know Early If We're Wrong
The whole call rests on "one team operates everything." If in the first month:
- The API team keeps having to touch model code to deploy API changes
- Model experiments are blocked by API release cycles
- We're spending more than 20% of sprint time on deploy coordination between "API" and "model" code

...that premise is already breaking and we need to revisit the decision.