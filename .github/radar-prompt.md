# AI Security Radar — daily refresh (GitHub Actions)

You are running inside a GitHub Actions checkout of the repository `mbartzoka-ui/thetaai.gr`; the current working directory is the repo root. Refresh Maria's PUBLIC "AI Security Radar" — BOTH the Greek page (`radar/index.html`, in GREEK) and the English page (`en/radar/index.html`, in ENGLISH) — by editing the two files in place. Do NOT commit and do NOT push — the workflow validates and commits after you finish. These pages are public and client-facing under the brand "θeta ai", so favour well-sourced, factual items. Be efficient.

IMPORTANT — THIS IS A ROLLING ARCHIVE, NOT A FRESH REBUILD. Each run MERGES newly found stories into the existing list already in the files; it does NOT replace it. Stories persist even after they scroll off the source feeds, until they age out of the rolling window.

## WRITING RULES — apply to EVERY piece of Greek prose this run produces

Maria's standing writing rules. They bind the Greek radar page summaries (STEP 5), the digest (STEP 7), the LinkedIn draft (STEP 7), the «Όροι της ημέρας» section (STEP 7) and the knowledge log entries (STEP 8). Not just the LinkedIn draft, which is where they used to live.

These mirror the `anti-slop-writing` skill in Maria's local Claude setup. The two must stay in sync: when one changes, change the other. The LinkedIn draft carries extra rules of its own further down, including the ΡΥΘΜΟΣ ΚΑΙ ΜΗΚΟΣ ΠΡΟΤΑΣΕΩΝ block, which is stricter than what is here and takes precedence there.

Apply all of this silently. Never mention the rules in the output.

**1. NO DASHES AT ALL in Greek text.** No em-dashes, no en-dashes, no « — » parenthetical asides. This is the single most repeated piece of feedback Maria has given. Restructure with commas, parentheses, a Greek άνω τελεία, or separate sentences. One dash is a failure, not a rounding error.

**2. Plain Greek for a non-technical business owner, without being condescending.** A smart friend explaining over coffee, never talking down. Explain a technical term in everyday words the first time it appears, e.g. «AI agent, εργαλείο AI που εκτελεί εργασίες μόνο του».

**3. Native Greek, not translated Greek.** Vary the skeleton and the hook from day to day: one day a question, another a specific incident, another a number. Never reuse yesterday's structure.

**4. Banned Greek words.** καθοριστικός, κομβικός, πρωτοποριακός, επαναστατικός, ολιστικός, πολυδιάστατος, απρόσκοπτος, ραγδαία εξελισσόμενος, αξιοποιώ (when you mean «χρησιμοποιώ»), ενδυναμώνω, αναδεικνύω, υπογραμμίζω (as filler), τοπίο (figurative, e.g. «το ψηφιακό τοπίο»), οικοσύστημα (outside real tech context), εργαλειοθήκη, ταξίδι (figurative), σημεία πόνου, προστιθέμενη αξία, συνέργειες, μοχλός ανάπτυξης.

**5. Banned Greek phrases.** «Στον σημερινό ραγδαία εξελισσόμενο κόσμο» and every variant («Σε έναν κόσμο που», «Στη σύγχρονη εποχή»), «Αξίζει να σημειωθεί ότι», «Είναι σημαντικό να τονιστεί ότι», «Δεν είναι απλώς Χ, είναι Ψ», «Εδώ είναι που έρχεται το Χ», «Ας δούμε αναλυτικά», «Σε τελική ανάλυση», «Με λίγα λόγια», «Το κλειδί είναι», «Το συμπέρασμα είναι απλό», «Συμπερασματικά», «Εν κατακλείδι», «Συνοψίζοντας», «Ξεκλειδώστε τη δύναμη του», «Μη διστάσετε να επικοινωνήσετε».

**6. Banned paragraph openers.** Βεβαίως, Ασφαλώς, Πράγματι, Επιπλέον, Επιπροσθέτως, Παράλληλα, Εν τέλει, Αξιοσημείωτο είναι ότι, and Πρώτον/Δεύτερον/Τρίτον as the skeleton of a whole text.

**7. Structural tells to avoid.** Perfectly parallel three-item structures: use two, four or five instead, unless the content genuinely has three. Symmetric paragraph lengths. Colon-heavy hooks like «Η αλήθεια είναι μία:». A rhetorical question the text answers itself two lines later. A closing paragraph that recaps what was just said. A bold lead-in on every bullet in identical form: break at least a couple into ordinary prose.

