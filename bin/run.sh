
LIST="../list/"
PAGE="../page/"
BIN="../bin/"
TEMP="../temp/"
CODE="../code/"
DETAIL="../detail/"
date=$(date +"%Y%m%d")

HOME_URL="http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=48&type=jcmini"
curl $HOME_URL -o $TEMP/temp.data
python2.7 home_parser.py $TEMP/temp.data $date

input_file=$LIST/$date

while IFS= read -r var
do 
	curl $var -s -o $PAGE/$date
	str=$(python2.7 $BIN/parser.py $PAGE/$date $date)
	python2.7 $CODE/NBA.py $str
	sleep 1s
done < $input_file
