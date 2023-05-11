from sqlalchemy import create_engine
from configs.DBConfig import host, user, password, db_name, tablename
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT, BIGINT

engine = create_engine(f"postgresql://{user}:{password}@{host}/{db_name}")


class Base(DeclarativeBase):
    pass


class NamedEntity(Base):
    __tablename__ = tablename

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    entity = Column(VARCHAR(250), nullable=False)
    tag = Column(VARCHAR(25), nullable=False)
    text_name = Column(VARCHAR(250))
    link = Column(TEXT)
    concept_id = Column(VARCHAR(50))


def insertEntities(entity_list, file_path):
    for entity_info_list in entity_list:
        insertEntity(entity_info_list[0], entity_info_list[1],getFileNameFromPath(file_path),
                     entity_info_list[2], entity_info_list[3])


def insertEntity(entity, tag, text_name, concept_id, link):
    with Session(autoflush=False, bind=engine) as db:
        search_result = db.query(NamedEntity).filter(NamedEntity.entity == entity, NamedEntity.tag == tag,
                                                     NamedEntity.text_name == text_name).first()
        if search_result is None:
            newRecord = NamedEntity(entity=entity, tag=tag, text_name=text_name, concept_id=concept_id, link=link)
            db.add(newRecord)
        else:
            search_result.concept_id = concept_id
            search_result.link = link
        db.commit()


def getFileNameFromPath(file_path):
    return file_path.split("/")[-1]


def getEntityFromDB(entity, tag, text_name):
    with Session(autoflush=False, bind=engine) as db:
        entity_object = db.query(NamedEntity).filter(NamedEntity.entity == entity, NamedEntity.tag == tag,
                                                     NamedEntity.text_name == text_name).first()
        return entity_object


def getNamedEntity(entity, tag, text_name):
    db_record = getEntityFromDB(entity, tag, text_name)
    if not isinstance(db_record, NamedEntity):
        print("Not found")
    else:
        print(
            f"{db_record.id}, {db_record.entity}, {db_record.tag}, {db_record.text_name}, "
            f"{db_record.link}, {db_record.concept_id}")


