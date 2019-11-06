import React from 'react';
import { Card, CardBody, Col, Row } from 'reactstrap';
import { Bar } from 'react-chartjs-2';
import BoxHeader from '../Widget/BoxHeader';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { defaultOptions, getChartData } from '../../services/chartService';
import { dateLabels, getSums, getCountries } from './utils';

class AdjustInstalls extends React.Component {
  render() {
    const { dataIos, dataAndroid, colSizes } = this.props;
    return (
      <div>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Installs by type (IOS)</BoxHeader>
                <Bar
                  data={getChartData(dateLabels(dataIos()), {
                    'Organic installs': getSums(
                      this.props,
                      dataIos(),
                      'organic',
                    ),
                    'Paid installs': getSums(this.props, dataIos(), 'paid'),
                  })}
                  options={defaultOptions}
                />
              </CardBody>
            </Card>
          </Col>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Installs by type (Android)</BoxHeader>
                <Bar
                  data={getChartData(dateLabels(dataAndroid()), {
                    'Organic installs': getSums(
                      this.props,
                      dataAndroid(),
                      'organic',
                    ),
                    'Paid installs': getSums(this.props, dataAndroid(), 'paid'),
                  })}
                  options={defaultOptions}
                />
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Organic installs by country (IOS)</BoxHeader>
                <CountryChart
                  component={Bar}
                  data={{
                    labels: dateLabels(dataIos()),
                    datasets: getCountries(this.props, dataIos(), 'organic'),
                  }}
                  options={defaultOptions}
                />
              </CardBody>
            </Card>
          </Col>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Organic installs by country (Android)</BoxHeader>
                <CountryChart
                  component={Bar}
                  data={{
                    labels: dateLabels(dataAndroid()),
                    datasets: getCountries(this.props, dataAndroid(), 'organic'),
                  }}
                  options={defaultOptions}
                />
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default withFilters(
  AdjustInstalls,
  ['apps_flyer_installs_ios', 'dataIos'],
  ['apps_flyer_installs_android', 'dataAndroid'],
);
