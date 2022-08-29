"""initial data migration

Revision ID: b0d8fe0babc9
Revises: a56462c1c1d3
Create Date: 2022-04-05 13:10:34.484971

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import create_engine
from sqlalchemy.sql import text

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

INSERT_ROWS = """INSERT INTO pieces VALUES(1,'Haydn_Sonata_Hob._XVI37_Mov._1_D_Major','./resources/midi/full/Haydn_Sonata_Hob._XVI37_Mov._1_D_Major.mid');
INSERT INTO pieces VALUES(2,'cmaj','./resources/midi/full/cmaj.mid');
INSERT INTO pieces VALUES(3,'Happy_Birthday_To_You_C_Major','./resources/midi/full/Happy_Birthday_To_You_C_Major.mid');
INSERT INTO pieces VALUES(4,'Haydn_Hob._XVI34_1._Presto','./resources/midi/full/Haydn_Hob._XVI34_1._Presto.mid');
INSERT INTO subpieces VALUES(1,'Happy_Birthday_To_You_C_Major-Part2','./resources/midi/subpieces/Happy_Birthday_To_You_C_Major-Part2.mid',3,0);
INSERT INTO subpieces VALUES(2,'Haydn_Hob.XVI34_1-1','./resources/midi/subpieces/Haydn_Hob.XVI34_1-1.mid',4,0);
INSERT INTO subpieces VALUES(3,'Haydn_Hob.XVI34_1-2','./resources/midi/subpieces/Haydn_Hob.XVI34_1-2.mid',4,0);
INSERT INTO subpieces VALUES(4,'Haydn_Hob.XVI34_1-3','./resources/midi/subpieces/Haydn_Hob.XVI34_1-3.mid',4,0);
INSERT INTO subpieces VALUES(5,'Haydn_Hob.XVI34_1-4','./resources/midi/subpieces/Haydn_Hob.XVI34_1-4.mid',4,0);
INSERT INTO subpieces VALUES(6,'Haydn_Hob.XVI34_1-5','./resources/midi/subpieces/Haydn_Hob.XVI34_1-5.mid',4,0);
INSERT INTO subpieces VALUES(7,'Haydn_Hob.XVI34_1-6','./resources/midi/subpieces/Haydn_Hob.XVI34_1-6.mid',4,0);
INSERT INTO subpieces VALUES(8,'Haydn_Hob.XVI34_1-7','./resources/midi/subpieces/Haydn_Hob.XVI34_1-7.mid',4,0);
INSERT INTO subpieces VALUES(9,'Haydn_Hob.XVI34_1-8','./resources/midi/subpieces/Haydn_Hob.XVI34_1-8.mid',4,0);
INSERT INTO subpieces VALUES(10,'Haydn_Hob.XVI34_1-9','./resources/midi/subpieces/Haydn_Hob.XVI34_1-9.mid',4,0);
INSERT INTO subpieces VALUES(11,'Haydn_Hob.XVI34_1-10','./resources/midi/subpieces/Haydn_Hob.XVI34_1-10.mid',4,0);
INSERT INTO subpieces VALUES(12,'Haydn_Hob.XVI34_1-11','./resources/midi/subpieces/Haydn_Hob.XVI34_1-11.mid',4,0);
INSERT INTO subpieces VALUES(13,'Haydn_Hob.XVI34_1-12','./resources/midi/subpieces/Haydn_Hob.XVI34_1-12.mid',4,0);
INSERT INTO subpieces VALUES(14,'Haydn_Hob.XVI34_1-13','./resources/midi/subpieces/Haydn_Hob.XVI34_1-13.mid',4,0);
INSERT INTO subpieces VALUES(15,'Haydn_Hob.XVI34_1-14','./resources/midi/subpieces/Haydn_Hob.XVI34_1-14.mid',4,0);
INSERT INTO subpieces VALUES(16,'Haydn_Hob.XVI34_1-15','./resources/midi/subpieces/Haydn_Hob.XVI34_1-15.mid',4,0);
INSERT INTO subpieces VALUES(17,'Haydn_Hob.XVI34_1-16','./resources/midi/subpieces/Haydn_Hob.XVI34_1-16.mid',4,0);
INSERT INTO subpieces VALUES(18,'Haydn_Hob.XVI34_1-17','./resources/midi/subpieces/Haydn_Hob.XVI34_1-17.mid',4,0);
INSERT INTO subpieces VALUES(19,'Haydn_Hob.XVI34_1-18','./resources/midi/subpieces/Haydn_Hob.XVI34_1-18.mid',4,0);
INSERT INTO subpieces VALUES(20,'Haydn_Hob.XVI34_1-19','./resources/midi/subpieces/Haydn_Hob.XVI34_1-19.mid',4,0);
INSERT INTO schedules VALUES(1,0,9,'Pianist',3,NULL);
INSERT INTO schedules VALUES(2,10,18,'VirtuosoNet',3,1);
INSERT INTO schedules VALUES(3,1,8,'Pianist',4,2);
INSERT INTO schedules VALUES(4,9,29,'VirtuosoNet',4,3);
INSERT INTO schedules VALUES(5,30,35,'Pianist',4,4);
INSERT INTO schedules VALUES(6,36,53,'VirtuosoNet',4,5);
INSERT INTO schedules VALUES(7,54,74,'Pianist',4,6);
INSERT INTO schedules VALUES(8,75,80,'VirtuosoNet',4,7);
INSERT INTO schedules VALUES(9,81,90,'Pianist',4,8);
INSERT INTO schedules VALUES(10,91,95,'VirtuosoNet',4,9);
INSERT INTO schedules VALUES(11,96,123,'Pianist',4,10);
INSERT INTO schedules VALUES(12,124,139,'VirtuosoNet',4,11);
INSERT INTO schedules VALUES(13,140,145,'Pianist',4,12);
INSERT INTO schedules VALUES(14,146,153,'VirtuosoNet',4,13);
INSERT INTO schedules VALUES(15,154,177,'Pianist',4,14);
INSERT INTO schedules VALUES(16,178,190,'VirtuosoNet',4,15);
INSERT INTO schedules VALUES(17,190,221,'Pianist',4,16);
INSERT INTO schedules VALUES(18,222,227,'VirtuosoNet',4,17);
INSERT INTO schedules VALUES(19,228,235,'Pianist',4,18);
INSERT INTO schedules VALUES(20,236,240,'VirtuosoNet',4,19);
INSERT INTO schedules VALUES(21,241,254,'Pianist',4,20);
""".split()

# revision identifiers, used by Alembic.
revision = "b0d8fe0babc9"
down_revision = "a56462c1c1d3"
branch_labels = None
depends_on = None


def upgrade():
    # add initial data
    with engine.connect() as con:
        for insert in INSERT_ROWS:
            con.execute(text(insert))


def downgrade():
    pass
