from election_results.models import Constituency, Party, PartyVoteCount
from rest_framework.serializers import (
    FileField,
    HyperlinkedModelSerializer,
    Serializer,
    SerializerMethodField,
    SlugRelatedField,
)


class PartySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Party
        fields = ["id", "code", "name"]


class PartyVoteCountSerializer(HyperlinkedModelSerializer):

    party = SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
     )

    vote_share = SerializerMethodField()

    def get_vote_share(self, obj):
        return obj.total_vote_share

    class Meta:
        model = PartyVoteCount
        fields = ["party", "count", "vote_share"]


class ConstituencySerializer(HyperlinkedModelSerializer):

    vote_counts = SerializerMethodField()
    winning = SerializerMethodField()

    def get_vote_counts(self, obj):
        objs = obj.vote_counts.order_by("party__name") # order alphabetically by name
        # objs = obj.vote_counts.order_by("-count") # order by descending count
        return PartyVoteCountSerializer(objs, many=True, read_only=True).data

    def get_winning(self, obj):
        return sorted([o.name for o in obj.winning])

    class Meta:
        model = Constituency
        fields = ["id", "name", "vote_counts", "winning"]


class TotalResultsSerializer(HyperlinkedModelSerializer):

    mp_count = SerializerMethodField()
    vote_count = SerializerMethodField()

    def get_mp_count(self, obj):
        """
        Returns:
            int:
                MP Count for this party, based on current vote counts.
        """
        return obj.mp_count

    def get_vote_count(self, obj):
        """
        Returns:
            int:
                Total votes for this party.
        """
        return obj.total_vote_count

    class Meta:
        model = Party
        fields = ["id", "code", "name", "mp_count", "vote_count"]


class UploadSerializer(Serializer):
    file = FileField()
