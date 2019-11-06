import React from 'react';
import { Card, CardBody, Col, Row } from 'reactstrap';
import { Bar } from 'react-chartjs-2';
import BoxHeader from '../Widget/BoxHeader';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { defaultOptions, getChartData } from '../../services/chartService';
import { notDate, dateLabels, isCountrySelected, getCountryFromKey } from './utils';

const condition = (props, key, type) =>
  notDate(key) && key.includes(type) && isCountrySelected(props, key);

class AdjustInstalls extends React.Component {
  getInstallsSum(data, type) {
    return data.map(row =>
      Object.entries(row).reduce((sum, [key, value]) => {
        return condition(this.props, key, type) ? sum + Number(value) : sum;
      }, 0),
    );
  }

  getCountries(data, type) {
    const datasets = {};
    data.forEach(row =>
      Object.entries(row).forEach(([key, value]) => {
        if (condition(this.props, key, type)) {
          const country = getCountryFromKey(key)
          datasets[country] = datasets[country] ? datasets[country] : [];
          datasets[country].push(value);
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
                    'Organic installs': this.getInstallsSum(
                      dataIos(),
                      'organic',
                    ),
                    'Paid installs': this.getInstallsSum(dataIos(), 'paid'),
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
                    'Organic installs': this.getInstallsSum(
                      dataAndroid(),
                      'organic',
                    ),
                    'Paid installs': this.getInstallsSum(dataAndroid(), 'paid'),
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
                    datasets: this.getCountries(dataIos(), 'organic'),
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
                    datasets: this.getCountries(dataAndroid(), 'organic'),
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
