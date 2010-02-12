# Uploading data from Bokhylla.no to Google App Engine

# 0. Move to the upload directory

cd /Volumes/home-2/Magnus/gae/libriotech/bokhylladb/upload

# 1. Download files from Bokhylla: 

wget http://nb.no/nbdigital/bokliste/bokhylla_02.txt
wget http://nb.no/nbdigital/bokliste/public.txt
wget http://nb.no/nbdigital/bokliste/totalt.txt 

# 2. Run preprocess.pl

perl preprocess.pl > bokhylla.csv

# 3. Upload the data: 

appcfg.py upload_data --config_file=../libriotech/bokhylladb/upload/upload.py --filename=bokhylla.csv --kind=BokhyllaItem --url=http://libriotech.appspot.com/bokhylladb/remote_api --log_file=/tmp/bokhylladbupload.log --db_filename=/tmp/bokhylladbupload.sql3 --http_limit=5 --rps_limit=10 ../libriotech/ 