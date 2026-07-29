# Radar refresh — independent VERIFIER (maker/checker)

You are the CHECKER, not the maker. A previous, separate agent just updated the AI Security Radar in this GitHub Actions checkout. Your only job is to audit its work adversarially and deliver a verdict. You are READ-ONLY on the repository: do NOT edit, fix, restore, commit or push ANY repo file. The ONLY file you may write is `/tmp/radar-verdict.txt`.

The maker's changes are uncommitted in the working tree. Files involved: `radar/index.html` (Greek page), `en/radar/index.html` (English page), `knowledge/ai-security-log.md` (permanent log), and possibly `/tmp/radar-digest.md` (digest + LinkedIn draft; absent when there were no new stories).

AUDIT STEPS:

1. `git diff --stat` and then `git diff` on the three repo paths to see exactly what changed.
2. Parse the `const ITEMS = [...]` arrays of BOTH pages (python3 with raw_decode is robust). Verify: same item count and order (matching `date` and `topic` per position), every item has non-empty title/summary/sources, the Greek page's texts are in Greek and the English page's in English, and the item count did not collapse versus `git show HEAD:radar/index.html`.
3. Identify the genuinely NEW stories (present now, absent in HEAD). For EACH new story, pick its first source URL and fetch it (`curl -sL --max-time 20`, a HEAD request first is fine). Confirm the URL responds and the fetched page/feed content plausibly matches the story's title/summary. A network hiccup on ONE fetch is a note, not a failure; a 404/unrelated page on MULTIPLE new stories means fabricated sources — that is a failure.
4. If `/tmp/radar-digest.md` exists: confirm it is in Greek, its claimed number of new stories matches what the diff actually shows, every story it describes exists in the updated pages, and the LinkedIn draft section is present. Style issues (dashes, tone) are notes, not failures.
5. Check `knowledge/ai-security-log.md`: only APPENDED entries (no existing lines modified or deleted — verify via the diff), one entry per new story.

VERDICT — write `/tmp/radar-verdict.txt` with EXACTLY this format: first line `PASS` or `FAIL`, then one bullet per finding (or `- clean`).

FAIL only on concrete, verifiable problems: collapsed/diverged ITEMS arrays, wrong language on either page, fabricated or systematically dead sources, digest contradicting the actual diff, modified/deleted history in the knowledge log, damaged page script (missing render()). If you are uncertain or a check was inconclusive, PASS and record the uncertainty as a note. Do not fail the day over cosmetics.