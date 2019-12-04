import PropTypes from 'prop-types';
import React from 'react';
import { createBrowserHistory } from 'history';
import { Button, Form, FormGroup, Input } from 'reactstrap';
import { authenticationService } from '../services/authService';

class AuthForm extends React.Component {
  state = {
    history: createBrowserHistory(),
    accessKeyId: '',
    secretAccessKey: '',
    bucketName: '',
    error: false,
  };

  constructor(props) {
    super(props);
    if (authenticationService.currentBucketData) {
      this.props.onChangeAuthState(STATE_LOGIN);
    }
  }
  get isLogin() {
    return this.props.authState === STATE_LOGIN;
  }

  changeAuthState = authState => event => {
    event.preventDefault();
    this.props.onChangeAuthState(authState);
  };

  handleSubmit = event => {
    authenticationService.login(
      this.state.accessKeyId,
      this.state.secretAccessKey,
      this.state.bucketName,
    );
    const { state } = this.state.history.location;
    if (state) {
      window.location = state.from.pathname + state.from.search;
    } else {
      window.location = '/';
    }
    event.preventDefault();
  };

  render() {
    return (
      <Form onSubmit={this.handleSubmit}>
        <FormGroup>
          <Input
            {...this.props.bucketName}
            value={this.state.bucketName}
            onChange={e => this.setState({ bucketName: e.target.value })}
          />
        </FormGroup>
        <FormGroup>
          <Input
            {...this.props.accessKeyId}
            value={this.state.accessKeyId}
            onChange={e => this.setState({ accessKeyId: e.target.value })}
          />
        </FormGroup>
        <FormGroup>
          <Input
            {...this.props.secretAccessKey}
            value={this.state.secretAccessKey}
            onChange={e => this.setState({ secretAccessKey: e.target.value })}
          />
        </FormGroup>
        <hr />
        <Button
          size="lg"
          className="primary border-0"
          block
          onClick={this.handleSubmit}
        >
          Login
        </Button>
      </Form>
    );
  }
}

export const STATE_LOGIN = 'LOGIN';
export const STATE_SIGNUP = 'SIGNUP';

AuthForm.propTypes = {
  authState: PropTypes.oneOf([STATE_LOGIN, STATE_SIGNUP]).isRequired,
  showLogo: PropTypes.bool,
  usernameLabel: PropTypes.string,
  usernameInputProps: PropTypes.object,
  passwordLabel: PropTypes.string,
  passwordInputProps: PropTypes.object,
  confirmPasswordLabel: PropTypes.string,
  confirmPasswordInputProps: PropTypes.object,
  onLogoClick: PropTypes.func,
};

AuthForm.defaultProps = {
  authState: 'LOGIN',
  accessKeyId: {
    type: 'text',
    placeholder: 'Access Key Id',
  },
  secretAccessKey: {
    type: 'text',
    placeholder: 'Secret Access Key',
  },
  bucketName: {
    type: 'text',
    placeholder: 'Bucket Name',
  },
};

export default AuthForm;
