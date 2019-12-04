import React from 'react';
import { Card, CardBody, Row, Col } from 'reactstrap';
import VersionWidget from '../Widget/VersionWidget';
import BoxHeader from '../Widget/BoxHeader';
import withFiltersTimeline from '../Filters/withFiltersTimeline';

class ChangesTimeline extends React.Component {
  render() {
    const { data } = this.props;
    return (
      <Row>
        <Col>
          <Card>
            <CardBody>
              <BoxHeader>Changes Timeline</BoxHeader>
              {this.props.params.selectedCountries.length === 1
                ? data('dataIos').map(([date, data]) => (
                    <VersionWidget key={date} date={date} {...data} country={this.props.country} />
                  ))
                : 'Visible only when one country selected'}
            </CardBody>
          </Card>
        </Col>
      </Row>
    );
  }
}

export default withFiltersTimeline(
  ChangesTimeline,
  ['sensortower_app_update_timeline_ios', 'dataIos'],
  ['sensortower_app_update_timeline_android', 'dataAndroid'],
);