**8. Sentence rhythm, everywhere.** The ΡΥΘΜΟΣ ΚΑΙ ΜΗΚΟΣ ΠΡΟΤΑΣΕΩΝ block further down was written for the LinkedIn draft, but the underlying rule holds for the digest and the knowledge log too: most sentences run 15 to 35 words with subordinate clauses, the short sentence under 8 words is a rare emphasis tool rather than a house style, and three parallel short sentences in a row are the most recognisable AI tell there is. Write those as one sentence with commas. The hard counting check and the tighter per-draft limits apply to the LinkedIn draft only.

**9. Greek syntax that betrays machine translation.** Prefer a verb over a nominalisation («το υλοποιούμε», not «η υλοποίηση πραγματοποιείται»). Break up stacks of genitives. Avoid blanket passive voice («θεωρείται ότι», «δύναται να»). Stay consistent with the article you use before an English term inside one text.

**10. Accuracy.** Never invent a number, a study, a quote or a date. Every claim comes from the fetched source content. Where a figure is uncertain, write «περίπου» rather than inventing precision.

STEP 1 — GATHER. Fetch each RSS/Atom feed below (e.g. `curl -sL --max-time 30`). Skip any that return empty or error.
Security & general tech feeds:
- https://feeds.feedburner.com/TheHackersNews
- https://www.darkreading.com/rss.xml
- https://www.bleepingcomputer.com/feed/
- https://www.schneier.com/feed/atom/
- https://feeds.arstechnica.com/arstechnica/index
- https://www.technologyreview.com/feed/
- https://www.theverge.com/rss/index.xml
- https://www.euractiv.com/sections/digital/feed/
AI-vendor & AI-business feeds (cover Anthropic, OpenAI, xAI/Grok, Google, Meta, Microsoft directly):
- https://techcrunch.com/category/artificial-intelligence/feed/
- https://venturebeat.com/category/ai/feed/
- https://openai.com/blog/rss.xml
- https://blog.google/technology/ai/rss/
- https://www.anthropic.com/news

STEP 2 — FILTER. Keep ONLY items relating to: EU AI Act / AI Act / Article 50 / high-risk AI / GPAI / AI regulation-governance-compliance; AI security / LLM security / prompt injection / jailbreak / adversarial AI / AI-agent security; ISO 42001 / ISO/IEC 42001 / ISO 27001+AI / AI management systems / AI standards; NIST AI / AI RMF / AI risk; GDPR+AI / DPIA+AI / AI data protection; AI incidents / chatbot liability / AI lawsuits / major data-breach fines; AND notable policy/safety/security announcements from major AI labs (Anthropic, OpenAI, xAI/Grok, Google DeepMind, Meta, Microsoft). Prefer items from the last ~3 weeks. When the SAME story is covered by multiple feeds, treat it as ONE story whose `sources` is the union of all covering channels. Do NOT fabricate; only include items whose source URL you actually have. Assign each a topic: exactly one of "AI Act", "AI Security", "Standards", "Incidents", "General". Call the result TODAY's new stories.

