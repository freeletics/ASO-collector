import React from 'react';
import moment from 'moment';
import { CardImg, Table } from 'reactstrap';
import VersionChangeRow from './VersionChangeRow';
import VersionTextRow from './VersionTextRow';
import BoxHeader from '../Widget/BoxHeader';

class VersionWidget extends React.Component {
  state = {
    changesVisible: false,
  };

  onClick = () => {
    this.setState({ changesVisible: !this.state.changesVisible });
  };

  getCarouselItems = images => {
    return images.map(image => {
      return {
        src: image,
      };
    });
  };

  render() {
    const {
      date,
      description,
      icon,
      imessage_screenshot,
      name,
      promo_text,
      screenshot,
      subtitle,
      version,
    } = this.props;
    const openChangesProps = {
      onClick: this.onClick,
      changesVisible: this.state.changesVisible,
    };
    return name ||
      description ||
      subtitle ||
      screenshot ||
      icon ||
      imessage_screenshot ||
      promo_text ||
      imessage_screenshot ? (
      <div className="p-4">
        <BoxHeader className="align-left margin-left-10">
          {moment.utc(date).format('YYYY-MM-DD')}
          {version && `, version: ${version.after}`}
        </BoxHeader>
        <Table className="align-top">
          <thead>
            {this.state.changesVisible ? (
              <tr>
                <th>Changes </th>
                <th>Previous version</th>
                <th>Current version</th>
              </tr>
            ) : (
              <tr>
                <th>Changes </th>
              </tr>
            )}
          </thead>
          <tbody className={this.state.changesVisible ? '' : 'flex'}>
            <VersionTextRow
              attributeName="Title"
              changed={name}
              currentValue={name && name.after}
              previousValue={name && name.before}
              {...openChangesProps}
            />
            <VersionTextRow
              attributeName="Subtitle"
              changed={subtitle}
              currentValue={subtitle && subtitle.after}
              previousValue={subtitle && subtitle.before}
              {...openChangesProps}
            />
            <VersionTextRow
              attributeName="Subtitle"
              changed={promo_text}
              currentValue={promo_text && promo_text.after}
              previousValue={promo_text && promo_text.before}
              {...openChangesProps}
            />
            <VersionChangeRow
              attributeName="Icon"
              changed={icon}
              currentValue={<CardImg top src={icon && icon.after.url}></CardImg>}
              previousValue={<CardImg top src={icon && icon.before.url}></CardImg>}
              {...openChangesProps}
            />
            <VersionTextRow
              attributeName="Description"
              changed={description}
              currentValue={description && description.after}
              previousValue={description && description.before}
              {...openChangesProps}
            />
            <VersionChangeRow
              attributeName="Screenshots"
              changed={screenshot}
              currentValue={
                <div className="screenshots-preview">
                  {screenshot && screenshot.phone &&
                    screenshot.phone.after.map(screenshot => (
                      <CardImg key={screenshot.img} top src={screenshot.img}></CardImg>
                    ))}
                </div>
              }
              previousValue={
                <div className="screenshots-preview">
                  {screenshot && screenshot.phone &&
                    screenshot.phone.before.map(screenshot => (
                      <CardImg key={screenshot.img} top src={screenshot.img}></CardImg>
                    ))}
                </div>
              }
              {...openChangesProps}
            />
            <VersionChangeRow
              attributeName="Screenshots"
              changed={imessage_screenshot}
              currentValue={
                <div className="screenshots-preview">
                  {imessage_screenshot && imessage_screenshot.phone &&
                    imessage_screenshot.phone.after.map(screenshot => (
                      <CardImg key={screenshot.img} top src={screenshot.img}></CardImg>
                    ))}
                </div>
              }
              previousValue={
                <div className="screenshots-preview">
                  {imessage_screenshot && imessage_screenshot.phone &&
                    imessage_screenshot.phone.before.map(screenshot => (
                      <CardImg key={screenshot.img} top src={screenshot.img}></CardImg>
                    ))}
                </div>
              }
              {...openChangesProps}
            />
          </tbody>
        </Table>
      </div>
    ) : null;
  }
}

export default VersionWidget;
