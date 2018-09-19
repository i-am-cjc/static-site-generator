#!/usr/bin/python
import shutil as sh

"""Constants"""
files = {
            "head": "_templates/header.html",
            "foot": "_templates/footer.html",
            "index": "_output/index.html",
            "adv": "_output/advisories/index.html",
            "arc": "_output/posts/index.html",
            "tag": "_output/tags/index.html",
            "proj": "_output/projects/index.html"
        }

print(">> Wiping _output")
sh.rmtree("./_output")
