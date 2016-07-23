HEADER=_templates/header.html
FOOTER=_templates/footer.html
PAGEHEADER=_templates/pageheader.html
PAGEFOOTER=_templates/pagefooter.html
INDEX=_output/index.html
ADV=_output/advisories/index.html
ARCHIVE=_output/archive/index.html
PREPROCESSOR=Markdown.pl
POSTCOUNT=5

echo ">> Wiping _output"
mkdir -p _output
rm -rf _output/*
mkdir -p _output/archive
mkdir -p _output/advisories

echo ">> Copying assets"
cp -r _assets/* _output

cat $HEADER > $INDEX
cat $HEADER > $ARCHIVE
cat $HEADER > $ADV

cat $PAGEHEADER >> $INDEX
cat $PAGEHEADER >> $ARCHIVE
cat $PAGEHEADER >> $ADV

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
    LINE=$(cat _posts/$POST | head -n 1)
    DIR=$(echo $LINE | awk '{ gsub(" ", "-"); print }')

    mkdir -p _output/log/$DIR

    LINK="<a href=\"/log/$DIR\">$POST - $LINE</a><br />"
    
    if [ "$count" -le "$POSTCOUNT" ] 
    then
        echo $LINK >> $INDEX
    fi
    echo $LINK >> $ARCHIVE

    count=$(($count+1))
    FILE=_output/log/$DIR/index.html
    cat $HEADER > $FILE
    cat _posts/$POST | perl $PREPROCESSOR >> $FILE
    cat $FOOTER >> $FILE
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
