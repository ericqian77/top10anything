## Ranking Models

### RankedItem
- `rank`: Integer (1-10)
- `name`: String (2-100 chars)
- `score`: Float (0-10)
- `key_attributes`: 3-5 unique strings
- `description`: 50-500 characters

### RankingResult
- `topic`: Topic name (3-50 chars)
- `generated_at`: UTC timestamp
- `rankings`: Exactly 10 ranked items
- `sources`: At least 1 source URL
- `methodology`: 100+ characters analysis

# Data Models Documentation

## RankedItem Model

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| rank | int | 1-10 (inclusive) | Ranking position |
| name | str | 2-100 chars, alphanumeric+space | Item name |
| score | float | 0.0-10.0 | Normalized quality score |
| key_attributes | list[str] | 3-5 unique items | Distinctive features |
| description | str | 50-500 chars | Detailed explanation |

## RankingResult Model

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| topic | str | 3-50 chars | Ranking subject |
| generated_at | datetime | UTC timestamp | Generation time |
| rankings | list[RankedItem] | Exactly 10 items | Ordered results |
| sources | list[URL] | ≥1 valid URL | Data sources |
| methodology | str | ≥100 chars | Analysis process |

## Validation Rules
- All ranking positions must be unique
- Key attributes must have distinct values
- Scores are normalized to 0-10 scale 

## Ranking Agent Workflow

1. Receives user query
2. Performs web search using integrated tool
3. Analyzes results with LLM using ranking criteria
4. Validates output against Pydantic models
5. Returns structured RankingResult 

## Search Integration

Uses DuckDuckGo's official API with:
- Real-time web results
- Domain extraction
- Category tagging
- Strict content filtering

API Documentation: https://duckduckgo.com/api 