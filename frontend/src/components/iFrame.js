import React from 'react';

import fetchEmbeddedUrl from '../services/fetchEmbeddedUrl';

class IFrame extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      url: '',
    };
  }

  componentDidMount() {
    fetchEmbeddedUrl(
      this.props.name,
      response =>
        typeof response === 'object' && response.url && this.setState(response),
    );
  }

  render() {
    return (
      <iframe
        title={this.props.name}
        height="100%"
        src={this.state.url}
        frameBorder="0"
        allowFullScreen
      ></iframe>
    );
  }
}

export default IFrame;
