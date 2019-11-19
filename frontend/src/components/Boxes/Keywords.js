import React from 'react';
import { Card, CardBody, Col, Row } from 'reactstrap';
import { Line } from 'react-chartjs-2';
import BoxHeader from '../Widget/BoxHeader';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { defaultOptions } from '../../services/chartService';
import { dateLabels, getKeywords } from './utils';

class Keywords extends React.Component {
  render() {
    const countriesSelectedCount = this.props.params.selectedCountries.length;
    const dataIos = this.props.dataIos();
    const dataAndroid = this.props.dataAndroid();
    const { colSizes } = this.props;
    return (
      <Row>
        <Col {...colSizes} lg={6} md={12}>
          <Card>
            <CardBody>
              <KeywordsRankingHistory
                platform="IOS"
                data={{
                  labels: dateLabels(dataIos),
                  datasets: getKeywords(dataIos),
                }}
                countriesSelectedCount={countriesSelectedCount}
              ></KeywordsRankingHistory>
            </CardBody>
          </Card>
        </Col>
        <Col {...colSizes}  lg={6} md={12}>
          <Card>
            <CardBody>
              <KeywordsRankingHistory
                platform="Android"
                data={{
                  labels: dateLabels(dataAndroid),
                  datasets: getKeywords(dataAndroid),
                }}
                countriesSelectedCount={countriesSelectedCount}
              ></KeywordsRankingHistory>
            </CardBody>
          </Card>
        </Col>
      </Row>
    );
  }
}

const KeywordsRankingHistory = ({ platform, data, countriesSelectedCount }) => {
  const containsData = Object.entries(data.datasets).length !== 0;
  return (
    <div>
      <BoxHeader>Keywords ranking ({platform})</BoxHeader>
      {countriesSelectedCount === 1
        ? containsData && (
            <CountryChart
              component={Line}
              data={data}
              options={{
                ...defaultOptions,
                scales: {
                  yAxes: [
                    {
                      ticks: {
                        reverse: true,
                      },
                    },
                  ],
                },
                display: true,
              }}
            />
          )
        : 'Visible only when one country selected'}
      {!containsData &&
        countriesSelectedCount === 1 &&
        'No data or keywords not tracked for selected country'}
    </div>
  );
};

export default withFilters(
  Keywords,
  ['app_follow_keywords_ios', 'dataIos'],
  ['app_follow_keywords_android', 'dataAndroid'],
);