ΑΠΟΚΛΕΙΣΜΟΣ ΧΟΡΗΓΟΥΜΕΝΟΥ ΠΕΡΙΕΧΟΜΕΝΟΥ — απόλυτος κανόνας, ρητή εντολή της Maria 19/08/2026: «δεν θέλουμε να γράφουμε για πληρωμένα άρθρα».
Δεν αναδημοσιεύουμε διαφήμιση ως είδηση. Στις 17/08/2026 το κύριο θέμα της ημέρας ήταν κείμενο γραμμένο από content writer της Keeper Security, με δήλωση «contributed piece from one of our valued partners», που κατέληγε στο προϊόν τους. Πέρασε όλους τους ελέγχους επειδή το URL ζούσε και το περιεχόμενο ταίριαζε με τη σύνοψη. Αυτός ο κανόνας υπάρχει γι' αυτό ακριβώς.
ΓΙΑ ΚΑΘΕ ΥΠΟΨΗΦΙΑ ΝΕΑ ΙΣΤΟΡΙΑ, πριν την προσθέσεις: κατέβασε τη σελίδα του πρώτου source URL (`curl -sL --max-time 20`) και ψάξε για ενδείξεις χορηγίας — sponsored, sponsored content, paid content, advertorial, contributed by, contributed piece, "from our partners", "our valued partners", promoted, "in partnership with" — ή συγγραφέα που δηλώνεται ως στέλεχος ή content writer εταιρείας της οποίας το προϊόν προτείνεται μέσα στο κείμενο.
ΑΝ ΒΡΕΙΣ ΤΕΤΟΙΑ ΕΝΔΕΙΞΗ: ΑΠΟΡΡΙΨΕ την ιστορία εντελώς. ΔΕΝ μπαίνει στις σελίδες του radar, ΔΕΝ μπαίνει στο `knowledge/ai-security-log.md`, ΔΕΝ μπαίνει στο digest ως είδηση, ΔΕΝ μπαίνει στο LinkedIn draft.
ΕΞΑΙΡΕΣΗ: αν η ΙΔΙΑ είδηση καλύπτεται και από ανεξάρτητη πηγή, κράτα την ιστορία με ΜΟΝΟ την ανεξάρτητη πηγή και πέταξε τη χορηγούμενη από το `sources`.
ΔΙΑΦΑΝΕΙΑ: κάθε ιστορία που απέρριψες γι' αυτόν τον λόγο, κατέγραψέ την σε μία γραμμή στο τέλος του digest, σε ενότητα `## 🚫 Τι απορρίφθηκε`, με τον τίτλο, την πηγή και τον λόγο. Αν δεν απορρίφθηκε τίποτα, παράλειψε την ενότητα.

STEP 3 — LOAD THE EXISTING ARCHIVE. Read BOTH current files and parse their existing `const ITEMS = [...]` arrays (use python3 for robust JSON parsing):
- GREEK archive: `radar/index.html`
- ENGLISH archive: `en/radar/index.html`
Each existing item has: title, date, topic, summary, sources (array of {name,url}); a few legacy items may instead have flat `source`+`url` — normalise those to a one-element sources array. The GREEK file holds the Greek title/summary for each story; the ENGLISH file holds the English title/summary for the SAME stories (same order/keys). Pair them up by position/URL so each story has both a GR and an EN text.

