import React from 'react';
import { CardImg, Button, Table } from 'reactstrap';
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
      releaseDate,
      title,
      country,
      subtitle,
      video,
      videoImg,
      screenshots,
      promoBanner,
      shortDescription,
      description,
      platform,
      titlePrevious,
      subtitlePrevious,
      videoPrevious,
      videoImgPrevious,
      screenshotsPrevious,
      promoBannerPrevious,
      shortDescriptionPrevious,
      descriptionPrevious,
    } = this.props;
    const videoUrlProps =
      platform === 'android' ? { target: '_blank' } : { download: true };
    const openChangesProps = {
      onClick: this.onClick,
      changesVisible: this.state.changesVisible,
    };
    return (
      <div className="p-4">
        <BoxHeader className="align-left margin-left-10">
          {releaseDate}{' '}
          <div className="upper-case">
            {country} {platform}
          </div>
        </BoxHeader>
        <Table className="align-top">
          <thead>
              { this.state.changesVisible ? (
            <tr>
              <th>Changes </th>
              <th>Previous version</th>
              <th>Current version</th>
            </tr>
              ) : <tr><th>Changes </th></tr> }
          </thead>
          <tbody className={this.state.changesVisible ? "" : "flex"}>
            <VersionTextRow
              attributeName="Title"
              changed={title || titlePrevious}
              currentValue={title}
              previousValue={titlePrevious}
              {...openChangesProps}
            />
            <VersionTextRow
              attributeName="Subtitle"
              changed={subtitle || subtitlePrevious}
              currentValue={subtitle}
              previousValue={subtitlePrevious}
            />
            <VersionChangeRow
              attributeName="Banner"
              changed={promoBanner || promoBannerPrevious}
              currentValue={<CardImg top src={promoBanner}></CardImg>}
              previousValue={<CardImg top src={promoBannerPrevious}></CardImg>}
              {...openChangesProps}
            />
            <VersionTextRow
              attributeName="Short description"
              changed={shortDescription || shortDescription}
              currentValue={shortDescription}
              previousValue={shortDescriptionPrevious}
              {...openChangesProps}
            />
            <VersionTextRow
              attributeName="Description"
              changed={description || descriptionPrevious}
              currentValue={description}
              previousValue={descriptionPrevious}
              {...openChangesProps}
            />
            <VersionChangeRow
              attributeName="Video image"
              changed={videoImg || videoImgPrevious}
              currentValue={<CardImg top src={videoImg}></CardImg>}
              previousValue={<CardImg top src={videoImgPrevious}></CardImg>}
              {...openChangesProps}
            />
            <VersionChangeRow
              attributeName="Video"
              changed={video || videoPrevious}
              currentValue={
                video && (
                  <a href={video} {...videoUrlProps}>
                    <Button size="m" className="primary border-0" block>
                      Video
                    </Button>
                  </a>
                )
              }
              previousValue={
                videoPrevious && (
                  <a href={videoPrevious} {...videoUrlProps}>
                    <Button size="m" className="primary border-0" block>
                      Video
                    </Button>
                  </a>
                )
              }
              {...openChangesProps}
            />
            <VersionChangeRow
              attributeName="Screenshots"
              changed={screenshots || screenshotsPrevious}
              currentValue={
                <div className="screenshots-preview">
                  {screenshots &&
                    screenshots.map(screenshot => (
                      <CardImg key={screenshot} top src={screenshot}></CardImg>
                    ))}
                </div>
              }
              previousValue={
                <div className="screenshots-preview">
                  {screenshotsPrevious &&
                    screenshotsPrevious.map(screenshot => (
                      <CardImg key={screenshot} top src={screenshot}></CardImg>
                    ))}
                </div>
              }
              {...openChangesProps}
            />
          </tbody>
        </Table>
      </div>
    );
  }
}

export default VersionWidget;
