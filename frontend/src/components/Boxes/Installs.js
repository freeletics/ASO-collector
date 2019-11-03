import React from 'react';
import { Card, CardBody, Col, Row } from 'reactstrap';
import { Bar } from 'react-chartjs-2';
import BoxHeader from '../Widget/BoxHeader';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { defaultOptions, getChartData } from '../../services/chartService';
import { notDate, dateLabels, isCountrySelected } from './utils';

class AdjustInstalls extends React.Component {
  getInstallsSum(data) {
    return data.map(row =>
      Object.entries(row).reduce((sum, [key, value]) => {
        return notDate(key) && isCountrySelected(this.props, key)
          ? sum + Number(value)
          : sum;
      }, 0),
    );
  }

  getCountries(data) {
    const datasets = {};
    data.forEach(row =>
      Object.entries(row).forEach(([key, value]) => {
        if (notDate(key) && isCountrySelected(this.props, key)) {
          datasets[key] = datasets[key] ? datasets[key] : [];
          datasets[key].push(value);
        }
      }),
    );
    return datasets;
  }

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
                    'Total installs': this.getInstallsSum(dataIos()),
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
                    'Total installs': this.getInstallsSum(dataAndroid()),
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
                    datasets: this.getCountries(dataIos()),
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
                    datasets: this.getCountries(dataAndroid()),
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
