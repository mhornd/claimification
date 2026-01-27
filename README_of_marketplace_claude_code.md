# TwoDigits Marketplace

> **A curated registry of high-quality Claude Code plugins for enterprise development workflows**

The TwoDigits Marketplace is a quality-focused plugin registry that connects you with professional Claude Code plugins for legacy migration, development automation, and enterprise workflows.

## What is This?

Unlike traditional plugin marketplaces that host code, TwoDigits Marketplace is a **curated registry** that:

- **Links to** external plugins (we don't host the code)
- **Curates** quality plugins that meet professional standards
- **Maintains** metadata and compatibility information
- **Verifies** security and functionality

**Think of it as:** "Editor's Choice" for Claude Code plugins.

## Why Use TwoDigits Marketplace?

### For Users

✅ **Quality Guaranteed:** All plugins meet rigorous curation criteria
✅ **Enterprise-Ready:** Professional documentation and maintenance standards
✅ **Security Verified:** Security review before inclusion
✅ **Modular Installation:** Install only what you need
✅ **Up-to-Date:** Regular compatibility and maintenance verification

### For Plugin Authors

✅ **You Maintain Ownership:** Your code stays in your repository
✅ **We Handle Discovery:** Users find your plugin through our registry
✅ **Quality Badge:** Inclusion signals quality and trust
✅ **No Hosting Burden:** We link to you, we don't fork you

## Quick Start

### 1. Install the Marketplace

```bash
/plugin marketplace add TwoDigits/twodigits-marketplace
```

### 2. Browse Available Plugins

See [registry/README.md](./registry/README.md) for the full catalog.

### 3. Install Plugins

```bash
# Legacy migration framework
/plugin install human-in-the-core@twodigits-marketplace

# Mainframe analysis toolkit
/plugin install mainframe-discovery-toolkit@twodigits-marketplace

# Task management
/plugin install task-manager@twodigits-marketplace
```

### 4. Update Plugins

```bash
/plugin update human-in-the-core
```

## Featured Plugins

### 🚀 human-in-the-core
**AI-assisted legacy system migration framework**

Complete COBOL→Java migration toolkit with 15 specialized agents, 28 workflow commands, quality gates, and interactive artifact viewer.

**Best for:** Enterprise legacy system migrations
**[View Details](./registry/README.md#human-in-the-core)**

---

### 🔍 mainframe-discovery-toolkit
**Automated mainframe codebase analysis**

Python-powered analysis toolkit for mainframe inventory, dependency graphs, complexity scoring, and migration wave generation.

**Best for:** Mainframe migration planning
**[View Details](./registry/README.md#mainframe-discovery-toolkit)**

---

### ✅ task-manager
**Priority-based development task management**

Directory-based task system with priority queues, archival, and TodoWrite integration.

**Best for:** Organized project workflows
**[View Details](./registry/README.md#task-manager)**

## Architecture

### Registry-First Design

```
twodigits-marketplace/
├── registry/                      # Plugin metadata (JSON)
│   ├── human-in-the-core.json
│   ├── mainframe-toolkit.json
│   └── task-manager.json
├── docs/                          # Documentation
│   ├── REGISTRY-GUIDE.md          # How to add plugins
│   └── CURATION-PROCESS.md        # Quality criteria
└── .claude-plugin/
    └── plugin.json                # Marketplace manifest
```

### How It Works

1. **Plugin authors** create Claude Code plugins in their own repositories
2. **We curate** plugins that meet quality standards
3. **We publish** metadata in `registry/*.json` pointing to original repos
4. **Users install** plugins via our marketplace reference
5. **Claude Code** fetches from the original repository
6. **Original authors** maintain and update their plugins

**Result:** Quality curation without hosting burden.

## For Plugin Authors

### Submit Your Plugin

Want your plugin featured in TwoDigits Marketplace?

1. **Review criteria:** [docs/CURATION-PROCESS.md](./docs/CURATION-PROCESS.md)
2. **Follow submission guide:** [docs/REGISTRY-GUIDE.md](./docs/REGISTRY-GUIDE.md)
3. **Submit PR** with metadata file

### Curation Criteria

Plugins must meet:
- ✅ Professional documentation
- ✅ Active maintenance
- ✅ Security best practices
- ✅ Open-source license
- ✅ Clear value proposition

See [docs/CURATION-PROCESS.md](./docs/CURATION-PROCESS.md) for detailed criteria.

## Philosophy

### Curation Over Aggregation

We believe in **quality over quantity**. Every plugin in this registry:
- Has been manually reviewed
- Meets professional standards
- Solves real problems
- Is actively maintained

### Responsibility Separation

- **Original authors** maintain their code
- **We** curate and verify quality
- **Users** benefit from trusted recommendations

This model scales better than monolithic bundles or unmaintained forks.

### Enterprise-Ready

All plugins meet enterprise standards:
- Professional documentation
- Security review
- Version management
- Support channels

## Contributing

### Add a Plugin

See [docs/REGISTRY-GUIDE.md](./docs/REGISTRY-GUIDE.md)

### Report Issues

- **Registry issues:** Open issue in this repository
- **Plugin issues:** Open issue in the plugin's repository

### Improve Documentation

PRs welcome for:
- Documentation improvements
- Curation process refinements
- Registry tooling

## Repository Structure

```
twodigits-marketplace/
├── .claude-plugin/
│   └── plugin.json              # Marketplace manifest
├── registry/
│   ├── README.md                # Plugin catalog
│   ├── human-in-the-core.json   # Plugin metadata
│   ├── mainframe-toolkit.json
│   └── task-manager.json
├── docs/
│   ├── REGISTRY-GUIDE.md        # Submission guide
│   └── CURATION-PROCESS.md      # Quality criteria
├── design-decisions.md           # Architecture decisions
├── LICENSE
└── README.md                     # This file
```

## Roadmap

### v1.0 (Current)
- ✅ Registry foundation
- ✅ Manual curation process
- ✅ 3 initial plugins (migration + development)

### v1.1 (Planned)
- [ ] Automated JSON schema validation
- [ ] Link verification tests
- [ ] Dependency security scanning

### v2.0 (Future)
- [ ] CLI tooling (`twodigits-cli`)
- [ ] Automated metadata generation
- [ ] Community contribution workflow
- [ ] Plugin statistics & analytics

## FAQ

### How is this different from npm/PyPI?

We're a **curated registry**, not a package manager. We link to quality plugins, we don't host packages.

### Do you fork plugins?

**No.** We only maintain metadata. Original code stays in original repositories.

### What if a plugin breaks?

Contact the original author via their repository. We verify quality at inclusion, but authors maintain their code.

### Can I install plugins outside this registry?

**Yes!** Claude Code supports any plugin. Our registry is for curated, verified plugins.

### How do I update plugins?

```bash
/plugin update <plugin-name>
```

This fetches the latest version from the original repository.

### What licenses are acceptable?

Open-source licenses: MIT, Apache 2.0, GPL, BSD. See [docs/CURATION-PROCESS.md](./docs/CURATION-PROCESS.md#6-licensing-).

## Support

- **Registry questions:** Open an issue in this repository
- **Plugin support:** Contact the plugin's author via their repository
- **Marketplace bugs:** Report in this repository with label `bug`

## License

This registry (metadata and documentation) is licensed under [MIT License](./LICENSE).

Individual plugins retain their own licenses (see plugin repositories).

## Maintained By

**TwoDigits**
- Email: info@twodigits.dev
- GitHub: [@TwoDigits](https://github.com/TwoDigits)

---

**Registry Version:** 1.0.0
**Total Plugins:** 3
**Last Updated:** 2026-01-26