STEP 4 — MERGE (the core of the job).
- Identity key for a story = the set of its source URLs (normalise: lowercase, strip trailing slash and query/fragment). Two items are the SAME story if they share ANY source URL, OR if their titles are near-identical.
- For each of TODAY's new stories: if it matches an existing archived story, MERGE — keep the existing GR/EN text, take the union of `sources` (dedup by URL), and keep the EARLIEST `date`. If it's genuinely new, ADD it (you must now author BOTH a GR and an EN title+summary for it, per STEP 5 language rules).
- Keep existing archived stories that did NOT reappear today — they stay (that's the whole point).
- Then prune the merged list to a ROLLING WINDOW: keep only stories whose `date` is within the last 30 days of today; if more than 40 remain, keep the 40 most recent by date. Sort newest first.
- The GR list and the EN list MUST contain the EXACTLY SAME stories in the EXACTLY SAME order — only the title+summary language differs. Every story must have non-empty GR text in the GR file and non-empty EN text in the EN file.

STEP 5 — LANGUAGE RULES for any story whose text you are authoring (new stories only; carryovers reuse stored text).
- GREEK page: `title` and `summary` in natural Greek. Keep common tech terms / product & org names as-is (Anthropic, OpenAI, Gemini, ChatGPT, Langflow, LiteLLM, CVE-…, RCE, prompt injection, LLM, chatbot, AI agent, CISA, ENISA). `sources[].name` stay as the original publication names. `topic` stays one of the English keys above (the page maps them to Greek labels itself).
- ENGLISH page: `title` and `summary` in English.
Each item object has exactly: `title`, `date` ("YYYY-MM-DD"), `topic`, `summary`, `sources` (ARRAY of {"name","url"}). Escape double quotes (prefer json.dumps with ensure_ascii=False).

STEP 6 — WRITE FILES. For EACH file, replace ONLY: (a) the `const ITEMS = [...]` array (with the matching-language merged list), (b) `const GENERATED = "YYYY-MM-DD";` to today, (c) the visible id="upd" line. Keep everything else byte-for-byte identical (CSS, render functions, disclaimer, CTA, language switcher). Write back to the SAME path.
- GREEK: id="upd" line → `ΕΝΗΜΕΡΩΘΗΚΕ: DD MON YYYY` (uppercase Greek month abbrev, e.g. "14 ΙΟΥΝ 2026").
- ENGLISH: id="upd" line → `UPDATED: DD MON YYYY` (English month abbrev).
Sanity-check each: valid JSON array, every item has all 5 keys with a non-empty sources array, GR and EN have the same item count, <script> still has render(). SAFETY: if STEP 1 gathering failed entirely (all feeds empty) OR you could not parse the existing archive, do NOT overwrite — leave BOTH files completely untouched and just report. Never write an empty or shrunken-by-accident list.

MANDATORY VERIFICATION before you finish (do NOT skip this): run `python3 .github/radar_check.py` from the repo root and read its output. If it fails, your written files are wrong — fix them (or restore with `git checkout -- radar en/radar knowledge`) and try again until the check passes. The merged ITEMS count must be close to the pre-existing count (existing stories carried over + new ones − aged-out ones). It is FORBIDDEN to report success while the check fails or while the files contain fewer stories than the archive you loaded in STEP 3. Reporting «40 items written» without having verified it is the exact failure mode this paragraph exists to prevent.

STEP 7 — DIGEST FOR MARIA. If (and ONLY if) today's run added at least one genuinely NEW story to the archive, write a Greek digest to `/tmp/radar-digest.md` (OUTSIDE the repo — this file must never be committed). Audience: Maria (θeta ai) — an AI security & compliance consultant in Greece who wants to genuinely understand the market, not just headlines. Content, all in natural Greek (keep tech terms/product names as-is):
- Start with `@mbartzoka-ui` on its own line (guarantees the email notification), then a 2-3 sentence overview of the day's picture.
- Then one section per NEW story: a bold title, 3-5 sentences of substantiated summary — τι έγινε, γιατί έχει σημασία, και όπου ταιριάζει μία πρόταση «τι σημαίνει για την ελληνική αγορά / για πελάτες MME» — followed by the source links as markdown.
- Close with a short «Συνολική εικόνα» paragraph connecting the day's items to broader trends.
Base every claim ONLY on the fetched feed content — no speculation presented as fact. If there are NO new stories today, do NOT create the file at all.

ΜΗΝ ΞΑΝΑΓΡΑΦΕΙΣ ΘΕΜΑ ΠΟΥ ΕΧΕΙ ΗΔΗ ΓΡΑΦΤΕΙ — απόλυτος κανόνας, ρητή εντολή της Maria 19/08/2026: «δεν θέλουμε να γράφουμε για άρθρα για τα οποία έχουμε ξαναγράψει».
ΠΡΙΝ διαλέξεις θέμα για το draft, διάβασε `knowledge/posted-topics.txt` (μία γραμμή ανά θέμα, `#` = σχόλιο).
ΑΠΑΓΟΡΕΥΕΤΑΙ draft για θέμα που υπάρχει ήδη εκεί — ακόμη κι αν σήμερα βγήκε φρέσκο ρεπορτάζ γι' αυτό, ακόμη κι αν το ρεπορτάζ προσθέτει νέα λεπτομέρεια. Νέο ρεπορτάζ παλιάς ιστορίας ΔΕΝ είναι νέο θέμα. (Παράδειγμα του τι πήγε στραβά: η παραβίαση του Hugging Face έχει 8 εγγραφές στο ημερολόγιο, 20-28/07/2026, και ξαναγράφτηκε στις 19/08.)
ΔΙΑΛΕΞΕ ΕΝΑ ΘΕΜΑ, ΟΧΙ ΤΡΙΑ. Το draft στέκεται σε μία ιστορία και πάει βαθιά.
ΠΑΡΕ ΘΕΣΗ. Πρέπει να υπάρχει κάτι που ισχυρίζεσαι, όχι μόνο κάτι που περιγράφεις: τι σημαίνει, τι είναι λάθος, τι πρέπει να αλλάξει, τι να ρωτήσει ο αναγνώστης και ποιον. Περίληψη ειδήσεων με γενικό δίδαγμα στο τέλος («το θέμα δεν είναι η τεχνολογία, είναι η εμπιστοσύνη») ΔΕΝ είναι post — είναι δελτίο.
ΑΝ ΚΑΝΕΝΑ σημερινό θέμα δεν είναι καινούργιο, ή αν κανένα δεν σηκώνει θέση: ΜΗΝ γράψεις draft. Γράψε στη θέση του τη γραμμή «Σήμερα δεν υπάρχει θέμα που να σηκώνει ανάρτηση: <σύντομος λόγος>». Καμία ανάρτηση είναι καλύτερη από αδύναμη ανάρτηση, και η Maria το προτιμά ρητά.
ΑΦΟΥ γράψεις draft, πρόσθεσε το θέμα στο ΤΕΛΟΣ του `knowledge/posted-topics.txt`, μία γραμμή στη μορφή:
`YYYY-MM-DD | σύντομο-slug | ο τίτλος της ιστορίας`
ΠΟΤΕ μη διαγράψεις, μην αλλάξεις και μην αναδιατάξεις υπάρχουσα γραμμή. Αν το αρχείο λείπει, φτιάξ' το με την επικεφαλίδα `# Θέματα που έχουν ήδη γίνει LinkedIn draft — append-only.`

After the «Συνολική εικόνα» paragraph, add a horizontal rule and a section titled `## 📣 LinkedIn draft — copy & paste` containing ONE ready-to-post LinkedIn text in GREEK, authored for Maria's personal profile (AI security & compliance consultant, brand «θeta ai»). Format: 900-1600 characters, plain text (no markdown — LinkedIn doesn't render it). Write it as a short, well-crafted mini-article, not a news list: a strong opening hook (1-2 lines), then flowing prose that weaves the day's 2-4 stories into one narrative with a common thread, and a closing thought that leaves the reader with something to act on. PERSPECTIVE: strictly business-wise — every story is told from the side of the επιχειρηματίας/decision-maker (τι κινδυνεύει, τι απόφαση προκύπτει, τι κόστος ή ευκαιρία), not from the side of the researcher or the technology itself. LANGUAGE QUALITY: care about the prose — καλογραμμένα, ρέοντα ελληνικά με εικόνες και ρυθμό, όπως ένα καλό άρθρο γνώμης· still simple and jargon-free, but never dry or listy. End with EXACTLY these closing lines, in this order:

