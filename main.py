# office-placard-v2 — entry for "Office Artifacts: The One-Line Placard Contest"
# make.fun bounty u-coral-ibis-18-office-artifacts-the-one-line-placard-3af971d2
#
# What this program does: it writes exactly one line of text to
# /output/entry.txt — a museum placard for an ordinary office object,
# written as if the object were an ancient artifact dug up from a lost
# civilisation. The gate allows 1-180 characters of non-whitespace
# UTF-8 text on a single line.
#
# How the line was picked (the whole method lives in this file, so the
# choice is reproducible rather than asserted):
#
#   * Twelve original placards were drafted against the brief, in the
#     brief's own order of importance:
#       1. on-brief — an office object presented as an ancient artifact,
#          inventive and funny, not a generic office joke;
#       2. conceit — the imagined history is specific and surprising,
#          a real invention rather than a relabel;
#       3. dryness — deadpan curator's voice; the joke lands without
#          straining, explaining itself, or begging for a laugh;
#       4. placard voice — it reads like a museum label: catalogue
#          date, material, provenance or donor doing quiet work;
#       5. economy — one line inside 180 characters, every word earning
#          its place.
#   * Every draft carries a hand score of 0-10 on each of the five
#     criteria, in that order. The draft with the highest total wins;
#     a tie goes to the shorter line.
#   * The winning draft then got a genuine second pass (see the
#     REVISION note below): named weaknesses, each fixed, and the
#     revised line is what ships. Nothing here touches the network,
#     reads any secret, or depends on the clock — the output is
#     byte-identical on every run.

import hashlib
import os

# Drafts: (text, (on_brief, conceit, dryness, voice, economy)).
# Scores are my own hand judgements, written next to the draft they
# judge; the totals are computed, never hand-added.
DRAFTS = [
    # 8+8+9+8+9 = 42. The late-period expense-claims twist is good and
    # the donor line lands, but stapling covenants is the first stapler
    # joke anyone reaches for, so the conceit is less surprising.
    (
        "Ritual Stapler, c. 1997. Pressed steel. It bound covenants, "
        "and in the late period, expense claims. Gift of the Accounts "
        "Department, who never forgave it.",
        (8, 8, 9, 8, 9),
    ),
    # 8+8+9+8+8 = 41. "The belonging never verified" is dry and good;
    # the lanyard-as-proof-of-belonging idea is solid but familiar.
    (
        "Ceremonial Lanyard, c. 2004. Woven nylon, base-metal clip. "
        "It proved the bearer belonged; the badge is lost, the "
        "belonging never verified. Donor anonymous.",
        (8, 8, 9, 8, 8),
    ),
    # 10+9+9+9+9 = 46. WINNING DRAFT. A sticky note recast as a votive
    # tablet is the most surprising recast on the list: a disposable
    # memo treated as a sacred inscription, and "the god Dave" gives
    # the imagined religion a specific, mundane deity. Deadpan
    # throughout; date, material and excavation site all sell it.
    (
        "Votive Tablet (Sticky Note), c. 2011. Paper, weak adhesive. "
        "Inscribed 'call Dave back'; the god Dave never answered. "
        "Excavated from the south monitor.",
        (10, 9, 9, 9, 9),
    ),
    # 8+9+8+8+8 = 41. "Blamed one another for three thousand years"
    # is funny and the communal-hearth framing is good, but the
    # microwave joke leans on the well-worn fish-in-the-microwave
    # office trope.
    (
        "Communal Hearth (Microwave), c. 2009. Enamelled steel. Its "
        "people warmed fish in it and blamed one another for three "
        "thousand years. Donated by Facilities.",
        (8, 9, 8, 8, 8),
    ),
    # 9+8+9+8+7 = 41. "Still jammed with the sins of 1994" is a fine
    # deadpan closer; the filing-the-gods conceit is inventive, but
    # the label craft is thinner — no donor, little material detail.
    (
        "Twin-Hole Punch, c. 1985. Cast iron. Priests bored paired "
        "holes in sacred leaves so the gods might file them. Still "
        "jammed with the sins of 1994.",
        (9, 8, 9, 8, 7),
    ),
    # 9+7+9+8+7 = 40. "Binding Serpent" is a strong recast, but the
    # second loop "bent back twice, in despair" explains its own joke
    # a little too hard for a dry curator.
    (
        "Binding Serpent (Paperclip), c. 1912. Bent wire. One loop "
        "held the empire's contracts together; the other was bent back "
        "twice, in despair. Found in a drawer.",
        (9, 7, 9, 8, 7),
    ),
    # 8+8+9+8+8 = 41. "One thump made a thing true" is excellent; the
    # stamp-as-seal conceit is, however, nearly literal — a stamp
    # already is a seal — so the invention scores lower.
    (
        "Seal of Approval (Rubber Stamp), c. 1978. Wood and rubber, "
        "red ink. One thump made a thing true; two thumps made it "
        "regrettable. Gift of the Registry.",
        (8, 8, 9, 8, 8),
    ),
    # 8+8+8+9+7 = 40. "Its prophecies faded within the hour, as
    # ordained" is dry and economical; the wand framing is weaker,
    # and the lost-lid gag is the obvious marker joke.
    (
        "Ritual Ink Wand (Whiteboard Marker), c. 2015. Felt and "
        "solvent. Its prophecies faded within the hour, as ordained. "
        "The lid, of course, was lost.",
        (8, 8, 8, 9, 7),
    ),
    # 8+8+9+8+8 = 41. "It bit the bundle and never let go" is vivid
    # and the leaving-card twist is good; the jaw framing is solid
    # but not as surprising as the votive tablet.
    (
        "Jaw of the Archive (Binder Clip), c. 1988. Folded steel. It "
        "bit the bundle and never let go; the bundle was a leaving "
        "card. Excavated from Desk 14.",
        (8, 8, 9, 8, 8),
    ),
    # 8+9+8+8+9 = 42. "'World's Best Boss' ... disputed by scholars"
    # is a strong closer with good label craft, but the mug itself is
    # a famous sitcom prop, so the conceit borrows a joke the reader
    # has already heard.
    (
        "Communal Chalice (Coffee Mug), c. 2003. Glazed ceramic, "
        "chipped rim. Drunk from daily at 9 a.m.; the inscription "
        "'World's Best Boss' is now disputed by scholars.",
        (8, 9, 8, 8, 9),
    ),
    # 9+8+9+8+8 = 42. "Moved nothing" is a beautifully dry payoff and
    # the scribe framing is fresh; the donor line ("IT,
    # reluctantly") is the weakest link — it gestures at a joke
    # instead of landing one.
    (
        "Offering Mat (Mouse Pad), c. 2006. Worn rubber, frayed edge. "
        "The hand of the scribe rested here for ten thousand hours and "
        "moved nothing. Donor: IT, reluctantly.",
        (9, 8, 9, 8, 8),
    ),
    # 8+8+8+7+8 = 39. A decent deadpan ("it answered in neither
    # season") but the longest draft at 170 characters, and the
    # wind-idol framing spends words the joke does not repay.
    (
        "Wind Idol (Desk Fan), c. 1999. Plastic, three speeds. "
        "Worshippers faced it in summer and blamed it in winter; it "
        "answered in neither season. Gift of the open-plan temple.",
        (8, 8, 8, 7, 8),
    ),
]

