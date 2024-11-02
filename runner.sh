#!/bin/bash
#assume pwd is final . ie you are inside final flask
#activate vurtual environment 
source finalflask/bin/activate

#run server
cd server || { echo "Server directory not found!"; exit 1; }
echo "Running dataserver.py..."
python dataserver.py &  
echo "Running imgServer.py..."
python imgServer.py 

#react app start
cd ../front/client || { echo "Client directory not found!"; exit 1; }
echo "Starting the React client..."

npm start
