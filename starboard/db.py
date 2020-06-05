from dataclasses import dataclass
from typing import Iterable, Optional
from sqlite3 import Connection


STARRED_PROJECTS_TABLE = "starred_projects"


def initialise_db(db: Connection):
  c = db.cursor()
  c.execute(f"""
    CREATE TABLE {STARRED_PROJECTS_TABLE} (
      proj_id integer primary key autoincrement,
      url text not null,
      title text not null,
      description text not null,
      note text,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  """.strip())

  c.close()


@dataclass
class StarredProject:
  proj_id: int
  url: str
  title: str
  description: str
  note: Optional[str]
  timestamp: str


def list_starred_projects(db: Connection) -> Iterable[StarredProject]:
  c = db.cursor()
  for row in c.execute(f"SELECT * FROM {STARRED_PROJECTS_TABLE} ORDER BY timestamp DESC"):
    yield StarredProject(*row)

  c.close()


def get_existing_project(db: Connection, url):
  c = db.cursor()
  for row in c.execute(f"SELECT * FROM {STARRED_PROJECTS_TABLE} WHERE url = ?", (url,)):
    c.close()
    return StarredProject(*row)

  c.close()
  return None


def add_project(db: Connection, project: StarredProject):
  c = db.cursor()

  existing_project = get_existing_project(db, project.url)
  if get_existing_project(db, project.url) is not None:
    return existing_project

  c.execute(f"INSERT INTO {STARRED_PROJECTS_TABLE}" \
    "(url, title, description, note) VALUES (?, ?, ?, ?)",
    (project.url, project.title, project.description, project.note)
  )
  db.commit()

  return get_existing_project(db, project.url)
