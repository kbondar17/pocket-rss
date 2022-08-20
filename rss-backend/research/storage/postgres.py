import json
from typing import Any, Dict

from sqlalchemy import desc, inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import func

from weedly.db.session import db_session
from weedly.db.repos.storage import Storage


class PostgreStorage(Storage):
    def __init__(self, table):
        self.db_session = db_session
        self.table = table
        self.table_name = table.__tablename__
        self.table_headers = table.__table__.columns.keys()

    def add(self, payload: Dict[str, Any]) -> None:
        """Adding a payload data to a table in a database and checking if the data row is good enough for the operation """
        wrong_keys = [key for key in payload if key not in self.table_headers]
        if wrong_keys:
            print(f"Please check provided article, you have wrong keys: {', '.join(wrong_keys)}")
            return None
        elif (payload["author"] and payload["title"] and payload["url"] and payload["source_name"])\
                and not self._url_in_table(payload["url"]):
            try:
                self._bulk_db_data_load(self.table, [payload])
            except:
                print(f"(!) We were not able to insert the article for some reason.")
        else:
            print(f"We were not able to insert the article:")
            print(f"""{payload["author"]}, {payload["title"]}, {payload["url"]}, {payload["source_name"]}, {self._url_in_table(payload["url"])}""")

    def _url_in_table(self, url) -> bool:
        """Checking if url is in url attribute of a table. Maybe we can merge _url_in_table and _id_in_table"""
        try:
            self.db_session.query(self.table).filter(self.table.url == url).one()
            return True
        except NoResultFound:
            return False

    def _id_in_table(self, index) -> bool:
        """Checking if index exists in a table, aux for multiple functions that use index value"""
        try:
            self.db_session.query(self.table).filter(self.table.id == index).one()
            return True
        except NoResultFound:
            return False

    def _bulk_db_data_load(self, table_object, data_to_load) -> None:
        """Inserting data to a table, can be used both for bulk and one insert in other functions"""
        self.db_session.bulk_insert_mappings(table_object, data_to_load)
        self.db_session.commit()

    def delete(self, index) -> bool:
        """Deleting a row from a table by index"""
        if self._id_in_table(index):
            self.db_session.query(self.table).filter(self.table.id == index).delete()
            db_session.commit()
            return True
        return False

    def get_one(self, index):
        """Obtaining a row from a table by index if the index exists"""
        if self._id_in_table(index):
            return self.db_session.query(self.table).filter(self.table.id == index).one()
        return False

    def get_all(self, num_rows):
        """Getting first :num_rows: of elements sorted by date. Newest first"""
        return self.db_session.query(self.table).order_by(desc(self.table.published)).limit(num_rows)

    @property
    def get_last_id(self) -> int:
        """Getting the max id from a table, returning an integer"""
        return self.db_session.query(func.max(self.table.id)).scalar()

    def get_latest_by_id(self, num_rows=5):
        """Obtaining :num_rows: of elements by max id value from a table"""
        return self.db_session.query(self.table).order_by(desc(self.table.id)).limit(num_rows)

    def update(self, index, payload) -> bool:
        """Updating a row by index with a payload"""
        if self._id_in_table(index):
            wrong_keys = [key for key in payload if key not in self.table_headers]
            if wrong_keys:
                print(f"Please check provided article, you have wrong keys: {', '.join(wrong_keys)}")
                return False
            elif (payload["author"] and payload["title"] and payload["url"] and payload["source_name"]) \
                    and not self._url_in_table(payload["url"]):
                try:
                    self.db_session.query(self.table).filter(self.table.id == index).update(payload)
                    self.db_session.commit()
                    return True
                except:
                    print(f"(!) We were not able to update the article for some reason.")
        return False

    def _row_as_dict(self, query_row):
        return {column.key: str(getattr(query_row, column.key))
                for column in inspect(query_row).mapper.column_attrs}

    def query_as_json(self, query_result):
        try:
            return json.dumps(self._row_as_dict(query_result))
        except (AttributeError, TypeError):
            final_list = []
            for q in query_result:
                final_list.append(self._row_as_dict(q))
            return json.dumps(final_list)
