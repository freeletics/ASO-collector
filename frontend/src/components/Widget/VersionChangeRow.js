import React from 'react';
import { Button } from 'reactstrap';

class VersionChangeRow extends React.Component {
  render() {
    const { changed, attributeName, currentValue, previousValue } = this.props;
    return changed ? (
      <tr>
        <td onClick={this.props.onClick}><Button className="w-100">{attributeName}</Button></td>
        <td width="42.5%">{this.props.changesVisible && previousValue}</td>
        <td width="42.5%">{this.props.changesVisible && currentValue}</td>
      </tr>
    ) : null
  }
}

export default VersionChangeRow;
