import logging
log = logging.getLogger(__name__)

import io, csv
from django.core.files import File
from election_results.api.serializers import (
    ConstituencySerializer,
    PartySerializer,
    PartyVoteCountSerializer,
    TotalResultsSerializer,
    UploadSerializer,
)
from election_results.models import Constituency, Party, PartyVoteCount
from rest_framework import views, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

class ConstituencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows constituencies to be viewed, but not edited.
    """
    queryset = Constituency.objects_ordered()
    serializer_class = ConstituencySerializer


class PartyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows parties to be viewed, but not edited.
    """
    queryset = Party.objects_ordered()
    serializer_class = PartySerializer


class PartyVoteCountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows party vote counts to be viewed, but not edited.
    """
    queryset = PartyVoteCount.objects.all()
    serializer_class = PartyVoteCountSerializer


class TotalResultsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows party total results to be viewed.
    """
    queryset = Party.objects_ordered()
    serializer_class = TotalResultsSerializer


class FileUploadView(views.APIView):
    """
    API endpoint (POST only) for uploading an election results file.
    """
    serializer_class = [UploadSerializer]

    def post(self, request, filename, *args, **kwargs):
        field_name = "file"
        if field_name in request.FILES:
            in_mem_file = request.FILES[field_name]

            # Read csv file InMemoryUploadedFile
            file = in_mem_file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(file), escapechar="\\", fieldnames=[])

            for line in reader:
                values = line[None]

                # Nothing to do when no party counts are present.
                if len(values) < 2:
                    log.warn(f"No party counts; skipping (line: {line})")
                    continue

                constituency_name, party_counts = values[0].strip(), [v.strip() for v in values[1:]]

                # Check repeating set of pairs of count and party code
                n_party_fields = len(party_counts)
                if n_party_fields % 2 != 0:
                    log.error(f"Odd party field count; skipping (line: {line})")
                n_parties = int(n_party_fields / 2)

                for i in range(n_parties):
                    try:
                        count, party_code = int(party_counts[i*2]), party_counts[i*2 + 1]
                    except ValueError:
                        log.error(f"Invalid count {count} for party code {party_code}; skipping")
                    else:
                        constituency, created = Constituency.objects.get_or_create(name=constituency_name)
                        constituency.update_vote_counts(party_code=party_code, count=count)

            return Response(status=200)
        else:
            return Response(status=400)
