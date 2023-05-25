import datetime
from typing import Dict, List

import pyodata
import requests

from src.common import ScrapedData


class KnessetOdata:
    SERVICE_URL = 'https://knesset.gov.il/Odata/ParliamentInfo.svc/'

    def __init__(self):
        self.client = pyodata.Client(self.SERVICE_URL, requests.Session())

    def get_committees(self, knesset_num=25) -> Dict[str, int]:
        res = self.client.entity_sets.KNS_Committee.get_entities().filter(f'KnessetNum eq {knesset_num}').execute()
        return {cmt.CommitteeID: cmt.Name for cmt in res}

    def get_committee_session_ids_by_filter(self,
                                            committee_id=None,
                                            from_date: datetime.datetime = None,
                                            to_date: datetime.datetime = None) -> List[int]:
        filters_list = []
        if committee_id:
            filters_list.append(f'CommitteeID eq {committee_id}')
        if from_date:
            filters_list.append(f"StartDate gt datetime'{from_date}'")
        if to_date:
            filters_list.append(f"EndDate lt datetime'{to_date}'")
        filter_str = ' and '.join(filters_list)
        print(filter_str)

    def get_documents_by_session_id(self, session_id: int) -> List[ScrapedData]:
        pass


if __name__ == '__main__':
    knesset_data = KnessetOdata()
    # knesset_data.get_committee_session_ids_by_filter(committee_id=991)
    knesset_data.get_committee_session_ids_by_filter(committee_id=991, start_date=datetime.datetime.now())
    # print(knesset_data.get_committees())
