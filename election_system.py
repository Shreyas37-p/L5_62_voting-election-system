
"""Voting and election management system."""

from datetime import datetime, time
from secrets import randbelow
from defusedxml import ElementTree

MINIMUM_VOTING_AGE = 18
POLLS_CLOSE_TIME = time(18, 0)
ELECTION_OFFICER_ROLE = "election_officer"

voters = {}
candidates = ["Alice", "Bob", "NOTA"]
ballots = []


def register_voter(voter_id, age):
    """Register a voter if the voter meets the minimum age requirement."""
    if age < MINIMUM_VOTING_AGE or voter_id in voters:
        return False

    voters[voter_id] = {"age": age, "voted": False}
    return True


def is_officer(role):
    """Return whether the supplied role is an election officer."""
    return role == ELECTION_OFFICER_ROLE


def cast_vote(voter_id, candidate, when=None):
    """Record one valid vote before polls close."""
    if when is None:
        when = datetime.now().time()

    if voter_id not in voters:
        return False

    if voters[voter_id]["voted"]:
        return False

    if when >= POLLS_CLOSE_TIME:
        return False

    candidate_lookup = {name.casefold(): name for name in candidates}
    canonical_candidate = candidate_lookup.get(candidate.casefold())

    if canonical_candidate is None:
        return False

    ballots.append(
        {
            "voter_id": voter_id,
            "candidate": canonical_candidate,
            "receipt": receipt_number(),
        }
    )
    voters[voter_id]["voted"] = True
    return True


def tally_votes(ballot_list=None):
    """Return vote counts for every candidate."""
    if ballot_list is None:
        ballot_list = ballots

    tally = {candidate: 0 for candidate in candidates}

    for ballot in ballot_list:
        candidate = ballot.get("candidate")
        if candidate in tally:
            tally[candidate] += 1

    return tally


def winner():
    """Return the winner, or the tied candidates if applicable."""
    tally = tally_votes()
    if not tally or max(tally.values(), default=0) == 0:
        return None

    highest_count = max(tally.values())
    winners = [
        candidate
        for candidate, count in tally.items()
        if count == highest_count
    ]

    return winners[0] if len(winners) == 1 else winners


def vote_percent(candidate):
    """Return a candidate's percentage of all valid ballots."""
    total = len(ballots)
    if total == 0:
        return 0.0

    tally = tally_votes()
    return tally.get(candidate, 0) * 100.0 / total


def turnout_percent():
    """Return the percentage of registered voters who cast a ballot."""
    total_voters = len(voters)
    if total_voters == 0:
        return 0.0

    voted_count = sum(
        1 for voter in voters.values() if voter["voted"]
    )
    return voted_count * 100.0 / total_voters


def count_for(candidate, ballot_list=None):
    """Count valid ballots for a specific candidate."""
    return tally_votes(ballot_list).get(candidate, 0)


def announcements():
    """Generate one announcement per candidate."""
    tally = tally_votes()
    return [
        f"{candidate}: {tally[candidate]}"
        for candidate in candidates
    ]


def receipt_number():
    """Generate a receipt identifier."""
    return f"RCPT-{randbelow(1_000_000):06d}"


def import_postal_ballots(xml_data):
    """Import valid XML postal ballots without unsafe XML parsing."""
    try:
        root = ElementTree.fromstring(xml_data)
    except (ElementTree.ParseError, TypeError, ValueError):
        return 0

    imported = 0

    for ballot in root.findall(".//ballot"):
        voter_id = ballot.findtext("voter_id")
        candidate = ballot.findtext("candidate")

        if not voter_id or not candidate:
            continue

        if voter_id not in voters:
            continue

        if voters[voter_id]["voted"]:
            continue

        if cast_vote(voter_id, candidate):
            imported += 1

    return imported


def main():
    """Run a demonstration of the election system."""
    register_voter("Asha", 18)
    register_voter("Ben", 25)
    register_voter("Chen", 30)
    register_voter("Dia", 28)

    print("Register Asha (age 18):", "Asha" in voters)
    print("Is a plain 'voter' an election officer?", is_officer("voter"))
    print("Ben votes Alice:", cast_vote("Ben", "Alice"))
    print("Ben votes Alice again:", cast_vote("Ben", "Alice"))
    print("Chen votes 'bob':", cast_vote("Chen", "bob"))
    print(
        "Dia votes Bob at 18:30:",
        cast_vote("Dia", "Bob", datetime(2026, 1, 1, 18, 30).time()),
    )

    postal_xml = """
    <ballots>
        <ballot>
            <voter_id>Asha</voter_id>
            <candidate>Bob</candidate>
        </ballot>
    </ballots>
    """
    print("Postal ballots imported:", import_postal_ballots(postal_xml))
    print("Tally:", tally_votes())
    print("Winner:", winner())
    print("Alice %:", vote_percent("Alice"))
    print("Turnout %:", turnout_percent())
    print("Announcements:", announcements())

    if ballots:
        print("Receipt:", ballots[0]["receipt"])


if __name__ == "__main__":
    main()
