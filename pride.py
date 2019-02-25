#!/usr/bin/python
import shutil as sh
import os
import markdown
import datetime

# This is a line by line convert of the old
# shell script, optimisation to come in the 
# future(tm)

# Append data to a file
def append(f, content):
    with open(f, "a") as out:
        out.write(content)

# Take a file, compile MD, return data
def md(f):
    with open(f, 'r') as fin:
        return markdown.markdown(fin.read())

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
MAX_COUNT = 5

print(">> Wiping _output")
try:
    sh.rmtree("./_output")
except:
    pass

# Make all the directories required
# Copy static assets
print(">> Copying assets")
sh.copytree("_assets/", "_output/")
os.mkdir("_output/posts")
os.mkdir("_output/advisories")
os.mkdir("_output/tags")
os.mkdir("_output/tag")
os.mkdir("_output/projects")



# Write the header to :allthefiles:
header_content = open(files['head']).read()
footer_content = open(files['foot']).read()

append(files['index'], header_content)
append(files['arc'], header_content)
append(files['adv'], header_content)
append(files['proj'], header_content)
append(files['tag'], header_content)

append(files['index'], "</h1>")
append(files['index'], md('./_pages/about'))
append(files['arc'], ' / posts</h1>')
append(files['adv'], ' / advisories</h1>')
append(files['tag'], ' / tags</h1>')
append(files['proj'], ' / projects</h1>')

print(">> Generating PAGES")
os.mkdir("_output/page")

for page in os.listdir("_pages"):
    os.mkdir("_output/" + page)
    file = "_output/" + page + "/index.html"
    append(file, header_content)
    append(file, " / " + page + "</h1>")
    append(file, md("./_pages/" + page))
    append(file, footer_content)

count = 0

append(files['index'], "<h3>posts<small> (<a href=\"/posts\">all</a> | <a href=\"/tags\">tags</a>)</small></h3>")
print(">> Generating POSTS")
for post in reversed(os.listdir("_posts")):
    file_contents = open("_posts/" + post).read().split("\n")
    date = "-".join(post.split("-")[0:3])
    line = file_contents[0]
    title = line.replace(" ", "-")
    dir = "/".join(date.split("-")) + "/" + title
    directory = "_output"
    for d in dir.split("/"):
        directory += "/" + d
        try:
            os.mkdir(directory)
        except:
            pass

    link = "<a href=\"/" + dir + "\">" + date + "</a> " + line + "<br />" 

    if count < MAX_COUNT:
        append(files['index'], link)
    
    count += 1

    append(files['arc'], link)

    f = "_output/" + dir + "/index.html"
    append(f, header_content)
    append(f, " / <a href=\"/posts\">posts</a> / " + line + "</h1>")
    datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d')

    append(f, "<time class=\"post-date\">" + datetime_object.strftime('%b %m, %Y') + "</time>")
    content = markdown.markdown("\n".join(file_contents[3:-2]))
    append(f, content)

    append(f, "<strong>Tags: </strong>")

    # TAGS
    tags = file_contents[-2].split(":")[-1].split(",")

    for tag in tags:
        try:
            os.mkdir("_output/tag/" + tag)
        except:
            pass
        append(f, "<i><a href=\"/tag/" + tag + "\">" + tag + "</a></i> ")
        append('_output/tag/' + tag + '/body.html', link)
    
    append(f, footer_content)

print(">> Generating TAGS")
for tag in os.listdir("_output/tag"):
    tag_index = "_output/tag/" + tag + "/index.html"
    tag_body = "_output/tag/" + tag + "/body.html"
    
    append(tag_index, header_content)
    append(tag_index, " / <a href=\"/tag/" + tag + "\">tags</a> / " + tag + "</h1>")
    with open(tag_body, 'r') as tag_body_file:
        append(tag_index, tag_body_file.read())
    append(tag_index, footer_content)
    append(files["tag"], "<a href=\"/tag/" + tag + "\">" + tag + "</a><br /> ")

count = 0

append(files['index'], "<h3>advisories<small> (<a href=\"/advisories\">all</a>)</small></h3>")

print(">> Generating ADVISORIES")
for adv in reversed(os.listdir("_advisories")):
    line = open("_advisories/" + adv).readlines()[0]
    os.mkdir("_output/advisories/" + adv)
    link = "<a href=\"/advisories/" + adv + "\">" + adv + "</a> " + line + "<br />"

    append(files["adv"], link)
    if count < 5:
        append(files["index"], link)
    count += 1

    f = "_output/advisories/" + adv + "/index.html"
    append(f, header_content)
    append(f, " / <a href=\"/advisories\">advisories</a> / " + adv + "</h1>")
    
    with open("_advisories/" + adv) as file_contents:
        append(f, markdown.markdown(file_contents.read()))
    append(f, footer_content)


count = 0

append(files['index'], "<h3>projects<small> (<a href=\"/projects\">all</a>)</small></h3>")

print(">> Generating Projects")
for prj in reversed(os.listdir("_projects")):
    line = open("_projects/" + prj).readlines()[0]
    os.mkdir("_output/projects/" + prj)
    link = "<a href=\"/projects/" + prj + "\">" + prj + "</a> " + line + "<br />"

    append(files["proj"], link)
    if count < 5:
        append(files["index"], link)
    count += 1

    f = "_output/projects/" + prj + "/index.html"
    append(f, header_content)
    append(f, " / <a href=\"/projects\">projects</a> / " + prj + "</h1>")
    
    with open("_projects/" + prj) as file_contents:
        append(f, markdown.markdown(file_contents.read()))
    append(f, footer_content)

append(files["index"], footer_content)
append(files["arc"], footer_content)
append(files["proj"], footer_content)
append(files["adv"], footer_content)
append(files["tag"], footer_content)