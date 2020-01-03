from data.models import NrClasses, NrChains, NrReleases
from infrastructure.utility import reject_ife

REJECT_LIST = ['5AFI|1|a', '5LZE|1|A', '5LZA|1|a', '5WFK|1|a', '4WRO|1|3L', '4WSD|1|1K', '4WSD|1|1L', '4WSD|1|3L', '4WT1|1|1K', '4WT1|1|1L',
               '5U4J|1|a', '4WT1|1|3K', '4WT1|1|3L', '4WZO|1|3K', '4WZO|1|3L', '4Y4P|1|1w', '3R8N|1|A', '3R8O|1|A',
               '4V80|1|CA', '4V80|1|AA']


def get_ec_members(query_ife):
    ife_list = NrChains.query.join(NrClasses, NrReleases) \
        .filter(NrChains.ife_id == query_ife).filter(NrClasses.resolution == '4.0') \
        .order_by(NrReleases.date.desc()).limit(1)
    for row in ife_list:
        class_id = row.nr_class_id

    members_query = NrChains.query.filter_by(nr_class_id=class_id)
    ec_members = []
    for row in members_query:
        ec_members.append(row.ife_id)

    rejected_members, cleaned_ec_members = reject_ife(ec_members, REJECT_LIST)

    members_pdb = []
    members_chain = []

    for ife in cleaned_ec_members:
        members_pdb.append(ife.split('|')[0])
        members_chain.append(ife.split('|')[-1])

    members_info = zip(members_pdb, members_chain)

    return rejected_members, members_info
