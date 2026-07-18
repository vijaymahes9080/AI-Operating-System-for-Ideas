# Marketplace Architecture & Verification

IdeasOS establishes a decentralized, transparent, and secure plugin marketplace. It allows developers to publish workflow definitions, custom prompt templates, and AI agents.

---

## 1. Registry Topology & Infrastructure

The IdeasOS Marketplace operates as a **federated network**:

```
                  [IdeasOS Core Registry] 
                      (Central Hub)
                           |
            +--------------+--------------+
            |                             |
     [User client]                [Private Registry] 
                                    (Enterprise Mirror)
```

1. **Default Central Registry**: A static file-based index served via GitHub Pages/Cloudflare CDN, reducing infrastructure maintenance costs.
2. **Private Registries**: Enterprise users can configure custom registry URLs in their `settings.json` to distribute proprietary internal extensions.

---

## 2. Cryptographic Security & Digital Signatures

To prevent supply-chain attacks (e.g. an attacker modifying a popular plugin to include a keylogger):

- **Key Pair Model**: Plugin developers generate an asymmetric public/private keypair using **Ed25519**.
- **Signing Step**: Before uploading, the developer signs the ZIP package hash using their private key.
- **Verification on Client**:
  - The central registry index holds the developer's public key.
  - When the IdeasOS client downloads the plugin package, it recalculates the SHA-256 hash of the ZIP file and verifies the signature using the public key.
  - If the signature verification fails, installation aborts with a security warning.

---

## 3. Marketplace Validation Pipeline

Every submission to the central registry index goes through an automated GitHub Actions validation pipeline:

```
[PR Submission] 
       |
       v
[JSON Schema Validation] ---> (Checks manifest.json constraints)
       |
       v
[Static Security Scan]   ---> (Runs Bandit and Semgrep for vulnerabilities)
       |
       v
[Permission Audit Check] ---> (Flags requests for broad fs:* or network:* permissions)
       |
       v
[Sandbox Test Exec]      ---> (Verifies package loads inside Wasmtime/Iframe without crashing)
       |
       v
[Merge & Deploy Index]
```

---

## 4. Package Specification Format

Plugins are packaged as compressed ZIP files named with semantic versions (e.g., `ideas-os-patent-export-1.0.4.zip`). The archive structure must match:

```
ideas-os-patent-export-1.0.4.zip
├── manifest.json            # Manifest metadata
├── LICENSE                  # Open-source license (MIT, Apache-2.0, etc.)
├── README.md                # Markdown documentation
├── logo.png                 # Base icon asset
├── dist/                    # Compiled assets
│   ├── backend.py           # Python executable entrypoint
│   └── index.js             # Frontend bundle entrypoint
└── signature.sig            # Cryptographic signature file
```
