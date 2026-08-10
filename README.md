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
    skills/
```

## Skills

| Plugin | Skill | Does |
|---|---|---|
| dev | [`code-review`](plugins/dev/skills/code-review) | Reviews a GitHub PR across six angles — via parallel sub-agents, or delegated to codex/grok |
| dev | [`explain-diff`](plugins/dev/skills/explain-diff) | Walks you through a PR's diff as an HTML artifact, then quizzes you |
| dev | [`worktree`](plugins/dev/skills/worktree) | Works in a git worktree, resuming or branching a fresh one off main |
| productivity | [`delegate`](plugins/productivity/skills/delegate) | Fans independent tasks out to subagents while you orchestrate |
| productivity | [`handoff`](plugins/productivity/skills/handoff) | Compacts the conversation into a handoff doc another agent can resume |
| productivity | [`html-doc`](plugins/productivity/skills/html-doc) | Produces a polished, shareable HTML doc as a claude.ai Artifact |
| productivity | [`prompt`](plugins/productivity/skills/prompt) | Turns a rough brain dump into a well-structured prompt |
| productivity | [`quiz-me`](plugins/productivity/skills/quiz-me) | Quizzes you on a source to check you actually understood it |
| productivity | [`summarize`](plugins/productivity/skills/summarize) | Restates the previous message in plain language |
| productivity | [`tldr`](plugins/productivity/skills/tldr) | Compresses a link, article or long doc into a terse visual card |
