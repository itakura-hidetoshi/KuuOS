# KuuOS Browser MCP Compatibility v7.21

## Purpose

KuuOS now has verified repository, semantic, and documentation MCP planes.

v7.21 verifies the browser plane through two distinct MCP presentations:

```text
Playwright MCP
-> deterministic functional browser verification

Chrome DevTools MCP
-> browser diagnostics, console, network and performance inspection
```

They are deliberately not collapsed into one provider.

## Exact targets

### Playwright MCP

```text
microsoft/playwright-mcp
main SHA: e87bb897e15a6f2af402afb0f10b45eced9e1f9b
@playwright/mcp: 0.0.82
```

### Chrome DevTools MCP

```text
ChromeDevTools/chrome-devtools-mcp
main SHA: ae0aaef884c41445d83f86f099ef211f4584b791
chrome-devtools-mcp: 1.10.1
```

## Shared deterministic fixture

The CI probe starts one ephemeral HTTP server bound only to:

```text
127.0.0.1
```

The page contains:

- a stable accessibility marker;
- a stable console marker;
- a simple button.

No external website is used for compatibility evidence.

## Playwright observation

The Playwright server is started:

```text
--browser chrome
--headless
--isolated
--no-webmcp
--block-service-workers
```

The browser is allowed to request only the local fixture origin during the probe.

The required calls are:

```text
browser_navigate
browser_snapshot
```

The accessibility snapshot must contain the fixture marker.

## Chrome DevTools observation

Chrome DevTools MCP is started:

```text
--headless=true
--isolated=true
--usage-statistics=false
--performance-crux=false
```

The probe calls:

```text
new_page
list_pages
take_snapshot
list_console_messages
```

The accessibility snapshot must contain the same fixture marker.

The console plane must independently contain:

```text
KUUOS_BROWSER_FIXTURE_READY
```

## Different presentations, shared conditioned world

The two servers observe the same local browser fixture, but their meanings differ.

Playwright's primary question is:

> does the browser flow function deterministically?

Chrome DevTools' primary question is:

> what happened inside the browser runtime?

Therefore:

```text
same fixture
!=
same browser presentation
```

and:

```text
Playwright success
!=
Chrome DevTools diagnostic success
```

Both can be available simultaneously.

## Effect boundary

Browser navigation is a real effect, but this compatibility probe is tightly bounded:

- localhost only;
- temporary isolated profiles;
- no persistent session;
- no user data;
- no external target;
- Chrome DevTools usage statistics disabled;
- CrUX lookup disabled.

A successful compatibility receipt does not grant future browser-effect authority.

## Promotion

If final exact-head CI succeeds, both servers may move from:

```text
recommended_sandboxed
->
verified_compatible
```

while retaining separate browser-session effect authority.
