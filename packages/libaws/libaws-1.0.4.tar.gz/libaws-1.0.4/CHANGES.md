Changelog
=========

Changes with latest version of libaws
----------------------------------------------

Version 1.0 -------------2016-06-04

1.use boto software to implement base amazon web service
2.enable upload muliti part files to bucket
3.enable max upload retry attemps
4.upload files enable resume from break point
5.real upload speed end progress show
6.enable download files from bucket to local
7.download files enable resume from break point
8.enable max download retry attemps
5.real download speed end progress show



Version 1.0.1 -------------2016-06-04
1.fix tiny bug of init app data path

Version 1.0.2 -------------2016-06-05
1.fix missing logger config file 
2.when download files path is not exist,create it

Version 1.0.3 -------------2016-06-06
1.enable download or upload zero files
2.enable color print log
3.enable upload daemon process
4.add switch param to enable debug log or not 

Version 1.0.4 -------------2016-06-17
1. fix get file hash memory error cause program corrupted
2. modidy and optimise program description
3. adjust upload and download some warn log level 
4. enable create instance vpc subnet route security from config file
5. develop an awskit tool to enable s3 and ec2 command collection with console commandline
6. repair download bucket child folder files bug
7. repair when bucket set policy , cause download file fail bug
8. enable set bucket policy with bucket console commandline
9. enable launch a default instance and auto connect with ssh

