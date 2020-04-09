import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

conn_str = 'mysql+pymysql://root:root@127.0.0.1/rna3dhub-next?' \
           'unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock'

print "Connecting to DB with {}".format(conn_str)

engine = create_engine(conn_str)
Base = declarative_base(engine)


class UnitCorrespondence(Base):
    __tablename__ = "correspondence_units"

    # correspondence_id = db.Column(db.String, primary_key=True)
    unit_id_1 = sa.Column(sa.String, primary_key=True)
    unit_id_2 = sa.Column(sa.String, primary_key=True)
    pdb_id_1 = sa.Column(sa.String, primary_key=True)
    pdb_id_2 = sa.Column(sa.String, primary_key=True)
    chain_name_2 = sa.Column(sa.String, primary_key=True)


# ----------------------------------------------------------------------

def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

