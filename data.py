from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbconfig import Server,Base

engine = create_engine('sqlite:///guide.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

proj1 = Server(project = "Debit Host",description = "Host All debit cards and its transactions (card and Mobile),batch node database 'debitCardIssuance'(10.10.5.106)",app_prod_ip = "10.10.100.56",app_stage_ip="10.10.16.8",db_prod_ip = "10.10.5.109,56445",db_stage_ip="10.10.16.72,51573")
session.add(proj1)
session.commit()

proj2 = Server(project = "Credit Host",description = "Host All Credit cards and its transactions ,batch node database 'CreditCardIssuance'(10.10.5.106)",app_prod_ip = "10.10.100.81",app_stage_ip="10.10.16.8",db_prod_ip = "10.10.5.109,56445",db_stage_ip="10.10.16.72,51573")
session.add(proj2)
session.commit()

proj3 = Server(project = "CpesCMS",description = "Host and managing All gov and prepaid cards .Gov,prepaid and mobile transactions are exisit on database 'TransactionOlap'(10.10.5.106)",app_prod_ip = "10.10.100.83",app_stage_ip="10.10.16.8",db_prod_ip = "10.10.5.106",db_stage_ip="10.10.16.169")
session.add(proj3)
session.commit()

proj4 = Server(project = "MobileInterbankSwitch 'Tahweel'",description = "it is a Switch between MasterCard Schemes and Non MasterCard schemes",app_prod_ip = "10.10.100.216",app_stage_ip="10.10.16.116",db_prod_ip = "10.10.5.109,56445",db_stage_ip="10.10.16.72,51573")
session.add(proj4)
session.commit()

proj5 = Server(project = "NPS 'Meeza'",description = "National Payment scheme (Meeza)",app_prod_ip = "10.10.100.35",app_stage_ip="10.10.16.35",db_prod_ip = "10.10.5.106",db_stage_ip="10.10.16.169")
session.add(proj5)
session.commit()

proj6 = Server(project = "UPG",description = "Unified payment gateway to route the POS transactions locally ",app_prod_ip = "10.10.50.10",app_stage_ip="10.10.47.10",db_prod_ip = "10.10.5.105",db_stage_ip="10.10.16.190,5321")
session.add(proj6)
session.commit()
