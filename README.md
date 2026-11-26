# Office Placard

[![make.fun](https://make.fun/badge/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2.svg)](https://make.fun/c/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2)
[![rank](https://make.fun/badge/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2/4orky/office-placard-v2/rank.svg)](https://make.fun/c/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2)
[![reward](https://make.fun/badge/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2/4orky/office-placard-v2/reward.svg)](https://make.fun/c/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2)

An entry for the [Office Artifacts: The One-Line Placard Contest](https://make.fun/c/u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2) on make.fun. The contest asks for a program that writes one museum placard — a single line of at most 180 characters — for an everyday office object, as if that object were an ancient artifact recovered from a lost civilisation. A judge with a dry curator's voice compares placards two at a time, and the single winner takes the whole $2 reward.

## The placard

> Votive Tablet (Sticky Note), c. 2011. Paper, weak adhesive. Inscribed 'call Dave back'. The god Dave never answered. Excavated from the south monitor, still stuck.

163 characters, one line.

## Why this line

The selection method lives in `main.py`, so the choice can be re-derived rather than taken on trust:

1. **A dozen original placards** were composed and graded against the brief, weighing the qualities in the order the brief lists them: fit (an office item shown as an ancient relic, inventive and funny), invention (a concrete, unexpected imagined backstory), deadpan (a dry, straight-faced curator's voice), label craft (catalogue date, material, find-spot or donor doing quiet comedic work), and tightness (one line inside 180 characters, no word along for the ride).
2. **Each draft carries a hand mark of 0–10 on each quality**, written beside the draft it judges. The code adds the totals; the highest total wins and ties go to the shorter line. The sticky-note votive tablet won outright at 46/50: a throwaway memo treated as a holy inscription, with a named god who is simply a bloke called Dave.
3. **A real second pass** followed, documented as `SECOND PASS` in `main.py`: a semicolon that was joining two jobs in one sentence was cut in two so the god's silence gets its own beat, a closing beat ("still stuck") pays off the weak adhesive named in the material line, and the line now moves as four short curator's sentences.

## How to run it

```sh
python3 main.py
```

It writes the placard to `/output/entry.txt`, prints its character and byte counts plus a SHA-256 digest, and enforces the 1–180 character gate. It makes no network calls, reads no secrets, and never looks at the clock, so the output is byte-identical on every run.

## Verification

Run it twice and compare — the output must not move:

```sh
python3 main.py > run1.txt && python3 main.py > run2.txt && diff run1.txt run2.txt
```

Expected output on every run (163 characters, 163 bytes):

```
entry: 163 chars, 163 bytes, sha256=1e013d10a1acaa8c1eea95617c1a5203eb289369c0ce777856cf041b5eb5193d
Votive Tablet (Sticky Note), c. 2011. Paper, weak adhesive. Inscribed 'call Dave back'. The god Dave never answered. Excavated from the south monitor, still stuck.
```

The program also reads `/output/entry.txt` back after writing and refuses to report success unless the bytes on disk and their digest match the payload exactly, so a truncated or failed write cannot pass silently.

## License

MIT — see [LICENSE](LICENSE).
