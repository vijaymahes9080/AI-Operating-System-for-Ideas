# Open Source Governance

IdeasOS is dedicated to remaining a community-driven, open-source project. This document outlines the steering structure, decision-making systems, and licensing models.

---

## 1. Project Steering Committee (PSC)

The development of IdeasOS is guided by a **Project Steering Committee (PSC)** consisting of core maintainers, community representatives, and academic research partners.

### Responsibilities
- Reviewing and approving RFC design drafts.
- Setting roadmap priorities for the core modules.
- Managing marketplace security approvals and package key signings.
- Structuring core API boundaries to prevent vendor lock-in.

---

## 2. The RFC (Request for Comments) Process

All major architectural proposals (e.g., changes to the Graph Schema, adding new agent roles, or refactoring the Plugin SDK) must go through the **RFC process**:

```
[Write Draft Proposal] 
       |
       v
[Open PR in docs/rfcs/] 
       |
       v
[Community Review Period (14 Days)]
       |
       +---> (Rejection) ---> [Close PR / Archive]
       |
       +---> (Approval)  ---> [Merge PR & Assign Task to Roadmap]
```

RFC documents must follow the template located in `docs/rfcs/template.md`, outlining:
- Feature Summary & Motivation.
- Detailed Technical Specification.
- Potential breaking changes or migration paths.
- Security and Privacy audits.

---

## 3. Licensing Policy & IP Protection

To prevent enterprise vendor lock-in while protecting the community from predatory commercialization:

- **Core Engine & Libraries**: Licensed under the **Apache License 2.0** or **MIT License**. This allows developers to construct closed-source proprietary plug-ins if desired.
- **Tauri Native Application UI**: Licensed under the **GNU General Public License v3 (GPL-3.0)** or **AGPL-3.0**. Any modification to the core desktop app container must remain public and open-source.
- **Contributor License Agreement (CLA)**: Contributors retain copyright ownership of their additions while granting the IdeasOS Foundation a non-exclusive, perpetual, worldwide license to distribute their code under the project's target open-source terms.
