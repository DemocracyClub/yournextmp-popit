from collections import defaultdict
import json

from candidates.popit import PopItApiMixin, popit_unwrap_pagination
from candidates.static_data import MapItData, PartyData

from django.core.management.base import BaseCommand

class Command(PopItApiMixin, BaseCommand):

    def handle(self, **options):
        all_constituencies = MapItData.constituencies_2010_name_sorted
        all_parties = PartyData.party_id_to_name

        counts = {
            'candidates_2015': 0,
            'parties': {n: 0 for n in all_parties.values()},
            'constituencies': {n[1]['name']: 0 for n in all_constituencies},
        }

        for person in popit_unwrap_pagination(
                self.api.persons,
                embed="membership.organization",
                per_page=100
        ):
            if '2015' in person['standing_in'] and person['standing_in'][
                '2015']:
                counts['candidates_2015'] += 1

                party_name = person['party_memberships']['2015']['name']
                counts['parties'][party_name] += 1

                constituency_name = person['standing_in']['2015']['name']
                counts['constituencies'][constituency_name] += 1

        print json.dumps(counts, indent=4)