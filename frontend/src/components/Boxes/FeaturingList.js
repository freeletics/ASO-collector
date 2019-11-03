import React from 'react';
import { Table, CardImg, Card, CardBody, Row, Col } from 'reactstrap';
import FreeleticsIcon from '../../assets/freeletics.png';
import BoxHeader from '../Widget/BoxHeader';
import withFilters from '../Filters/withFilters';

class FeaturingList extends React.Component {
  render() {
    const { dataIos, dataAndroid } = this.props;
    return (
      <div>
        <Row>
          <Col>
            <Card>
              <CardBody>
                <BoxHeader>Featured Creatives (Android)</BoxHeader>
                <FeaturedTable
                  featuredList={dataAndroid('dataAndroid')}
                ></FeaturedTable>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col>
            <Card>
              <CardBody>
                <BoxHeader>Featured Creatives (IOS)</BoxHeader>
                <FeaturedTable
                  featuredList={dataIos('dataIos')}
                ></FeaturedTable>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col>
            <Card>
              <CardBody>
                <BoxHeader>Featured Today Tab (IOS)</BoxHeader>
                <FeaturedTabTable
                  featuredList={dataIos('dataIosToday')}
                ></FeaturedTabTable>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col>
            <Card>
              <CardBody>
                <BoxHeader>Featured Apps Tab (IOS)</BoxHeader>
                <FeaturedTabTable
                  featuredList={dataIos('dataIosApps')}
                ></FeaturedTabTable>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

const FeaturedTabTable = ({ featuredList }) => {
  return (
    <div className="featured-table">
      <Table className="align-middle ">
        <thead>
          <tr>
            <th width="100px">Creative</th>
            <th>Date</th>
            <th width="90px">Position</th>
            <th>Title</th>
            <th>App Name</th>
            <th>Country</th>
          </tr>
        </thead>
        <tbody>
          {featuredList.map((entity, index) => (
            <tr key={index}>
              <td>
                {entity.artwork ? (
                  <a target="_blank" href={entity.artwork}>
                    Go to image
                  </a>
                ) : (
                  <CardImg src={entity.app_icon}></CardImg>
                )}
              </td>
              <td>{entity.date}</td>
              <td>{entity.position}</td>
              <td>{entity.title}</td>
              <td>{entity.app_name}</td>
              <td>{entity.country}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

const FeaturedTable = ({ featuredList }) => {
  return (
    <div className="featured-table">
      <Table className="align-middle">
        <thead>
          <tr>
            <th width="100px">Creative</th>
            <th>Date</th>
            <th>Type</th>
            <th>Category</th>
            <th>Title</th>
            <th width="80px">Country</th>
            <th width="80px">Position</th>
          </tr>
        </thead>
        <tbody>
          {featuredList.map((entity, index) => (
            <tr key={index}>
              <td>
                {entity.creatives ? (
                  <a target="_blank" href={entity.creatives}>
                    Go to image
                  </a>
                ) : (
                  <CardImg src={FreeleticsIcon}></CardImg>
                )}
              </td>
              <td>{entity.date}</td>
              <td>{entity.type}</td>
              <td>{entity.category}</td>
              <td>{entity.path}</td>
              <td>{entity.country}</td>
              <td>{entity.position}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default withFilters(
  FeaturingList,
  ['sensortower_featured_creatives_android', 'dataAndroid'],
  ['sensortower_featured_creatives_ios', 'dataIos'],
  ['sensortower_featured_apps_ios', 'dataIosApps'],
  ['sensortower_featured_today_ios', 'dataIosToday'],
);
