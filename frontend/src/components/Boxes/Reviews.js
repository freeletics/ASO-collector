import React from 'react';
import { Card, CardBody, Col, Row } from 'reactstrap';
import { Bar, Line } from 'react-chartjs-2';
import BoxHeader from '../Widget/BoxHeader';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { defaultColors, starColors } from '../../config/colors';
import {
  starsConfig,
  defaultOptions,
  getChartData,
  ratingScaleOption,
} from '../../services/chartService';
import { dateLabels, getCountriesAvg, getReviewsDatasets } from './utils';

class Reviews extends React.Component {
  render() {
    const { dataIos, dataAndroid, colSizes } = this.props;
    return (
      <div>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Review rating (iOS)</BoxHeader>
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
                <BoxHeader>Review rating (Android)</BoxHeader>
                <Bar
                  data={getChartData(
                    dateLabels(dataAndroid()),
                    getReviewsDatasets(this.props, dataAndroid()),
                    [defaultColors[0], ...Object.values(starColors)],
                  )}
                  options={starsConfig}
                />
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Review rating by country (IOS)</BoxHeader>
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
                <BoxHeader>Review rating by country (Android)</BoxHeader>
                <CountryChart
                  component={Line}
                  data={{
                    labels: dateLabels(dataAndroid()),
                    datasets: getCountriesAvg(this.props, dataAndroid()),
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
        </Row>
      </div>
    );
  }
}

export default withFilters(
  Reviews,
  ['sensortower_reviews_ios', 'dataIos'],
  ['sensortower_reviews_android', 'dataAndroid'],
);
