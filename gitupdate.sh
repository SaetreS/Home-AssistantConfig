#  give executive permission:
#  sudo chmod +x gitupdate.sh
#
#  run:
#  ./gitupdate.sh

cd /home/homeassistant/.homeassistant
source /srv/homeassistant/homeassistant_venv/bin/activate
hass --script check_config -c /home/homeassistant/.homeassistant/

git add .
git status
echo -n "Enter the description for the change: " [minor update]
read CHANGE_MSG
git commit -m "${CHANGE_MSG}"
git push origin master

exit
