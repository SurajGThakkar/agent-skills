# Contributing to Agent Skills

First off, thank you for considering contributing to Agent Skills! It's people like you that make open source such a great community.

## Philosophy

We strive to build **Bespoke and Holistic** skills. Before submitting a skill, ask yourself:
- Does this solve a real-world problem elegantly?
- Is the prompt engineering concise, robust, and free of vague instructions?
- Have I provided a `README.md` that explains the human-facing side of the skill?

## How to Contribute

1. **Fork the repository.**
2. **Create a new branch** for your skill (`git checkout -b feature/my-new-skill`).
3. **Add your skill** to the appropriate category folder under `skills/` (e.g., `skills/engineering/my-new-skill`).
4. **Include a `SKILL.md`** file detailing the instructions.
5. **Include a `README.md`** inside your skill's folder explaining how to use it.
6. **Commit your changes** with clear commit messages.
7. **Push to the branch** and open a Pull Request.

## Formatting Guidelines

- All documentation should be written in clean, standard Markdown.
- Keep your `SKILL.md` files focused. Avoid sprawling over 500 lines unless absolutely necessary; use the `references/` pattern to load extra context on demand.
- Add your skill to the global `skills.sh.json` file in the appropriate grouping before submitting.

We review PRs actively and look forward to your contributions!
