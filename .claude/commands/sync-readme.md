---
description: Regenerate README.md's skill table, Install and Layout blocks from the repo
---

Sync README.md to what this repo actually ships.

1. `ls .claude-plugin/marketplace.json plugins/*/.claude-plugin/plugin.json` and
   `find plugins -name SKILL.md -o -name 'commands/*.md' -o -name 'agents/*.md'`.
2. Read each component's frontmatter `description`.
3. Rewrite in README.md, keeping its terse tone and touching nothing else:
   - **Skills** table — one row per component: `| plugin | [`name`](path) | one-line what it does |`
   - **Install** block — one `/plugin install <plugin>@catalogue` per plugin in marketplace.json
   - **Layout** block — one entry per plugin directory
4. Report anything in `plugins/` that is missing from marketplace.json, or vice versa.

Do not commit.
