export const authenticationService = {
  login,
  logout,
  get currentBucketData() {
    return {
      bucketName: localStorage.getItem('bucketName'),
      secretAccessKey: localStorage.getItem('secretAccessKey'),
      accessKeyId: localStorage.getItem('accessKeyId'),
      region: localStorage.getItem('region'),
    };
  },
};

function login(accessKeyId, secretAccessKey, bucketName, region) {
  localStorage.setItem('accessKeyId', accessKeyId);
  localStorage.setItem('secretAccessKey', secretAccessKey);
  localStorage.setItem('bucketName', bucketName);
  localStorage.setItem('region', region);
}

function logout() {
  localStorage.removeItem('region');
  localStorage.removeItem('bucketName');
  localStorage.removeItem('accessKeyId');
  localStorage.removeItem('secretAccessKey');
  window.location = '/login';
}
