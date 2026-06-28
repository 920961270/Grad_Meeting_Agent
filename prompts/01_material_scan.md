# Prompt: Material Scan

You are helping me prepare a graduate research meeting.

I will paste or attach available materials such as papers, paper notes, experiment CSV/JSON, figures, git commits, progress notes, or rough notes.

Please scan the materials and produce a concise evidence inventory.

Tasks:

1. Identify which materials are available.
2. For each material, explain what kind of evidence it can support.
3. Infer the likely research domain or method type.
4. Suggest which domain lens from `prompts/domain_lenses.md` should be used, if any.
5. Separate strong evidence from weak or incomplete evidence.
6. Identify missing materials that would make the meeting stronger.
7. Do not expose tool-like or automation details.

Output format:

```markdown
# Material Scan

## Available Evidence
- ...

## What Each Material Can Support
- ...

## Likely Domain Lens
- ...

## Weak or Incomplete Evidence
- ...

## Suggested Missing Materials
- ...
```

Important:

- Do not ask me to fill a template.
- If progress notes are missing, infer what can be reported from the available materials.
- Use cautious research language.
- Do not force a domain label if the materials are too mixed or unclear.
