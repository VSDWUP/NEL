from sqlalchemy import create_engine
from configs.DBConfig import host, user, password, db_name, named_entities_table, texts_table, text_named_entities_table
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT, BIGINT
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

engine = create_engine(f"postgresql://{user}:{password}@{host}/{db_name}")


class Base(DeclarativeBase):
    pass


class NamedEntity(Base):
    __tablename__ = named_entities_table

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    entity = Column(VARCHAR(250), nullable=False)
    tag = Column(VARCHAR(25), nullable=False)
    concept_id = Column(VARCHAR(50))
    link = Column(TEXT)


class Text(Base):
    __tablename__ = texts_table

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    title = Column(VARCHAR(250), nullable=False)
    corpus = Column(VARCHAR(250), nullable=False)


class TextEntityLink(Base):
    __tablename__ = text_named_entities_table

    text_id = Column(BIGINT, primary_key=True)
    named_entity_id = Column(BIGINT, primary_key=True)


def upsertMethodResult(entity_set, file_path):
    text_id = upsertTextEntity(file_path)
    entity_id_list = upsertNamedEntities(entity_set)
    upsertEntityTextLinks(entity_id_list, text_id)


def upsertTextEntity(file_path):
    file_info = getFileInfo(file_path)
    title = file_info[0]
    corpus = file_info[1]
    with Session(autoflush=False, bind=engine) as db:
        text_id = db.query(Text).filter(Text.title == title, Text.corpus == corpus).first()
        if text_id is None:
            db.add(Text(title=title, corpus=corpus))
            db.commit()
            text_id = db.query(Text).filter(Text.title == title, Text.corpus == corpus).first()
    db.close()
    return text_id.id


def getFileInfo(file_path):
    splitted_file_path = file_path.split("/")
    file_name = splitted_file_path[-1].split(".")[-2]
    corpus = splitted_file_path[-2]
    return [file_name, corpus]


def upsertNamedEntities(entities_info_set):
    for entity in entities_info_set:
        upsertEntity(entity=entity[0], tag=entity[1], link=entity[2], concept_id=entity[3])

    entity_id_list = []
    with Session(autoflush=False, bind=engine) as db:
        for entity in entities_info_set:
            query_result = db.query(NamedEntity).filter(NamedEntity.entity == entity[0],
                                                        NamedEntity.tag == entity[1]).first()
            if query_result is None:
                pass
            else:
                entity_id_list.append(query_result.id)
    db.close()

    return entity_id_list


def upsertEntity(entity, tag, concept_id, link):
    with Session(autoflush=False, bind=engine) as db:
        query_result = db.query(NamedEntity).filter(NamedEntity.entity == entity, NamedEntity.tag == tag, ).first()
        if query_result is None:
            newRecord = NamedEntity(entity=entity, tag=tag, concept_id=concept_id, link=link)
            db.add(newRecord)
        else:
            query_result.concept_id = concept_id
            query_result.link = link
        db.commit()
    db.close()


def upsertEntityTextLinks(entity_id_list, file_id):
    with Session(autoflush=False, bind=engine) as db:
        for entity_id in entity_id_list:
            db.add(TextEntityLink(named_entity_id=entity_id, text_id=file_id))
            try:
                db.commit()
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    db.rollback()
                    pass
                else:
                    raise e
    db.close()


def getNamedEntityFromDB(entity, tag):
    with Session(autoflush=False, bind=engine) as db:
        named_entity = db.query(NamedEntity).filter(NamedEntity.entity == entity, NamedEntity.tag == tag).first()
        if not isinstance(named_entity, NamedEntity):
            print("Not found")
        else:
            print(
                f"{named_entity.id}, {named_entity.entity}, {named_entity.tag}, {named_entity.link},"
                f" {named_entity.concept_id}")
    db.close()


def getTextFromDB(text_name, text_corpus):
    with Session(autoflush=False, bind=engine) as db:
        text = db.query(Text).filter(Text.title == text_name, Text.corpus == text_corpus).first()
        if not isinstance(text, Text):
            print("Not found")
        else:
            print(f"{text.id}, {text.title}, {text.corpus}")
    db.close()
