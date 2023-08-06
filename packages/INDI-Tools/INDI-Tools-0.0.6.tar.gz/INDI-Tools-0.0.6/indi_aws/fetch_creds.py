# indi_aws/fetch_creds.py
#

'''
This module contains functions which return sensitive information from 
a csv file, with regards to connection to AWS services.
'''

# Function to return AWS secure environment variables
def return_aws_keys(creds_path):
    '''
    Method to return AWS access key id and secret access key using
    credentials found in a local file.

    Parameters
    ----------
    creds_path : string (filepath)
        path to the csv file downloaded from AWS; can either be root
        or user credentials

    Returns
    -------
    aws_access_key_id : string
        string of the AWS access key ID
    aws_secret_access_key : string
        string of the AWS secret access key
    '''

    # Init variables
    with open(creds_path, 'r') as creds_in:
        # Grab csv rows
        row1 = creds_in.readline()
        row2 = creds_in.readline()

    # Are they root or user keys
    if 'User Name' in row1:
        # And split out for keys
        aws_access_key_id = row2.split(',')[1]
        aws_secret_access_key = row2.split(',')[2]
    elif 'AWSAccessKeyId' in row1:
        # And split out for keys
        aws_access_key_id = row1.split('=')[1]
        aws_secret_access_key = row2.split('=')[1]
    else:
        err_msg = 'Credentials file not recognized, check file is correct'
        raise Exception(err_msg)

    # Strip any carriage return/line feeds
    aws_access_key_id = aws_access_key_id.replace('\r', '').replace('\n', '')
    aws_secret_access_key = aws_secret_access_key.replace('\r', '').replace('\n', '')

    # Return keys
    return aws_access_key_id, aws_secret_access_key


# Function to return an AWS S3 bucket
def return_bucket(creds_path, bucket_name):
    '''
    Method to a return a bucket object which can be used to interact
    with an AWS S3 bucket using credentials found in a local file.

    Parameters
    ----------
    creds_path : string (filepath)
        path to the csv file with 'Access Key Id' as the header and the
        corresponding ASCII text for the key underneath; same with the
        'Secret Access Key' string and ASCII text
    bucket_name : string
        string corresponding to the name of the bucket on S3

    Returns
    -------
    bucket : boto.s3.bucket.Bucket
        a boto s3 Bucket object which is used to interact with files
        in an S3 bucket on AWS
    '''

    # Import packages
    try:
        import boto3
        import botocore
    except ImportError as exc:
        err_msg = 'Boto3 package is not installed - install boto3 and '\
                  'try again.'
        raise Exception(err_msg)

    # Try and get AWS credentials if a creds_path is specified
    if creds_path:
        try:
            aws_access_key_id, aws_secret_access_key = \
                return_aws_keys(creds_path)
        except Exception as exc:
            err_msg = 'There was a problem extracting the AWS credentials '\
                      'from the credentials file provided: %s. Error:\n%s'\
                      % (creds_path, exc)
            raise Exception(err_msg)
        # Init connection
        print 'Connecting to S3 bucket: %s with credentials from %s ...'\
              % (bucket_name, creds_path)
        # Better when being used in multi-threading, see:
        # http://boto3.readthedocs.org/en/latest/guide/resources.html#multithreading
        session = boto3.session.Session(aws_access_key_id=aws_access_key_id,
                                        aws_secret_access_key=aws_secret_access_key)
        s3_resource = session.resource('s3', use_ssl=True)

    # Otherwise, connect anonymously
    else:
        print 'Connecting to AWS: %s anonymously...' % bucket_name
        session = boto3.session.Session()
        s3_resource = session.resource('s3', use_ssl=True)
        s3_resource.meta.client.meta.events.register('choose-signer.s3.*',
                                                     botocore.handlers.disable_signing)

    # Explicitly declare a secure SSL connection for bucket object
    bucket = s3_resource.Bucket(bucket_name)

    # And try fetch the bucket with the name argument
    try:
        s3_resource.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as exc:
        error_code = int(exc.response['Error']['Code'])
        if error_code == 403:
            err_msg = 'Access to bucket: %s is denied; check credentials'\
                      % bucket_name
            raise Exception(err_msg)
        elif error_code == 404:
            err_msg = 'Bucket: %s does not exist; check spelling and try '\
                      'again' % bucket_name
            raise Exception(err_msg)
        else:
            err_msg = 'Unable to connect to bucket: %s. Error message:\n%s'\
                      % (bucket_name, exc)
    except Exception as exc:
        err_msg = 'Unable to connect to bucket: %s. Error message:\n%s'\
                  % (bucket_name, exc)
        raise Exception(err_msg)

    # Return the bucket
    return bucket

