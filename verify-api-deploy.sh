RESULT=$(curl https://api.eduace.net/api/version)

if ! [[ $RESULT =~ ^$1.* ]] ;
then 
  echo "Wrong value returned"
  echo $RESULT
  exit 999
fi
echo "Correct value returned"
exit 0
