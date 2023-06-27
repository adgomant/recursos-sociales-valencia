# -*- coding: utf-8 -*-

import os
import sys
import time
import json
from whoosh import index, analysis, fields

def create_index(idx_dir):
    general_analyzer = analysis.LanguageAnalyzer(lang="es")
    exact_analyzer = analysis.RegexTokenizer()|analysis.LowercaseFilter()|analysis.StopFilter(lang="es")
    schema = fields.Schema(
        Id = fields.ID(stored=True, unique=True),
        name = fields.STORED,
        short_desc = fields.TEXT(stored=True, analyzer=exact_analyzer),
        address = fields.STORED,
        postcode = fields.STORED,
        phone = fields.STORED,
        mail = fields.STORED,
        website = fields.STORED,
        content = fields.TEXT(stored=True, analyzer=general_analyzer),
        theme = fields.TEXT(stored=True, analyzer=exact_analyzer)
    )
    ix = index.create_in(idx_dir, schema)
    return ix

def load_json(filename):
    with open(filename, encoding = "utf-8") as fh:
        d = json.load(fh)
    return d

def indexer(doc_dir, idx_dir):
    if not os.path.exists(idx_dir):
        os.mkdir(idx_dir)
        print("\ncreating index...\n")
        ix = create_index(idx_dir)
    else:
        print("\nopening index...\n")
        ix = index.open_dir(idx_dir)
    docs = load_json(doc_dir)
    writer = ix.writer()
    t1, ndocs = time.time(), 0
    for url, site in docs.items():
        if not site["short_description"]: continue
        phone = site["phone"]
        writer.add_document(
            Id=str(site["id"]),
            name = site["name"],
            short_desc = site["short_description"],
            address = site["address"],
            postcode = site["postcode"],
            phone = site["phone"],
            mail = site["mail"],
            website = site["website"] if site["website"] else [url],
            content = site["content"],
            theme = site["theme"]
        )
        ndocs += 1
    t2 = time.time()
    print("\n=========================")
    print(f"Docs: {ndocs}, Time: {t2-t1:.2f}s")
    print("=========================")
    print("\nwritting index...\n")
    writer.commit()
    t3 = time.time()
    print("=========================")
    print(f"Total time: {t3-t1:.2f}s")
    print("=========================")

if __name__ == "__main__":
    indexer(sys.argv[1], sys.argv[2])
