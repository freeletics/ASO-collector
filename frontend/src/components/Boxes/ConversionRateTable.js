import React from 'react';
import { Table, Card, CardBody, Col, Row } from 'reactstrap';
import { Line } from 'react-chartjs-2';
import BoxHeader from '../Widget/BoxHeader';
import withFilters from '../Filters/withFilters';
import { MAX_NUMBER_ENTITY_LABELS } from '../Widget/CountryChart';
import SearchAdsNote from '../Widget/SearchAdsNote';
import { getChartData } from '../../services/chartService';
import { dateLabels, getAvgs, getCountries, getFormatedPercent } from './utils';

const getLegendDisplay = data => Object.entries(data).length <= MAX_NUMBER_ENTITY_LABELS;

class ConversionRateTable extends React.Component {
  render() {
    const { dataIos, dataAndroid, colSizes } = this.props;
    return (
      <div>
        <Row>
          <Col lg="7" md="12" sm="12" xs="12">
            <Card>
              <CardBody>
                <BoxHeader>Conversion Rates (IOS)</BoxHeader>
                <Table className="align-middle conversion-table">
                  <thead>
                    <tr>
                      <th />
                      <th colSpan="3" className="border-right">
                        Organic
                      </th>
                      <th colSpan="2" className="border-right">
                        Paid
                      </th>
                      <th />
                    </tr>
                    <tr>
                      <th width="120px" />
                      <th>Total Organic</th>
                      <th>Searchers*</th>
                      <th className="border-right">Browsers</th>
                      <th>Search Ads</th>
                      <th className="border-right">Other Paid</th>
                      <th>Total Searchers (Organic Searchers + Search Ads)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th scope="row">Downloads / Impressions</th>
                      <td>
                        {getFormatedPercent(
                          this.props,
                          dataIos(),
                          'total_organic_impressions',
                        )}
                      </td>
                      <td>
                        {getFormatedPercent(this.props, dataIos(), 'organic_searchers')}
                      </td>
                      <td>
                        {getFormatedPercent(
                          this.props,
                          dataIos(),
                          'impressions_browsers',
                        )}
                      </td>
                      <td>{getFormatedPercent(this.props, dataIos(), 'search_ads')}</td>
                      <td>
                        {getFormatedPercent(this.props, dataIos(), 'impressions_paid')}
                      </td>
                      <td>{getFormatedPercent(this.props, dataIos(), 'searchers')}</td>
                    </tr>
                    <tr>
                      <th scope="row" rowSpan="2">
                        Downloads / Page Views
                      </th>
                      <td>N/A</td>
                      <td>N/A</td>
                      <td>
                        {getFormatedPercent(this.props, dataIos(), 'page_view_browsers')}
                      </td>
                      <td>N/A</td>
                      <td>
                        {getFormatedPercent(this.props, dataIos(), 'page_view_paid')}
                      </td>
                      <td>N/A</td>
                    </tr>
                  </tbody>
                </Table>
                <SearchAdsNote></SearchAdsNote>
              </CardBody>
            </Card>
          </Col>
          <Col lg="5" md="12" sm="12" xs="12">
            <Card>
              <CardBody>
                <BoxHeader>Conversion Rates (Android)</BoxHeader>
                <Table className="align-middle conversion-table">
                  <thead>
                    <tr>
                      <th width="120px" />
                      <th className="border-right">Organic</th>
                      <th>Paid</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th scope="row" rowSpan="2">
                        Downloads / Page Views
                      </th>
                      <td>{getFormatedPercent(this.props, dataAndroid(), 'organic')}</td>
                      <td>{getFormatedPercent(this.props, dataAndroid(), 'paid')}</td>
                    </tr>
                  </tbody>
                </Table>
                <div className="small">
                  Available data are aggregated only daily which leads to differences in
                  impressions/page views value when compering with weekly/monthly ones.
                </div>
                <div className="small">(real conversion rate could be higher)</div>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Conversion history (IOS)</BoxHeader>
                <Line
                  data={getChartData(
                    dateLabels(dataIos()),
                    {
                      'Cr1 = Downloads / Impression (Searches)': {
                        data: getAvgs(this.props, dataIos(), 'searchers'),
                      },
                      'Cr2 = Downloads / Page View (Browsers)': {
                        data: getAvgs(this.props, dataIos(), 'page_view_browsers'),
                      },
                    },
                    ['#00c9ff', '#f85032'],
                  )}
                />
              </CardBody>
            </Card>
          </Col>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Organic conversion history (Android)</BoxHeader>
                <Line
                  data={getChartData(
                    dateLabels(dataAndroid()),
                    {
                      'Cr = Downloads / Page View': {
                        data: getAvgs(this.props, dataAndroid(), 'organic'),
                      },
                    },
                    ['#f85032'],
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
                  Total Searchers conversion history (IOS)
                  <div className="small"> Cr = First-time Downloads / Impression</div>
                </BoxHeader>
                <ConversionRateChart
                  labels={dateLabels(dataIos())}
                  datasets={getCountries(this.props, dataIos(), 'searchers')}
                ></ConversionRateChart>
              </CardBody>
            </Card>
          </Col>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>
                  Organic conversion history (Android)
                  <div className="small"> Cr = First-time Downloads / Impression</div>
                </BoxHeader>
                <ConversionRateChart
                  labels={dateLabels(dataAndroid())}
                  datasets={getCountries(this.props, dataAndroid(), 'organic')}
                ></ConversionRateChart>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>
                  Organic Browsers conversion history (IOS)
                  <div className="small"> Cr = First-time Downloads / Page View</div>
                </BoxHeader>
                <ConversionRateChart
                  labels={dateLabels(dataIos())}
                  datasets={getCountries(this.props, dataIos(), 'page_view_browsers')}
                ></ConversionRateChart>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

const ConversionRateChart = ({ labels, datasets }) => (
  <Line
    data={getChartData(labels, datasets, {
      pointRadius: 2,
    })}
    options={{
      legend: {
        display: getLegendDisplay(datasets),
      },
    }}
  />
);

export default withFilters(
  ConversionRateTable,
  ['app_store_conversion_rates', 'dataIos'],
  ['play_store_conversion_rates', 'dataAndroid'],
);
