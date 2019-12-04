import React from 'react';
import ReactDiffViewer from 'react-diff-viewer';
import { Button } from 'reactstrap';

class VersionTextRow extends React.Component {
  render() {
    const { changed, attributeName, currentValue, previousValue } = this.props;
    return changed ? (
      <tr>
        <td onClick={this.props.onClick}><Button className="w-100">{attributeName}</Button></td>
        <td colSpan={2}>
          {this.props.changesVisible && (
            <ReactDiffViewer
              oldValue={previousValue || ''}
              newValue={currentValue || ''}
              splitView={true}
              hideLineNumbers={true}
            />
          )}
        </td>
      </tr>
    ) : null;
  }
}

export default VersionTextRow;
