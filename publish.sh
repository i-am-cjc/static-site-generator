./pride
echo ">> Built, publishing in 5"
sleep 5
mv _output/* ../i-am-cjc.github.io
cd ../i-am-cjc.gitub.io
git add * 
git commit -m "New post"
git push
