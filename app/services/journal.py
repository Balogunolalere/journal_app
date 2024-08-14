from app.models.journal import JournalEntryCreate, JournalEntry, JournalEntryUpdate
from app.utils.embeddings import get_embedding
from docarray import BaseDoc, DocList
from docarray.index import HnswDocumentIndex
from docarray.typing import NdArray, ID
from app.db.base import journal_base
from datetime import datetime
import numpy as np
import uuid
import json
from typing import List

class JournalDoc(BaseDoc):
    id: ID = None
    title: str
    content: str
    user_key: str
    embedding: NdArray[384]  # Assuming 384 is the dimension of your embeddings

doc_index = HnswDocumentIndex[JournalDoc](work_dir='./data/journal_index')

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def create_journal_entry(entry: JournalEntryCreate, user_key: str) -> JournalEntry:
    embedding = get_embedding(f"{entry.title} {entry.content}")
    journal_key = uuid.uuid4().hex
    new_entry = JournalEntry(
        key=journal_key,
        title=entry.title,
        content=entry.content,
        user_key=user_key,
        tags=entry.tags,
        created_at=entry.created_at or datetime.utcnow(),
        updated_at=entry.updated_at or datetime.utcnow(),
        embedding=embedding
    )
    
    # Index the new entry
    doc = JournalDoc(
        id=journal_key,
        title=new_entry.title,
        content=new_entry.content,
        user_key=new_entry.user_key,
        embedding=np.array(new_entry.embedding)
    )
    doc_index.index(DocList[JournalDoc]([doc]))

    
    # Store the entry in the database
    entry_dict = json.loads(json.dumps(new_entry.dict(), cls=DateTimeEncoder))
    journal_base.put(entry_dict)
    return new_entry

def get_journal_entry(key: str, user_key: str) -> JournalEntry:
    entry = journal_base.get(key)
    if entry and entry['user_key'] == user_key:
        return JournalEntry(**entry)
    return None

def update_journal_entry(key: str, user_key: str, update_data: JournalEntryUpdate) -> JournalEntry:
    entry = get_journal_entry(key, user_key)
    if not entry:
        return None
    
    update_dict = update_data.dict(exclude_unset=True)
    if 'title' in update_dict or 'content' in update_dict:
        update_dict['embedding'] = get_embedding(f"{update_dict.get('title', entry.title)} {update_dict.get('content', entry.content)}")
    
    update_dict['updated_at'] = datetime.utcnow()
    
    # Convert datetime objects to ISO format strings
    update_dict = json.loads(json.dumps(update_dict, cls=DateTimeEncoder))
    
    updated_entry = journal_base.update(update_dict, key)
    
    # Update the index
    doc = JournalDoc(
        title=updated_entry['title'],
        content=updated_entry['content'],
        user_key=updated_entry['user_key'],
        embedding=np.array(updated_entry['embedding'])
    )
    doc_index.index(DocList[JournalDoc]([doc]))
    
    return JournalEntry(**updated_entry)

def delete_journal_entry(key: str, user_key: str) -> bool:
    entry = get_journal_entry(key, user_key)
    if not entry:
        return False
    
    journal_base.delete(key)
    
    try:
        del doc_index[key]
    except KeyError:
        pass
    
    return True

def get_all_journal_entries(user_key: str) -> List[JournalEntry]:
    entries = journal_base.fetch({"user_key": user_key}).items
    return [JournalEntry(**entry) for entry in entries]

__all__ = ['doc_index', 'JournalDoc', 'create_journal_entry', 'get_journal_entry', 'update_journal_entry', 'delete_journal_entry', 'get_all_journal_entries']