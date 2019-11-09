import React from 'react';
import { Card, CardBody, Row, Col, ListGroup, ListGroupItem } from 'reactstrap';
import { Doughnut, Bar } from 'react-chartjs-2';
import { defaultColors } from '../../config/colors';
import BoxHeader from '../Widget/BoxHeader';
import PercentageWidget from '../Widget/PercentageWidget';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { defaultOptions, getChartData } from '../../services/chartService';
import SearchAdsNote from '../Widget/SearchAdsNote';
import { dateLabels, reduce, getCountries, getSums } from './utils';

const getLabel = (datasetLabel, datasetIndex, browsers, searchers) => {
  const sum = searchers + browsers;
  if (datasetIndex) {
    return getLabelForValue(datasetLabel, sum, searchers);
  } else {
    return getLabelForValue(datasetLabel, sum, browsers);
  }
};

const getLabelForValue = (datasetLabel, sum, value) => {
  return (
    datasetLabel +
    ': ' +
    ((value * 100.0) / sum).toPrecision(2) +
    '% (' +
    value.toLocaleString() +
    ')'
  );
};

class NewDownloads extends React.Component {
  getAndroidData(data) {
    return {
      labels: ['Organic', 'Paid'],
      datasets: [
        {
          data,
          backgroundColor: defaultColors,
        },
      ],
    };
  }

  getIosData(data) {
    return {
      labels: ['Browsers', 'Organic Searchers', 'Search Ads', 'Other Paid'],
      datasets: [
        {
          data,
          backgroundColor: defaultColors,
        },
      ],
    };
  }

  render() {
    const { dataIos, dataAndroid, colSizes } = this.props;
    const browsersIos = reduce(this.props, dataIos(), 'browsers');
    const searchersIos = reduce(this.props, dataIos(), 'organic_searches');
    const otherPaid = reduce(this.props, dataIos(), 'other_paid');
    const searchAds = reduce(this.props, dataIos(), 'search_ads');
    const downloadsIos = {
      searchAds: searchAds,
      otherPaid: otherPaid,
      browsers: browsersIos,
      searchers: searchersIos,
      total: searchersIos + browsersIos + otherPaid + searchAds,
    };
    const organicAndroid = reduce(this.props, dataAndroid(), 'organic');
    const paidAndroid = reduce(this.props, dataAndroid(), 'paid');
    const downloadsAndroid = {
      organic: organicAndroid,
      paid: paidAndroid,
      total: organicAndroid + paidAndroid,
    };
    console.log(downloadsAndroid);
    return (
      <div>
        <Row className="justify-content">
          <Col lg="5" md="5" sm="6" xs="12">
            <Card>
              <CardBody>
                <BoxHeader>First-time Downloads (IOS)</BoxHeader>
                <Doughnut
                  data={this.getIosData([
                    browsersIos,
                    searchersIos,
                    searchAds,
                    otherPaid,
                  ])}
                />
                <ListGroup flush>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Browsers"
                      data={downloadsIos}
                      field={'browsers'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Organic Searchers"
                      data={downloadsIos}
                      field={'searchers'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Search Ads"
                      data={downloadsIos}
                      field={'searchAds'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Other Paid"
                      data={downloadsIos}
                      field={'otherPaid'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                </ListGroup>
                <SearchAdsNote></SearchAdsNote>
              </CardBody>
            </Card>
          </Col>
          <Col lg="5" md="5" sm="6" xs="12">
            <Card>
              <CardBody>
                <BoxHeader>First-time Downloads (Android)</BoxHeader>
                <Doughnut data={this.getAndroidData([organicAndroid, paidAndroid])} />
                <ListGroup flush>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Organic"
                      data={downloadsAndroid}
                      field={'organic'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Paid"
                      data={downloadsAndroid}
                      field={'paid'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                </ListGroup>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Organic First-time Downloads by country (IOS)</BoxHeader>
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
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Organic First-time Downloads by country (Android)</BoxHeader>
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
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>
                  First-time Downloads Organic Searchers vs Browsers by country (IOS)
                </BoxHeader>
                <Bar
                  data={getChartData(dateLabels(dataIos()), {
                    Browsers: getSums(this.props, dataIos(), 'browsers'),
                    'Organic Searchers': getSums(
                      this.props,
                      dataIos(),
                      'organic_searchers',
                    ),
                  })}
                  options={{
                    ...defaultOptions,
                    tooltips: {
                      callbacks: {
                        label: function(tooltipItem, data) {
                          const datasetLabel =
                            data.datasets[tooltipItem.datasetIndex].label;
                          const browsers = Number(
                            data.datasets[0].data[tooltipItem.index],
                          );
                          const searchers = Number(
                            data.datasets[1].data[tooltipItem.index],
                          );
                          return getLabel(
                            datasetLabel,
                            tooltipItem.datasetIndex,
                            browsers,
                            searchers,
                          );
                        },
                      },
                    },
                  }}
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

export default withFilters(
  NewDownloads,
  ['app_store_downloads', 'dataIos'],
  ['play_store_downloads', 'dataAndroid'],
);
