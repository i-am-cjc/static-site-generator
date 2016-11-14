HEADER=_templates/header.html
FOOTER=_templates/footer.html
PAGEHEADER=_templates/pageheader.html
PAGEFOOTER=_templates/pagefooter.html
INDEX=_output/index.html
ADV=_output/advisories/index.html
ARCHIVE=_output/archive/index.html
TAGINDEX=_output/tag/index.html
PREPROCESSOR=Markdown.pl
POSTCOUNT=5

echo ">> Wiping _output"
mkdir -p _output
rm -rf _output/*
mkdir -p _output/archive
mkdir -p _output/advisories
mkdir -p _output/tags
mkdir -p _output/tag

echo ">> Copying assets"
cp -r _assets/* _output

cat $HEADER > $INDEX
cat $HEADER > $ARCHIVE
cat $HEADER > $ADV
cat $HEADER > $TAGINDEX

cat $PAGEHEADER >> $INDEX
cat $PAGEHEADER >> $ARCHIVE
cat $PAGEHEADER >> $ADV
cat $PAGEHEADER >> $TAGINDEX

echo ">> Generating PAGES"
mkdir -p _output/page

for PAGE in $(ls _pages/); do 
    mkdir -p _output/$PAGE
    FILE=_output/$PAGE/index.html
    cat $HEADER > $FILE
    cat _pages/$PAGE | perl $PREPROCESSOR >> $FILE
    cat $FOOTER >> $FILE
done

cat $PAGEFOOTER >> $INDEX
cat $PAGEFOOTER >> $ARCHIVE
cat $PAGEFOOTER >> $ADV

count=1

echo ">> Generating POSTS"
for POST in $(ls -r _posts/); do 
    DATE=$(echo $POST | cut -d"-" -f1,2,3)
    LINE=$(cat _posts/$POST | head -n 1)
    TITLE=$(echo $LINE | awk '{ gsub(" ", "-"); print }')
    DIR=$(echo $DATE | awk -F - '{print $1"/"$2"/"$3}')/$TITLE
    mkdir -p _output/$DIR

    LINK="<a href=\"/$DIR\">$DATE - $LINE</a><br />"
    
    if [ "$count" -le "$POSTCOUNT" ] 
    then
        echo $LINK >> $INDEX
    fi
    echo $LINK >> $ARCHIVE

    count=$(($count+1))

    FILE=_output/$DIR/index.html
    cat $HEADER > $FILE
    cat _posts/$POST | grep -v "TAGS" | perl $PREPROCESSOR >> $FILE
    cat $FOOTER >> $FILE

    # TAGS
    for TAG in $(cat _posts/$POST | grep "TAGS" | cut -d":" -f2| tr "," "\n"); do
        mkdir -p _output/tags/$TAG
        echo $LINK >> _output/tags/$TAG/body.html 
    done
done

echo ">> Generating TAGS"
for TAG in $(ls _output/tags/); do
    TINDEX=_output/tags/$TAG/index.html
    BODY=_output/tags/$TAG/body.html
    cat $HEADER > $TINDEX
    cat $BODY >> $TINDEX
    cat $FOOTER >> $TINDEX
    rm $BODY
    LINK="<a href=\"/tags/$TAG\">$TAG</a><br />"
    echo $LINK >> $TAGINDEX
done
count=1
echo "<br />" >> $INDEX

echo ">> Generating ADVISORIES"
for A in $(ls -r _advisories/); do 
    LINE=$(cat _advisories/$A | head -n 1)

    mkdir -p _output/advisories/$A

    LINK="<a href=\"/advisories/$A\">$A - $LINE</a><br />"
    
    if [ "$count" -le "$POSTCOUNT" ] 
    then
        echo $LINK >> $INDEX
    fi
    echo $LINK >> $ADV

    count=$(($count+1))
    FILE=_output/advisories/$A/index.html
    cat $HEADER > $FILE
    cat _advisories/$A | perl $PREPROCESSOR >> $FILE
    cat $FOOTER >> $FILE
done

cat $FOOTER >> $INDEX
cat $FOOTER >> $ARCHIVE
cat $FOOTER >> $ADV
cat $FOOTER >> $TAGINDEX
