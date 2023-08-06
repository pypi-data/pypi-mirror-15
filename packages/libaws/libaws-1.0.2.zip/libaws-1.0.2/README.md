# genetalk_upload


./run_upload.sh:
upload file to bucket
useage:
  -file FILE_PATH, --file FILE_PATH [Required]
  -bucket BUCKET, --bucket BUCKET
                        dest bucket to upload [Required]
  -part PART_NUM, --part PART_NUM
                        part num of file [DEFAULT 6]
  -key KEY, --key KEY   dest bucket key 
  -ignore-bucket-file, --ignore-bucket-file
                        when file exist in bucket ,ignore it or not [DEFAULT False]
  -force-again-upload, --force-again-upload
                        need to upload again when upload is exists [DEFAULT False]


						
./run_download.sh:
download bucket file to local computer
useage:
  -bucket BUCKET, --bucket BUCKET
                        dest bucket to download file [Required]
  -key KEY, --key KEY   bucket file to download [Required]
  -path PATH, --path PATH
                        file download path to save [Default .]
  -filename FILENAME, --filename FILENAME
                        download file name [DEFAULT False]
  -force-again-download, --force-again-download
                        need to download again when download is exists[DEFAULT False]

