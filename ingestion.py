from backend.constants import DATA_PATH, VECTOR_DB_PATH
from backend.data_models import Transcript
import lancedb
from pathlib import Path
import time

def setup_db(path):
    Path(path).mkdir(exist_ok=True)
    vector_db = lancedb.connect(uri=path)
    vector_db.create_table("transcripts", schema=Transcript, exist_ok=True)

    return vector_db

def ingest_md_to_db(table):
    for file in DATA_PATH.glob("*.md"):
        with open(file, "r") as f:
            content = f.read()

        script_id = file.stem                         # final part of path without suffix

        table.delete(f"script_id = '{script_id}'")    # Delete old entry (if exists)

        table.add(
            [
                {
                    "script_id": script_id,
                    "source_name": file.name,
                    "content": content
                }
            ]
        )

        print(f"Ingested {file.name}")
        print(table.to_pandas()["script_id"])
        time.sleep(20)

if __name__ == "__main__":
    vector_db = setup_db(VECTOR_DB_PATH)
    ingest_md_to_db(vector_db["transcripts"])