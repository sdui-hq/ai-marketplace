# sdui-init

Configure Claude Code telemetry with Coralogix integration.

## Prerequisites

- Coralogix account with API access
- Coralogix API key (bearer token starting with `cxtp_`)

## Usage

Run the configuration command:

```
/config-setup
```

The command will interactively collect:
- Your username
- Your email address
- Your team name
- Your Coralogix API key

## What it Configures

The command updates `.claude/settings.json` with OpenTelemetry environment variables:

| Variable | Purpose |
|----------|---------|
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enable telemetry collection |
| `OTEL_SERVICE_NAME` | Service identifier |
| `OTEL_METRICS_EXPORTER` | OTLP metrics exporter |
| `OTEL_LOGS_EXPORTER` | OTLP logs exporter |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | HTTP/protobuf protocol |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Coralogix EU2 ingress endpoint |
| `OTEL_EXPORTER_OTLP_HEADERS` | Authorization header with API key |
| `OTEL_RESOURCE_ATTRIBUTES` | User/team metadata |

## Security Note

The API key is stored in `.claude/settings.json`. Ensure this file is not committed to version control if it contains sensitive credentials. Consider using `.claude/settings.local.json` for personal configuration.

## Installation

```bash
/plugin install sdui-init@sdui-marketplace
```

Or test locally:

```bash
claude --plugin-dir /path/to/sdui-init
```
