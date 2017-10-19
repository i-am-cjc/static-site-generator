HEADER=_templates/header.html
FOOTER=_templates/footer.html
MENU=_templates/menu.html
INDEX=_output/index.html
ADV=_output/advisories/index.html
ARCHIVE=_output/posts/index.html
TAGINDEX=_output/tags/index.html
PREPROCESSOR=Markdown.pl
POSTCOUNT=15

echo ">> Wiping _output"
mkdir -p _output
rm -rf _output/*
mkdir -p _output/posts
mkdir -p _output/advisories
mkdir -p _output/tags
mkdir -p _output/tag

echo ">> Copying assets"
cp -r _assets/* _output

cat $HEADER > $INDEX
cat $HEADER > $ARCHIVE
cat $HEADER > $ADV
cat $HEADER > $TAGINDEX

echo "</h2>" >> $INDEX
cat $MENU >> $INDEX
echo " / posts</h2>" >> $ARCHIVE
echo " / advisories</h2>" >> $ADV
echo " / tags</h2>" >> $TAGINDEX

echo ">> Generating PAGES"
mkdir -p _output/page

for PAGE in $(ls _pages/); do 
    mkdir -p _output/$PAGE
    FILE=_output/$PAGE/index.html
    cat $HEADER > $FILE
    echo " / $PAGE </h2>" >> $FILE
    cat _pages/$PAGE | perl $PREPROCESSOR >> $FILE
    cat $FOOTER >> $FILE
done

count=1

echo ">> Generating POSTS"
for POST in $(ls -r _posts/); do 
    DATE=$(echo $POST | cut -d"-" -f1,2,3)
    LINE=$(cat _posts/$POST | head -n 1)
    TITLE=$(echo $LINE | awk '{ gsub(" ", "-"); print }')
    DIR=$(echo $DATE | awk -F - '{print $1"/"$2"/"$3}')/$TITLE
    mkdir -p _output/$DIR

    LINK="<a href=\"/$DIR\">$DATE</a> $LINE<br />"
    
    if [ "$count" -le "$POSTCOUNT" ] 
    then
        echo $LINK >> $INDEX
    fi
    echo $LINK >> $ARCHIVE

    count=$(($count+1))

    FILE=_output/$DIR/index.html
    cat $HEADER > $FILE
    echo " / <a href=\"/posts\">posts</a> / $LINE</h2>" >> $FILE
    if [ -f _assets/$POST.jpg ]; then
        echo "<img class=\"feature\" src=\"/$POST.jpg\" />" >> $FILE
        tail -n +4 _posts/$POST | grep -v "TAGS" | perl $PREPROCESSOR >> $FILE
    else
        tail -n +4 _posts/$POST | grep -v "TAGS" | perl $PREPROCESSOR >> $FILE
    fi

    echo "<strong>Tags: </strong>" >> $FILE
    # TAGS
    for TAG in $(cat _posts/$POST | grep "TAGS" | cut -d":" -f2| tr "," "\n"); do
        mkdir -p _output/tag/$TAG
        echo $LINK >> _output/tag/$TAG/body.html 
        TAGLINK="<i><a href=\"/tag/$TAG\">$TAG</a></i> "
        echo $TAGLINK >> $FILE
    done
    cat $FOOTER >> $FILE
done

echo ">> Generating TAGS"
for TAG in $(ls _output/tag/); do
    TINDEX=_output/tag/$TAG/index.html
    BODY=_output/tag/$TAG/body.html
    cat $HEADER > $TINDEX
    echo " / <a href=\"/tags\">tags</a> / $TAG</h2>" >> $TINDEX
    cat $BODY >> $TINDEX
    cat $FOOTER >> $TINDEX
    rm $BODY
    LINK="<a href=\"/tag/$TAG\">$TAG</a><br />"
    echo $LINK >> $TAGINDEX
done
count=1
echo "<br />" >> $INDEX

echo ">> Generating ADVISORIES"
for A in $(ls -r _advisories/); do 
    LINE=$(cat _advisories/$A | head -n 1)

    mkdir -p _output/advisories/$A

    LINK="<a href=\"/advisories/$A\">$A</a> $LINE<br />"
    
    echo $LINK >> $ADV

    count=$(($count+1))
    FILE=_output/advisories/$A/index.html
    cat $HEADER > $FILE
    echo " / <a href=\"/advisories\">advisories</a> / $A</h2>" >> $FILE
    cat _advisories/$A | perl $PREPROCESSOR >> $FILE
    cat $FOOTER >> $FILE
done

cat $FOOTER >> $INDEX
cat $FOOTER >> $ARCHIVE
cat $FOOTER >> $ADV
cat $FOOTER >> $TAGINDEX