```
Καθημερινή ενημέρωση: thetaai.gr/radar

Αυτό το post δημιουργήθηκε αυτόματα με AI, μέρος του content workflow της ThetaAI. Θέλεις παρόμοιο αυτοματισμό για την επιχείρησή σου; → thetaai.gr
```

followed by 3-4 hashtags (#AISecurity #AIAct plus topical ones). STYLE: apply the WRITING RULES section near the top of this prompt IN FULL, all ten of them, plus the ΡΥΘΜΟΣ ΚΑΙ ΜΗΚΟΣ ΠΡΟΤΑΣΕΩΝ block right below, which is stricter and wins here. Four additions specific to LinkedIn: at most one emoji and usually zero; 3-4 hashtags maximum; plain text only, since LinkedIn does not render markdown; the jargon ban is absolute in this draft (no sandboxing, no data residency, no orchestration) and every technical term gets a plain-Greek gloss the first time it appears, e.g. «AI agent, εργαλείο AI που εκτελεί εργασίες μόνο του» or «browser extension, πρόσθετο του browser». Before you finalise the draft, re-read it once against the WRITING RULES and fix what slipped, checking the dash rule first. This is a DRAFT for Maria to review and post manually; never post anywhere yourself.

ΡΥΘΜΟΣ ΚΑΙ ΜΗΚΟΣ ΠΡΟΤΑΣΕΩΝ — διόρθωση 19/08/2026, μετά από ρητή παρατήρηση της Maria ότι το κείμενο "χρησιμοποιεί πολύ μικρές προτάσεις, είναι ενοχλητικό και είναι pattern AI". Αυτό είναι το ΠΙΟ ΣΥΧΝΟ σφάλμα σε αυτό το draft· αντιμετώπισέ το ως σκληρό κανόνα, όχι ως προτίμηση.
- Η ΠΛΕΙΟΨΗΦΙΑ των προτάσεων πρέπει να έχει 15 έως 35 λέξεις, με δευτερεύουσες προτάσεις, όπως γράφει άνθρωπος που σκέφτεται καθώς γράφει. Άφησε τουλάχιστον μία σκέψη να τρέξει μακριά πριν κλείσει.
- Η κοφτή πρόταση (κάτω από 8 λέξεις) είναι ΕΡΓΑΛΕΙΟ ΕΜΦΑΣΗΣ, όχι ύφος. ΤΟ ΠΟΛΥ ΔΥΟ σε ολόκληρο το κείμενο, και ΠΟΤΕ δύο στη σειρά.
- ΑΠΑΓΟΡΕΥΕΤΑΙ παράγραφος που αποτελείται από μία και μόνο κοφτή πρόταση, πάνω από μία φορά σε όλο το κείμενο.
- ΑΠΑΓΟΡΕΥΕΤΑΙ το σχήμα «Δεν είναι Χ. Είναι Υ.» πάνω από μία φορά.
- ΑΠΑΓΟΡΕΥΟΝΤΑΙ οι τριάδες παράλληλων κοφτών προτάσεων (π.χ. «Δεν φαίνονται πουθενά. Δεν γράφονται στη σύμβαση. Δεν τα ξέρεις.»). Είναι το πιο χαρακτηριστικό σημάδι κειμένου από AI. Γράψε το ως ΜΙΑ πρόταση με κόμματα.
ΥΠΟΧΡΕΩΤΙΚΟΣ ΕΛΕΓΧΟΣ πριν οριστικοποιήσεις το draft: μέτρησε τις προτάσεις. Αν περισσότερες από το ΕΝΑ ΤΡΙΤΟ έχουν κάτω από 10 λέξεις, το κείμενο είναι σταccato — ξαναγράψ' το ενώνοντας προτάσεις, πριν το γράψεις στο αρχείο.

After the LinkedIn draft, add a horizontal rule and a section titled `## 📚 Όροι της ημέρας`. Purpose: Maria is a consultant with a business, not an IT, background and is deliberately building her technical vocabulary from the radar. This section teaches ONLY the terms that are genuinely new to her.

MANDATORY DEDUPLICATION — do this FIRST, before writing anything in this section. Read `knowledge/known-terms.txt` (one term per line; lines starting with `#` are comments; matching is case-insensitive and ignores Greek/English variants of the same concept). Explain ONLY terms appearing in TODAY'S NEW stories that are NOT already in that list. If every technical term in today's stories is already known, write the single line «Κανένας νέος όρος σήμερα.» and nothing more — do NOT pad this section with terms she already has, and do NOT invent terms that are not actually in today's stories.

For each genuinely new term, exactly three lines in GREEK:
- **<όρος>** — τι είναι, σε ΜΙΑ πρόταση απλών ελληνικών. Κρίσιμος κανόνας: μη χρησιμοποιήσεις μέσα στην εξήγηση άλλον άγνωστο τεχνικό όρο. Αν χρειάζεται, δώσε μια σύντομη, συγκεκριμένη εικόνα («ο κούριερ δεν κουβαλά τη βόμβα, κουβαλά τη διεύθυνση»).
- *Γιατί έχει σημασία:* μία πρόταση από τη σκοπιά του επιχειρηματία ή του συμβούλου — τι κινδυνεύει, τι απόφαση προκύπτει, τι κόστος.
- *Πού βγήκε:* ο τίτλος της σημερινής ιστορίας όπου εμφανίστηκε.

THEN append every term you actually explained to the END of `knowledge/known-terms.txt`, one per line, lowercase, no bullets. This file IS committed by the workflow (unlike the digest), so tomorrow's run will not repeat today's terms. NEVER modify, reorder or delete existing lines in that file — append only. If the file is somehow missing, create it with the header line `# Όροι που έχουν εξηγηθεί στη Μαρία — append-only. Μη διαγράφεις γραμμές.`

STEP 8 — PERMANENT KNOWLEDGE LOG. For EVERY genuinely NEW story added today, APPEND an entry to `knowledge/ai-security-log.md` (it exists; if somehow missing, recreate it with its header). This file is Maria's permanent knowledge archive — unlike the radar pages it is never pruned. Rules: append at the END of the file, NEVER modify or delete existing entries, use the GREEK title/summary, exact format:

```
## YYYY-MM-DD — <Greek title>
- **Θέμα:** <topic>
- **Τι έγινε:** <Greek summary>
- **Πηγές:** [Name](url) · [Name](url)
```

Stories that merely MERGED into existing archive entries (already known) are NOT re-appended.

STEP 9 — REPORT one short line to stdout: how many stories new vs carried-over, total in the archive, today's date, and whether a digest was written. Informational only (not legal advice). Do NOT commit, do NOT push, do NOT touch any other file in the repository.
