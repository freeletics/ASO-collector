import AWS from 'aws-sdk';
import * as CSV from 'csv-string';
import { authenticationService } from './authService';

function fetchData(filename, callback) {
  const {
    accessKeyId,
    secretAccessKey,
    bucketName,
  } = authenticationService.currentBucketData;
  AWS.config.update({
    accessKeyId,
    secretAccessKey,
  });
  var s3 = new AWS.S3();
  // TODO: dogadac co z max-age
  s3.getObject(
    {
      Bucket: bucketName,
      Key: filename,
      ResponseCacheControl: 'max-age: 3600',
    },
    function(error, data) {
      if (error != null) {
        alert('Failed to retrieve an object: ' + error);
      } else {
        const arr = CSV.parse(data.Body.toString('utf-8'));
        callback(arr);
      }
    },
  );
}

export default fetchData;
