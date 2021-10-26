# Toy Pipeline

This pipeline is intended to present the minimum possible orchestration.

The work criteria are:

- belongs to a ToL sample

No results are written anywhere of consequence. There are no staging requirements. The computation itself is trivial so as to not distract from core functionality needs.

It will prove the viability of the following componenents:

- Orchestration schema
- Work discovery life cycle
- Agent claiming of work and status updates
- Operation of a black box

What it does not do:

- Archive anything
- Use a container of any kind
- Use a scheduler such as WR to run work

Each component talks to the schema directly. This is not good for the long term.

**work_finder.py** looks for the specific work requirements and registers runs with the schema
**agent.py** picks individual jobs and claims them from the schema. It then executes them
**pipeline.py** is a "black box" implementation of the business logic.
