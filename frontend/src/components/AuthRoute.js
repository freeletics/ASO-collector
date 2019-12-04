import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { authenticationService } from '../services/authService';

const AuthRoute = ({ component: Component, ...rest }) => (
  <Route
    {...rest}
    render={props => {
      const currentBucket = authenticationService.currentBucketData;
      if (!currentBucket.bucketName) {
        return (
          <Redirect
            to={{ pathname: '/login', state: { from: props.location } }}
          />
        );
      }
      return <Component {...props} />;
    }}
  />
);

export default AuthRoute;
