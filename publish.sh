./pride
echo ">> Built, commiting in 5"
sleep 5
mv _output/* ../i-am-cjc.github.io
rmdir _output
git add *
git commit -m "New post"
git push
echo ">> Built, publishing in 5"
sleep 5
cd ../i-am-cjc.github.io
git add * 
git commit -m "New post"
git push
