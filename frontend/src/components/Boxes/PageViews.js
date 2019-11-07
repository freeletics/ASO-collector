import React from 'react';
import { Card, CardBody, Col, Row } from 'reactstrap';
import { Bar, Line } from 'react-chartjs-2';
import BoxHeader from '../Widget/BoxHeader';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { defaultOptions, getChartData } from '../../services/chartService';
import { dateLabels, getSums, getCountries } from './utils';

class PageViews extends React.Component {
  render() {
    const { dataIos, dataAndroid, colSizes } = this.props;
    return (
      <div>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Organic page views by country (IOS)</BoxHeader>
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
                <BoxHeader>Organic page views by country (Android)</BoxHeader>
                <CountryChart
                  component={Bar}
                  data={{
                    labels: dateLabels(dataAndroid()),
                    datasets: getCountries(
                      this.props,
                      dataAndroid(),
                      'organic',
                    ),
                  }}
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
                <BoxHeader>Page views by type (IOS)</BoxHeader>
                <Bar
                  options={defaultOptions}
                  data={getChartData(dateLabels(dataIos()), {
                    Browsers: getSums(this.props, dataIos(), 'browsers'),
                    Searchers: getSums(
                      this.props,
                      dataIos(),
                      'organic_searchers',
                    ),
                    'Other Paid': getSums(this.props, dataIos(), 'other_paid'),
                    'Search Ads': getSums(this.props, dataIos(), 'search_ads'),
                  })}
                />
              </CardBody>
            </Card>
          </Col>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>
                  Organic vs. non-organic page views (Android)
                </BoxHeader>
                <Line
                  data={getChartData(
                    dateLabels(dataAndroid()),
                    {
                      'Organic Page Views': getSums(
                        this.props,
                        dataAndroid(),
                        'organic',
                      ),
                      'Paid page views': getSums(
                        this.props,
                        dataAndroid(),
                        'paid',
                      ),
                    },
                    ['#2196f3', '#4caf50'],
                  )}
                />
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>
                  Organic page views browsers by country (iOS)
                </BoxHeader>
                <CountryChart
                  component={Bar}
                  data={{
                    labels: dateLabels(dataIos()),
                    datasets: getCountries(this.props, dataIos(), 'browsers'),
                  }}
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
                <BoxHeader>
                  Organic page views searchers by country (iOS)
                </BoxHeader>
                <CountryChart
                  component={Bar}
                  data={{
                    labels: dateLabels(dataIos()),
                    datasets: getCountries(
                      this.props,
                      dataIos(),
                      'organic_searchers',
                    ),
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
  PageViews,
  ['app_store_page_views', 'dataIos'],
  ['play_store_page_views', 'dataAndroid'],
);