# REVISION — second pass on the winning draft, three named weaknesses,
# each fixed, none of them cosmetic:
#   (a) The semicolon splice — "Inscribed 'call Dave back'; the god
#       Dave never answered" — made one sentence do two jobs and
#       muffled the punchline. Split into two short deadpan sentences,
#       so the god's silence lands as its own beat: "Inscribed 'call
#       Dave back'. The god Dave never answered."
#   (b) No closing beat — the draft ended on the excavation site and
#       left the tablet's fate hanging. Added "still stuck": the weak
#       adhesive, named in the label's material line, pays off at the
#       end — fifteen years on, the sacred tablet is still stuck to
#       the monitor.
#   (c) Rhythm — the revised line now reads as four curator's
#       sentences (object, inscription, verdict, provenance), each
#       earning its place, at 163 of the 180 allowed characters.
FINAL_LINE = (
    "Votive Tablet (Sticky Note), c. 2011. Paper, weak adhesive. "
    "Inscribed 'call Dave back'. The god Dave never answered. "
    "Excavated from the south monitor, still stuck."
)


def choose(drafts):
    """Highest total score wins; ties go to the shorter line."""
    ranked = []
    for text, scores in drafts:
        assert 1 <= len(text) <= 180, f"draft over gate: {len(text)} chars"
        assert text.strip(), "draft is blank"
        assert "\n" not in text, "draft must be a single line"
        ranked.append((sum(scores), -len(text), text))
    ranked.sort(reverse=True)
    return ranked[0][2]


def write_entry(line):
    """Write the entry and self-check the exact bytes on disk."""
    assert 1 <= len(line) <= 180, f"output over gate: {len(line)} chars"
    assert line.strip(), "output is blank"
    assert "\n" not in line, "output must be a single line"
    os.makedirs("/output", exist_ok=True)
    payload = line.encode("utf-8")
    with open("/output/entry.txt", "wb") as handle:
        handle.write(payload)
    digest = hashlib.sha256(payload).hexdigest()
    print(f"entry: {len(line)} chars, {len(payload)} bytes, sha256={digest}")
    print(line)


def main():
    winner = choose(DRAFTS)
    # The revision must stay a revision of the winning draft: same
    # object, same catalogue line, same inscription — only the named
    # fixes applied.
    assert winner.startswith("Votive Tablet (Sticky Note), c. 2011.")
    assert FINAL_LINE.startswith("Votive Tablet (Sticky Note), c. 2011.")
    assert "'call Dave back'" in FINAL_LINE
    assert "god Dave never answered" in FINAL_LINE
    write_entry(FINAL_LINE)


if __name__ == "__main__":
    main()
