import React from 'react';
import { Card, CardBody, Col, Row } from 'reactstrap';
import { Bar } from 'react-chartjs-2';
import BoxHeader from '../Widget/BoxHeader';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { defaultOptions, getChartData } from '../../services/chartService';
import SearchAdsNote from '../Widget/SearchAdsNote';
import { dateLabels, getSums, getCountries } from './utils';

class Downloads extends React.Component {
  render() {
    const { dataIos, dataAndroid, colSizes } = this.props;
    console.log(dateLabels(dataIos()));
    return (
      <div>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>First-time Downloads by type (iOS)</BoxHeader>
                <Bar
                  data={getChartData(
                    dateLabels(dataIos()),
                    {
                      'Organic installs': getSums(
                        this.props,
                        dataIos(),
                        'organic',
                      ),
                      'Paid installs': getSums(this.props, dataIos(), 'paid'),
                    },
                    ['#2196f3', '#4caf50'],
                  )}
                  options={defaultOptions}
                />
                <SearchAdsNote></SearchAdsNote>
              </CardBody>
            </Card>
          </Col>
          <Col {...this.props.colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>First-time Downloads by type (Android)</BoxHeader>
                <Bar
                  data={getChartData(
                    dateLabels(dataAndroid()),
                    {
                      'Organic installs': getSums(
                        this.props,
                        dataAndroid(),
                        'organic',
                      ),
                      'Paid installs': getSums(
                        this.props,
                        dataAndroid(),
                        'paid',
                      ),
                    },
                    ['#2196f3', '#4caf50'],
                  )}
                  options={defaultOptions}
                />
              </CardBody>
            </Card>
          </Col>
        </Row>

        <Row>
          <Col {...this.props.colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>
                  Organic First-time Downloads by Country (iOS)
                </BoxHeader>
                <CountryChart
                  component={Bar}
                  data={{
                    labels: dateLabels(dataIos()),
                    datasets: getCountries(this.props, dataIos(), 'organic'),
                  }}
                  options={defaultOptions}
                />
                <SearchAdsNote></SearchAdsNote>
              </CardBody>
            </Card>
          </Col>
          <Col {...this.props.colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>
                  Organic First-time Downloads by Country (Android)
                </BoxHeader>
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
  Downloads,
  ['app_store_downloads', 'dataIos'],
  ['play_store_downloads', 'dataAndroid'],
);
