"""Δημοσιεύει στο LinkedIn το «LinkedIn draft» του σημερινού digest.

Χρήση:  python3 .github/radar_linkedin.py /tmp/radar-issue-body.md

Τυπώνει ΜΙΑ γραμμή αποτελέσματος για το workflow:
  POSTED <url>       δημοσιεύτηκε
  SKIPPED <λόγος>    σκόπιμα δεν δημοσιεύτηκε (δεν είναι σφάλμα)
Σε σφάλμα του LinkedIn βγαίνει με κωδικό 1.

ΓΙΑΤΙ ΔΕΝ ΔΗΜΟΣΙΕΥΕΙ ΠΑΝΤΑ:
- Όταν ο radar γράφει «Σήμερα δεν υπάρχει θέμα που να σηκώνει ανάρτηση»,
  αυτή η γραμμή ΔΕΝ είναι ποστ. Η Maria προτιμά ρητά καμία ανάρτηση από
  αδύναμη ανάρτηση.
- Όταν το digest γράφτηκε με Haiku, το ίδιο το workflow προειδοποιεί ότι
  «το κείμενο για LinkedIn θέλει δούλεμα πριν το ποστάρεις». Δεν το
  ποστάρουμε αυτόματα· μένει στο email για χειροκίνητη χρήση.

Μόνο stdlib, για να μη χρειάζεται pip install στο runner.
"""
import json
import os
import sys
import urllib.error
import urllib.request

HEADING = "## 📣 LinkedIn draft"
NO_TOPIC = "Σήμερα δεν υπάρχει θέμα"
HAIKU_WARNING = "έτρεξε με Haiku"
POSTS_URL = "https://api.linkedin.com/rest/posts"
LINKEDIN_VERSION = "202604"
MIN_CHARS = 300  # κάτω από αυτό κάτι κόπηκε στραβά, όχι ποστ


def extract_draft(body):
    """Το κείμενο κάτω από τον τίτλο του draft, ως την επόμενη ενότητα.

    Η ενότητα κλείνει σε γραμμή `---` ή σε επόμενο `## `. Γραμμές που
    είναι σκέτο ``` (αν ο radar τύλιξε το κείμενο σε code block) πετιούνται.
    """
    lines = body.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith(HEADING)), None)
    if start is None:
        return None
    out = []
    for line in lines[start + 1:]:
        if line.strip() == "---" or line.startswith("## "):
            break
        if line.strip().startswith("```"):
            continue
        out.append(line)
    return "\n".join(out).strip() or None


def decide(body):
    """(text, None) για δημοσίευση, ή (None, λόγος) για παράλειψη."""
    if HAIKU_WARNING in body:
        return None, "το digest γράφτηκε με Haiku, το draft θέλει δούλεμα"
    draft = extract_draft(body)
    if draft is None:
        return None, "δεν βρέθηκε ενότητα LinkedIn draft"
    if draft.startswith(NO_TOPIC):
        return None, "ο radar έκρινε ότι σήμερα δεν υπάρχει θέμα για ανάρτηση"
    if len(draft) < MIN_CHARS:
        return None, f"το draft είναι ύποπτα μικρό ({len(draft)} χαρακτήρες)"
    return draft, None


def publish(text, token, author):
    body = json.dumps({
        "author": author,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }).encode("utf-8")
    req = urllib.request.Request(POSTS_URL, data=body, method="POST", headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": LINKEDIN_VERSION,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            post_id = resp.headers.get("x-restli-id", "")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        raise RuntimeError(f"LinkedIn {exc.code}: {detail}") from exc
    return f"https://www.linkedin.com/feed/update/{post_id}"


def main():
    with open(sys.argv[1], encoding="utf-8") as fh:
        body = fh.read()
    text, reason = decide(body)
    if text is None:
        print(f"SKIPPED {reason}")
        return 0
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "")
    author = os.environ.get("LINKEDIN_AUTHOR_URN", "")
    if not token or not author:
        print("SKIPPED λείπουν τα secrets LINKEDIN_ACCESS_TOKEN / LINKEDIN_AUTHOR_URN")
        return 0
    try:
        url = publish(text, token, author)
    except Exception as exc:
        print(f"ERROR {exc}")
        return 1
    print(f"POSTED {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
