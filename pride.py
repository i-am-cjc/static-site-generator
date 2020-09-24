#!/usr/bin/python
import shutil as sh
import os
import markdown
import datetime
import configparser
from feedgen.feed import FeedGenerator

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


config_reader = configparser.ConfigParser()
config_reader.read('config.ini')
pride_config = config_reader['pride']

config = {
    "adv": pride_config.getboolean('Advisories'), 
    "proj": pride_config.getboolean('Projects'),
    "postCount": int(pride_config['PostCount']),
    "title": pride_config['title'],
    "baseURL": pride_config['BaseURL'],
    "author": pride_config['Author'],
    "email": pride_config['Email'],
    "twitter": pride_config['Twitter']
}

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
if config["proj"]:
    os.mkdir("_output/projects")

# Write the header to :allthefiles:
header_content = open(files['head']).read().replace("{TITLE}", config["title"]).replace("{TWITUSER}", config["twitter"])
footer_content = open(files['foot']).read()

append(files['index'], header_content.replace("{OGDESC}", config['title']))
append(files['arc'], header_content.replace("{OGDESC}", config['title'] + " archive"))
append(files['adv'], header_content.replace("{OGDESC}", config['title'] + " advisories"))
if config["proj"]:
    append(files['proj'], header_content.replace("{OGDESC}", config['title'] + " projects"))
append(files['tag'], header_content.replace("{OGDESC}", config['title'] + " tags"))

append(files['index'], "</h1>")
append(files['index'], md('./_pages/about'))
append(files['arc'], ' / notes</h1>')
append(files['adv'], ' / advisories</h1>')
append(files['tag'], ' / tags</h1>')
if config["proj"]:
    append(files['proj'], ' / projects</h1>')

print(">> Generating PAGES")
os.mkdir("_output/page")

for page in os.listdir("_pages"):
    os.mkdir("_output/" + page)
    file = "_output/" + page + "/index.html"
    #p_header_content = header_content.replace("{OGURL}", config['baseURL'] + "/" + page)
    p_header_content = header_content.replace("{OGDESC}", config['title'] + " - " + page + " by " + config["author"])
    append(file, p_header_content)
    append(file, " / " + page + "</h1>")
    append(file, md("./_pages/" + page))
    append(file, footer_content)

count = 0

print(">> Generating POSTS")
fg = FeedGenerator()
fg.title(config["title"])
fg.id('https://' + config['baseURL'])
fg.author({'name':config['author'], 'email':config['email']})
fg.link( href='https://' + config['baseURL'], rel='alternate')
fg.link( href='https://' + config['baseURL'] + '/feed.xml', rel='self')
append(files['index'], "<h2>notes / <a href=\"/posts\">archive</a> </h2>")

for post in sorted(os.listdir("_posts"), reverse=True):
    file_contents = open("_posts/" + post).read().split("\n")
    date = "-".join(post.split("-")[0:3])
    line = file_contents[0]
    title = line.replace(" ", "-").replace(",", "-")
    dir = "/".join(date.split("-")) + "/" + title
    directory = "_output"
    for d in dir.split("/"):
        directory += "/" + d
        try:
            os.mkdir(directory)
        except:
            pass

    link = "<a href=\"/" + dir + "\">" + date + "</a> " + line + "<br />" 
    
    if count < config["postCount"]:
        append(files['index'], link)
        fe = fg.add_entry()
        fe.title(line)
        fe.link(href="https://" + config['baseURL'] + "/" + dir)
        fe.id("https://" + config['baseURL'] + "/" + dir)
    
    count += 1

    append(files['arc'], link)

    f = "_output/" + dir + "/index.html"
    append(f, header_content.replace("{OGDESC}", line))
    append(f, " / <a href=\"/posts\">notes</a> / " + line + "</h1>")
    datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d')

    append(f, "<time class=\"post-date\">" + datetime_object.strftime('%b %d, %Y') + "</time> | in ")
    
    
    # TAGS
    tags = file_contents[-2].split(":")[-1].split(",")

    for tag in tags:
        try:
            os.mkdir("_output/tag/" + tag)
        except:
            pass
        append(f, "<i>#<a href=\"/tag/" + tag + "\">" + tag + "</a></i> ")
        append('_output/tag/' + tag + '/body.html', link)
    
    append(f, "<hr />")
    content = markdown.markdown("\n".join(file_contents[3:-2]))
    append(f, content)

    append(f, footer_content)

print(">> Generating TAGS")
for tag in os.listdir("_output/tag"):
    tag_index = "_output/tag/" + tag + "/index.html"
    tag_body = "_output/tag/" + tag + "/body.html"
    
    append(tag_index, header_content.replace("{OGDESC}", tag))
    append(tag_index, " / <a href=\"/tags/\">tags</a> / " + tag + "</h1>")
    with open(tag_body, 'r') as tag_body_file:
        append(tag_index, tag_body_file.read())
    append(tag_index, footer_content)
    append(files["tag"], "<a href=\"/tag/" + tag + "\">" + tag + "</a><br /> ")

count = 0

if config["adv"]:
    append(files['index'], "<h2>advisories / <a href=\"/advisories\">archive</a></h2>")

print(">> Generating ADVISORIES")
for adv in sorted(os.listdir("_advisories"), reverse=True):
    line = open("_advisories/" + adv).readlines()[0]
    os.mkdir("_output/advisories/" + adv)
    link = "<a href=\"/advisories/" + adv + "\">" + adv + "</a> " + line + "<br />"

    append(files["adv"], link)
    if count < 5:
        if config["adv"]:
            append(files["index"], link)
    count += 1

    f = "_output/advisories/" + adv + "/index.html"
    append(f, header_content.replace("{OGDESC}", line))
    append(f, " / <a href=\"/advisories\">advisories</a> / " + adv + "</h1>")
    
    with open("_advisories/" + adv) as file_contents:
        append(f, markdown.markdown(file_contents.read()))
    append(f, footer_content)

count = 0

if config["proj"]:
    print(">> Generating Projects")
    append(files['index'], "<h2>projects</h2>")
    for prj in reversed(os.listdir("_projects")):
        line = open("_projects/" + prj).readlines()[0]
        os.mkdir("_output/projects/" + prj)
        link = "<a href=\"/projects/" + prj + "\">" + line + "</a><br />"
        append(files["proj"], link)
        append(files["index"], link)
        count += 1

        f = "_output/projects/" + prj + "/index.html"
        append(f, header_content.replace("{OGDESC}", line))
        append(f, " / <a href=\"/projects\">projects</a> / " + prj + "</h1>")
        
        with open("_projects/" + prj) as file_contents:
            append(f, markdown.markdown(file_contents.read()))
        append(f, footer_content)

append(files["index"], footer_content)
append(files["arc"], footer_content)
if config["proj"]:
    append(files["proj"], footer_content)
if config["adv"]:
    append(files["adv"], footer_content)
append(files["tag"], footer_content)

fg.atom_file('_output/feed.xml')
