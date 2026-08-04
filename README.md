# catalogue

Jeremy Curmi's shareable Claude Code setup, packaged as a plugin marketplace.

## Install

```
/plugin marketplace add JeremyCurmi/catalogue
/plugin install dev@catalogue
/plugin install productivity@catalogue
```

## Layout

```
.claude-plugin/marketplace.json
plugins/
  dev/                          engineering
    .claude-plugin/plugin.json
    skills/
  productivity/                 day-to-day
    .claude-plugin/plugin.json
    skills/tldr/
```

## Skills

| Plugin | Skill | Does |
|---|---|---|
| productivity | [`tldr`](plugins/productivity/skills/tldr) | Compresses an article, X thread or long doc into a terse visual card that reads in under two minutes |

`dev` is still an empty scaffold.
