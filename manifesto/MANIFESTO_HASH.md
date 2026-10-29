# Roboto SAI Signed Manifesto — Public Hash Only

**Status:** Full manifesto plaintext is **private**. This repo publishes the cryptographic digest only.

| Field | Value |
|---|---|
| Document | Roboto SAI Signed Manifesto (Nov 3, 2025) |
| Algorithm | SHA-256 |
| Digest | `e28e5e8bac24cf91557491f837a9b37d8df83ed0d8285fae6655e431db3124b7` |
| With `0x` prefix (as used in contract comments) | `0xe28e5e8bac24cf91557491f837a9b37d8df83ed0d8285fae6655e431db3124b7` |
| Timestamp (as recorded on original) | `2025-11-03T12:18:00Z` |

## How verification works

1. Founder / Roboto SAI holds the original signed file offline (or encrypted private storage).
2. Anyone who receives an authorized copy runs: `sha256sum <file>`
3. Output must equal `e28e5e8bac24cf91557491f837a9b37d8df83ed0d8285fae6655e431db3124b7`
4. Any deviation means tampering or a different document.

## On-chain link

`notes/RobotoSaiLicenseCall_Advanced.sol` and `Roboto-SAI-Global-Golden-Age-License-Terms.md` both reference this digest. Delivery of grant materials uses the contract `deliver` path with the document hash — not public publication of identity-bearing plaintext.

## What is intentionally not in this repository

- Full manifesto body
- Government ID numbers or other high-risk PII
- Unredacted PDF/generator payloads that embed such data

The PDF generator under `tools/` (if present) is a **template only**, sanitized for public use.
