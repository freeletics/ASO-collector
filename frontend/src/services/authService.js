export const authenticationService = {
  login,
  logout,
  get currentBucketData() {
    return {
      bucketName: localStorage.getItem('bucketName'),
      secretAccessKey: localStorage.getItem('secretAccessKey'),
      accessKeyId: localStorage.getItem('accessKeyId'),
    };
  },
};

function login(accessKeyId, secretAccessKey, bucketName) {
  localStorage.setItem('accessKeyId', accessKeyId);
  localStorage.setItem('secretAccessKey', secretAccessKey);
  localStorage.setItem('bucketName', bucketName);
}

function logout() {
  localStorage.removeItem('bucketName');
  localStorage.removeItem('accessKeyId');
  localStorage.removeItem('secretAccessKey');
  window.location = '/login';
}
