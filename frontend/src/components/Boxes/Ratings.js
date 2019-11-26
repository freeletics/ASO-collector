import React from 'react';
import { Card, CardBody, Col, Row } from 'reactstrap';
import { Bar, Line } from 'react-chartjs-2';
import { defaultColors, starColors } from '../../config/colors';
import BoxHeader from '../Widget/BoxHeader';
import withFilters from '../Filters/withFilters';
import CountryChart from '../Widget/CountryChart';
import {
  starsConfig,
  defaultOptions,
  getChartData,
  ratingScaleOption,
} from '../../services/chartService';
import { dateLabels, getCountriesAvg, getReviewsDatasets } from './utils';

class Ratings extends React.Component {
  render() {
    const { dataIos, dataAndroid, colSizes } = this.props;
    return (
      <div>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Rating (iOS)</BoxHeader>
                <Bar
                  data={getChartData(
                    dateLabels(dataIos()),
                    getReviewsDatasets(this.props, dataIos()),
                    [defaultColors[0], ...Object.values(starColors)],
                  )}
                  options={starsConfig}
                />
              </CardBody>
            </Card>
          </Col>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Rating (Android) global</BoxHeader>
                <div className="small">Cumulative data due to lack of an access to correct relative one (per day).</div>
                {this.props.params.selectedCountries.length === 0 ? (
                  <Bar
                    data={getChartData(
                      dateLabels(dataAndroid()),
                      getReviewsDatasets(this.props, dataAndroid()),
                      [defaultColors[0], ...Object.values(starColors)],
                    )}
                    options={starsConfig}
                  />
                ) : (
                  'Available only when no country selected'
                )}
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Rating by Country (iOS)</BoxHeader>
                <CountryChart
                  component={Line}
                  data={{
                    labels: dateLabels(dataIos()),
                    datasets: getCountriesAvg(this.props, dataIos()),
                  }}
                  options={{
                    ...defaultOptions,
                    ...ratingScaleOption,
                  }}
                  datasetOption={{
                    pointRadius: 2,
                  }}
                />
              </CardBody>
            </Card>
          </Col>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Rating by Country (Android)</BoxHeader>
                <div className="small">
                  Data per country for Android are not available
                </div>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default withFilters(
  Ratings,
  ['app_follow_rating_ios', 'dataIos'],
  ['app_follow_rating_android', 'dataAndroid'],
);
