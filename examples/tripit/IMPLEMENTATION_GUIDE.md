# TripIt Entity Types: Bulk Import CLI Integration Guide

This document provides implementation guidance for integrating the TripIt Pydantic
entity/edge type models (defined in `tripit_entity_types.py`) into the
openclaw-memory-graphiti bulk import CLI tooling.

## What the Models Provide

`tripit_entity_types.py` exports three configuration dicts:

| Export | Type | Count | Purpose |
|---|---|---|---|
| `ENTITY_TYPES` | `dict[str, type[BaseModel]]` | 16 types | Node classification for LLM extraction |
| `EDGE_TYPES` | `dict[str, type[BaseModel]]` | 14 types | Relationship classification |
| `EDGE_TYPE_MAP` | `dict[tuple[str, str], list[str]]` | 48 entries | Constrains which edges are valid between which entity pairs |

These are ready-to-use with Graphiti's `add_episode()` and `add_episode_bulk()`.

## Core Integration Pattern

Graphiti does **not** store entity/edge types on the client instance. They must be
passed on every ingestion call. The recommended pattern for CLI tools:

```python
from graphiti_core import Graphiti
from graphiti_core.utils.bulk_utils import RawEpisode
from graphiti_core.nodes import EpisodeType
from tripit_entity_types import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP

# 1. Initialize the Graphiti client once (no type params here)
client = Graphiti(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
await client.build_indices_and_constraints()

# 2. Pass type dicts on every ingestion call
await client.add_episode(
    name=episode_name,
    episode_body=content,
    source_description='TripIt API export',
    reference_time=reference_time,
    source=EpisodeType.json,       # or EpisodeType.text
    group_id=group_id,
    entity_types=ENTITY_TYPES,     # <-- pass every time
    edge_types=EDGE_TYPES,         # <-- pass every time
    edge_type_map=EDGE_TYPE_MAP,   # <-- pass every time
)
```

## Implementation Steps

### 1. Make the models importable

The `tripit_entity_types.py` file needs to be accessible to the CLI tool. Options:

- **Copy the file** into the openclaw-memory-graphiti package
- **Add graphiti (this repo) as a dependency** and import from `examples/tripit/`
- **Vendor the models** into a `models/` or `entity_types/` module in the CLI package

The models only depend on `pydantic` (BaseModel, Field) -- no Graphiti imports.

### 2. Wire the types into the bulk import path

Find where the CLI currently calls `graphiti_client.add_episode()` or
`graphiti_client.add_episode_bulk()` and add the three type parameters. If the CLI
currently has no entity_types support at all, the changes are:

```python
# Before (no custom types -- Graphiti extracts generic "Entity" nodes):
await client.add_episode(
    name=name,
    episode_body=body,
    source_description=desc,
    reference_time=ref_time,
    group_id=gid,
)

# After (with TripIt types):
await client.add_episode(
    name=name,
    episode_body=body,
    source_description=desc,
    reference_time=ref_time,
    group_id=gid,
    entity_types=ENTITY_TYPES,
    edge_types=EDGE_TYPES,
    edge_type_map=EDGE_TYPE_MAP,
)
```

The same applies to `add_episode_bulk()` -- it accepts the same type parameters.

### 3. Consider making type selection configurable

If the CLI will support multiple domains (not just TripIt), consider a pattern like:

```python
# registry of available type sets
TYPE_SETS = {
    'tripit': {
        'entity_types': ENTITY_TYPES,
        'edge_types': EDGE_TYPES,
        'edge_type_map': EDGE_TYPE_MAP,
    },
    # future: 'salesforce': { ... }, 'jira': { ... }
}

# CLI flag: --entity-schema tripit
schema = TYPE_SETS.get(args.entity_schema)
await client.add_episode(
    ...,
    entity_types=schema['entity_types'] if schema else None,
    edge_types=schema['edge_types'] if schema else None,
    edge_type_map=schema['edge_type_map'] if schema else None,
)
```

Passing `None` for all three reverts to Graphiti's default behavior (generic "Entity"
nodes with unconstrained edge types).

### 4. Source type considerations for TripIt data

Graphiti supports three `EpisodeType` values for the `source` parameter:

| EpisodeType | When to use |
|---|---|
| `EpisodeType.json` | Raw TripIt API JSON responses -- Graphiti will parse the structure |
| `EpisodeType.text` | Pre-formatted text descriptions of trips/itineraries |
| `EpisodeType.message` | Conversational content (e.g., "I booked a flight to NYC") |

For bulk importing TripIt API data, `EpisodeType.json` is likely the right choice.
The `episode_body` should be the JSON string of the TripIt object.

### 5. Group ID strategy

The `group_id` partitions the graph. Sensible strategies for TripIt:

- **Per-user**: `group_id = f"tripit_user_{user_id}"` -- each user's trips in a
  separate partition
- **Per-trip**: `group_id = f"trip_{trip_id}"` -- each trip isolated
- **Global**: Single `group_id` for all data -- enables cross-trip queries but
  increases dedup complexity

Entity deduplication happens within a group_id partition, so entities in different
groups are never deduplicated against each other.

## Things to Be Aware Of

### Entity deduplication is name-based, not type-based

Two entities with the same name but different types (e.g., an Airport named "SFO" and
a City named "SFO") will be considered duplicates by the exact/fuzzy matching stages.
The LLM judgment stage receives type context and may differentiate them, but this is
not guaranteed. Consider using more distinctive names where possible (e.g., "San
Francisco International Airport (SFO)" vs. "San Francisco").

### Edge type map uses entity type names as keys, not class references

The edge type map keys are string tuples like `('Flight', 'Airport')`, matching the
keys in the `ENTITY_TYPES` dict. If you rename a key in `ENTITY_TYPES`, you must
update the `EDGE_TYPE_MAP` entries to match.

### The `'Entity'` type in edge_type_map

Some edge type map entries use `'Entity'` as a target type (e.g.,
`('Flight', 'Entity'): ['BOOKED_WITH']`). This is Graphiti's built-in default label
that all entity nodes carry. It acts as a wildcard for entities that don't match any
custom type. In the TripIt models, `BOOKED_WITH` edges use `Entity` as the target
because booking sites/agencies aren't modeled as a dedicated entity type.

### Validation happens on every call

`validate_entity_types()` runs at the top of every `add_episode()` /
`add_episode_bulk()` call. It checks that no field name in any entity type model
collides with EntityNode's reserved field names: `uuid`, `name`, `group_id`, `labels`,
`created_at`, `name_embedding`, `summary`, `attributes`. The models in
`tripit_entity_types.py` have been validated and pass this check.

### No edge type validation exists

Unlike entity types, there is no `validate_edge_types()` function. Edge type models
are not checked for field name collisions. However, the same caution applies -- avoid
using field names that collide with `EntityEdge` base fields.

### Models are not persisted in the graph

The Pydantic model definitions themselves are not stored in Neo4j/FalkorDB. What gets
persisted is:

- **Entity nodes**: type name becomes a label (e.g., `(:Flight)`), field values go
  into the `attributes` dict property
- **Entity edges**: relation type name becomes the edge type, field values go into
  the `attributes` dict property

This means you can evolve the models over time (add/remove fields) without migrating
existing graph data. Old entities keep their stored attributes; new entities get the
updated field set.
