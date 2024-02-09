import logging
log = logging.getLogger(__name__)

from django.db.models import (
    CASCADE,
    CharField,
    F,
    ForeignKey,
    Max,
    Model,
    OuterRef,
    PositiveIntegerField,
    Subquery,
    Sum,
)

class OrderByNameMixin:
    """
    Model mixin to provide a MyModel.objects_ordered()
    equivalent to MyModel.objects.order_by("name").
    """

    @classmethod
    def objects_ordered(cls):
        """
        Returns:
            django.db.query.QuerySet:
                All party objects, ordered by name ascending (alphabetic).
        """
        return cls.objects.all().order_by("name")


class Constituency(Model, OrderByNameMixin):
    """A political constituency."""

    """
    Constituency name.
    Current max length constituency name is 38 chars
    ('Cumbernauld, Kilsyth and Kirkintilloch East')
    but let's allow extra space for the future.
    """
    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return f"name={self.name}"

    @property
    def vote_counts_desc(self):
        """
        Returns:
            django.db.query.QuerySet:
                All vote counts (PartyVoteCount) for this constituency,
                sorted by descending vote count (i.e. most votes first).
        """
        return self.vote_counts.order_by("-count")

    @property
    def total_vote_count(self):
        """
        Returns:
            int:
                Total number of votes cast across all parties in this constituency.
        """
        return next(iter(self.vote_counts.aggregate(Sum('count')).values()))

    @property
    def winning(self):
        """
        Returns:
            django.db.query.QuerySet:
                The Party currently winning in this constituency,
                or multiple parties in case of a vote tie,
                or no parties in case of no vote submissions.
        """
        # Identify party vote count object(s) with the max count amongst 'self.vote_counts'
        qs = self.vote_counts.filter(count=next(iter(self.vote_counts.aggregate(Max("count")).values())))
        # Translate these to party objects.
        return Party.objects.filter(id__in=qs.values_list("party__id", flat=True))

    def update_vote_counts(self, party_code, count):
        """
        Creates or replaces the related PartyVoteCount.

        Args:
            party_code (str):
                The 'code' for a Party object.
            count (int):
                The vote count.

        Raises:
            Party.DoesNotExist:
                If no Party with code `party_code` exists.
        """
        party = Party.objects.get(code=party_code)
        vote_counts, created = self.vote_counts.get_or_create(party=party)
        vote_counts.count = count
        vote_counts.save()


class Party(Model, OrderByNameMixin):
    """A political party."""

    """The party name shortform aka 'code'. Common sense max length chosen (not defined in spec)."""
    code = CharField(max_length=8, unique=True)

    """The party name. Common sense max length chosen (not defined in spec)."""
    name = CharField(max_length=64, unique=True)

    def __str__(self):
        return f"name={self.name}, code={self.code}"

    @property
    def mp_count(self):
        """
        Returns:
            int:
                Number of MPs according to current election results,
                i.e. number of constituencies where this party is winning
                (or has won, post-election).
        """
        return len([c for c in Constituency.objects.all() if self in c.winning])

    @property
    def total_vote_count(self):
        """
        Returns:
            int:
                Total number of votes cast for this party across all constituencies.
        """
        return next(iter(PartyVoteCount.objects.filter(party=self).aggregate(Sum("count")).values())) or 0

    @classmethod
    def as_dict_by_code(cls):
        """
        Returns:
            dict:
                All party objects as a single dictionary, with entries of form:
                    code <str>: name <str>
        """
        return { o.code:o.name for o in cls.objects_ordered() }

    @classmethod
    def as_dict_by_name(cls):
        """
        Returns:
            dict:
                All party objects as a single dictionary, with entries of form:
                    name <str>: code <str>
        """
        return { o.name:o.code for o in cls.objects_ordered() }


class PartyVoteCount(Model):

    constituency = ForeignKey(Constituency, on_delete=CASCADE, related_name="vote_counts")
    party = ForeignKey(Party, on_delete=CASCADE, related_name="vote_counts")
    count = PositiveIntegerField(default=0) 

    def __str__(self):
        return f"constituency={self.constituency.name}, party={self.party.name}, count={self.count}"

    @property
    def total_vote_share(self):
        """
        Returns:
            float:
                Percentage share (out of 100) of total votes cast for the given constituency.
        """
        return 100 * (self.count / self.constituency.total_vote_count)
