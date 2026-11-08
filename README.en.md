# ecommerce-price-hunt · Cross-platform Price Comparison Skill

[中文说明](README.md) · [DSH go (upstream)](https://github.com/ccch1mneyyy/dsh-go/)

> **Project positioning — read this first**
> This is an **open-source project for an ancillary feature built for [DSH go](https://github.com/ccch1mneyyy/dsh-go/)**. It packages the "let an AI automatically compare product / medicine prices across stores" capability as a reusable Skill (prompts + operating playbooks), for DSH go and other AI Agents with screen-reading ability.
> Upstream repository: **<https://github.com/ccch1mneyyy/dsh-go/>**
> This project is **not an official DSH go component**, is not affiliated with the upstream project, and contains or copies **no upstream code**. It is an independently published and independently licensed methodology reference.

---

## ⚠️ Disclaimer (mirrors `SKILL.md`; the Chinese text there is authoritative)

> **Statement of purpose**
> This project is a **comparison work instruction**: prompts and operating playbooks only, with **no automation scripts, no cracking tools and no reverse-engineered API code**. It is designed for an individual using their own device, their own account, and human-paced browsing. **Do not** use it for device farms, fake orders, flash-sale bots, bulk scraping, harvesting personal data, commercial price-comparison services, or price advertising. It does **not** bypass CAPTCHAs, risk controls, app locks or encrypted endpoints — hand control back to the user instead. For learning and personal research only; **not legal advice**. Consult a lawyer before commercial use or wide distribution.

> **Medicine-specific use restriction** (from `SKILL.md`, mandatory when the target is a medicine)
> - Results are **for personal reference only**; **they must not be used for medicine advertising, price promotion, diagnostic or treatment advice, or for publishing public price-comparison rankings**.
> - Purchasing and using medicines must follow a physician's or pharmacist's guidance.
> - Gate: an NMPA approval number (国药准字 + letter + 8 digits), an OTC/RX marking, and a dosage form matching the generic name — all three must be present; unverifiable approval numbers are recorded as "unverified", never invented.

> This project provides a method only. It is not medical, purchasing or investment advice. Prices are time-sensitive; the authors accept no liability for any loss arising from its use. Comply with each platform's terms of service and applicable law.

---

## What it is

A **methodology for AI Agents**: using accessibility-based screen reading on a phone or browser, an Agent visits each platform, records the real out-of-pocket price, shipping origin and delivery estimate, then produces a single-file HTML report self-checked on two viewports (phone + laptop).

It is **not** a crawler library, **not** a price API, **not** an automation script. There is no price-collection code in this repository and there never will be.

## Why a Skill instead of letting the Agent improvise

| Common Agent mistake | Constraint in this Skill | What it saves |
| --- | --- | --- |
| Reports "lowest price" from the first screen | 3–5 screens per platform, multiple shops, keep scrolling in detail pages, check the checkout page for specs | Avoids redoing the whole run after the conclusion breaks |
| Treats list price as final price | Final = list price + shipping − stackable coupons, with coupon conditions recorded | Avoids re-collecting every platform |
| Compares different package sizes directly | Normalise to ¥/g, ¥/ml, ¥/tablet; split multi-packs; never mix specs | Avoids scrapping the whole table |
| Mixes medicines with cosmetics / supplements | Step 0 category gate; medicine gate for 国药准字, exclude 妆/食/健/消/械 by default | Avoids unusable or risky output |
| Dumps every playbook into context | On-demand loading table per scenario | Directly cuts input tokens per turn |
| Redesigns the report every run | Fixed 10 sections + column definitions + dual-screen checklist | Cuts layout iterations and screenshot rounds |
| Guesses a number when the screen can't be read | No guessing; log it under "limitations"; separate inference from observation | Avoids hallucination and trust cost |
| Pushes past app locks / CAPTCHAs | Always hand off to the user; never bypass | Avoids dead ends and policy violations |

In short: **turn known pitfalls into gates, repeated work into templates, and long manuals into on-demand loads.** No quantitative efficiency claims are made.

## Quick start

1. Download `ecommerce-price-hunt-vX.Y.Z.zip` from the [latest Release](https://github.com/neurotracee/ecommerce-price-hunt/releases) and unzip it.
2. Put the whole directory into your Agent's skills folder.
3. Say: *"Run a cross-platform price comparison for ⟨brand + product + spec⟩, give me an HTML report, my delivery address is in ⟨city⟩."*

## Install

```bash
mkdir -p ~/.dsh/skills
cp -r ecommerce-price-hunt ~/.dsh/skills/
```

For other hosts (Claude Code, WorkBuddy, custom harnesses), follow their own skill / prompt directory convention; without a skill mechanism, use `SKILL.md` as a system prompt and inject `references/*.md` per the on-demand table. See [docs/portability.md](docs/portability.md).

## Layout

```
SKILL.md                     entry point: category gate, collection flow, pricing rules, medicine gate, hard rules
references/*.md              on-demand playbooks (platforms, screen reading, pricing math, report spec)
assets/report-skeleton.html  section skeleton only; all sample numbers are fictional
docs/ examples/ scripts/     design notes, usage examples, validation / packaging / publishing
.github/                     issue & PR templates, CI validation
```

## Prohibited uses

Device farms, account farming, fake orders/reviews, flash-sale bots, bulk scraping, harvesting personal data, bypassing CAPTCHA / risk control / app locks / biometric checks / undocumented endpoints, public price rankings, medicine advertising, price promotion, investment or treatment advice, high-frequency polling, unattended loops, concurrent multi-account operation.

Recommended ceiling: ≤30 links and ≤3 deeply-examined platforms per task. Record only comparison-required fields; never persist personal information.

## Releases

Each release ships a ready-to-install zip and repeats the full disclaimer plus the DSH go attribution in its notes. Mirrored on Gitee. See [CHANGELOG.md](CHANGELOG.md).

## License

- Code and templates (`assets/`, `scripts/`): [MIT](LICENSE).
- Documentation and prompts (`README*`, `SKILL.md`, `references/`, `docs/`, `examples/`): [CC BY-NC-SA 4.0](LICENSE-DOCS.md). Commercial use (including commercial price-comparison services) requires separate written permission.
- Because the docs use an NC clause, this project is strictly **source-available / free for non-commercial use**, not OSI-certified open source — a deliberate choice consistent with its use boundary.

Upstream [DSH go](https://github.com/ccch1mneyyy/dsh-go/) is AGPL-3.0. This project contains none of its code, is an independent work under its own license, and does not speak for the upstream project.

---

For personal learning and research only. Full disclaimer at the top of this file and in `SKILL.md`.
