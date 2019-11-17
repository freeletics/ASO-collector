import React from 'react';
import { Card, CardBody, Col, Row } from 'reactstrap';
import { Bar } from 'react-chartjs-2';
import BoxHeader from '../Widget/BoxHeader';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { defaultOptions, getChartData } from '../../services/chartService';
import { dateLabels, getSums, getCountries } from './utils';
import SearchAdsNote from '../Widget/SearchAdsNote';

class Impressions extends React.Component {
  render() {
    const { dataIos, colSizes } = this.props;
    return (
      <div>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Organic impressions by country (IOS)</BoxHeader>
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
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>
                  Organic impressions Browsers by country (iOS)
                </BoxHeader>
                <CountryChart
                  component={Bar}
                  data={{
                    labels: dateLabels(dataIos()),
                    datasets: getCountries(this.props, dataIos(), 'browsers'),
                  }}
                  options={defaultOptions}
                />
                <SearchAdsNote></SearchAdsNote>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>
                  Organic impressions Searchers by country (iOS)
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
                <SearchAdsNote></SearchAdsNote>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Impressions by type (IOS)</BoxHeader>
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
                <SearchAdsNote></SearchAdsNote>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default withFilters(Impressions, ['app_store_impressions', 'dataIos']);
