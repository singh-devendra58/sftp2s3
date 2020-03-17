import stat
import os
import paramiko
import boto3
import json
import socket
from stat import S_ISDIR
from datetime import datetime


def sftp_aws_connection(config):
    transport =paramiko.Transport(config["SFTP_IP"] , int(config["SFTP_PORT"]))
    transport.connect(username=config["USERNAME"], password=config["PASSWORD"])
    ftp_conn=paramilo.SFTPClient.from_transport(transport)
    s3=boto3.client('s3')
    s3=boto3.resource('s3',aws_access_key_id=config["AWS_ACCESS_KEY_ID"], aws_secret_access_key=["AWS_SECRET_ACCESS_KEY"])
    bucket=s3.Bucket(config["AWS_BUCKET_NAME"])
    return (ftp_conn,bucket)

def create_dir(directory,ftp_conn):
    try:
        fpt_conn.mkdir(directory)
    except Exception as e:
        print(str(e))

def isExistOnSftp(sftp,sftpPath):
    try:
        sftp.stat(sftpPath)
        return True
    except IOError as e:
        print(str(e))
        return False

def uploadSftpFileIntoAws(filePath, sftpConn, bucket, config,pathConfig, IsArchive=False):
    try:
        sftpConn.chdir(filePath)
        files=sftpConn.listdir()
        files=set(files)-set([pathConfig["ARCHIVE"]])
        if(len(files)>0):
            for file in files:
                fullPath=os.path.join(filePath,file)
                ftpFile=sftpConn.file(fullPath,'r')
                sourceSize=ftpFile._get_size()
                if k in pathConfig['AWS_FILE_LOC']:
                    if k in filePath:
                        bucket.upload_fileobj(ftpFile,pathConfig[k]+'/'+file)
                        break
                ftpFile.close()
                if IsArchive==True:
                    if isExistOnSftp(sftpConn, pathConfig["ARCHIVE"])==False:
                        create_dir(pathConfig["ARCHIVE"],sftpConn)
                    sftpConn.rename(sftpConn.getcwd()+'/'+file, sftpConn.getcwd()+'/'+pathConfig["ARCHIVE"]+'/'+datetime.now().strftime(
                        '%Y%m%d%H%M%S%f_')+file)
    except Exception as e :
        print('Exception occurred while file moved from working dir' +str(e))




