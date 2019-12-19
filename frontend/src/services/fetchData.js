import AWS from 'aws-sdk';
import { authenticationService } from './authService';

function fetchData(filename, callback) {
  const {
    accessKeyId,
    secretAccessKey,
    bucketName,
    region,
  } = authenticationService.currentBucketData;
  AWS.config.update({
    accessKeyId,
    secretAccessKey,
    region,
  });
  var s3 = new AWS.S3();
  s3.getObject(
    {
      Bucket: bucketName,
      Key: filename,
      ResponseCacheControl: 'max-age: 3600',
    },
    function(error, data) {
      if (error != null) {
        console.log('Failed to retrieve an object: ' + error);
        callback('')
      } else {
        callback(data.Body.toString('utf-8'));
      }
    },
  );
}

export default fetchData;
