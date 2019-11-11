import React from 'react';
import { Card, CardBody, Col, Row } from 'reactstrap';
import { Line } from 'react-chartjs-2';
import BoxHeader from '../Widget/BoxHeader';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { defaultOptions } from '../../services/chartService';
import { dateLabels, getKeywords, capitalize } from './utils';

const getData = (props, platform, countries) => {
  return countries.length
    ? props.data(`data${capitalize(platform)}${capitalize(countries[0].value)}`)
    : [];
};

class Keywords extends React.Component {
  render() {
    const countriesSelected = this.props.params.selectedCountries;
    const countriesSelectedCount = this.props.params.selectedCountries.length;
    const dataIos = getData(this.props, 'ios', countriesSelected);
    const dataAndroid = getData(this.props, 'android', countriesSelected);
    return (
      <Row>
        <Col xl={6} lg={6} md={12}>
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
        <Col xl={6} lg={6} md={12}>
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
  ['sensortower_current_keywords_ios_de', 'dataIosDe'],
  ['sensortower_current_keywords_android_de', 'dataAndroidDe'],
  ['sensortower_current_keywords_ios_us', 'dataIosUs'],
  ['sensortower_current_keywords_android_us', 'dataAndroidUs'],
  ['sensortower_current_keywords_ios_gb', 'dataIosGb'],
  ['sensortower_current_keywords_android_gb', 'dataAndroidGb'],
  ['sensortower_current_keywords_ios_fr', 'dataIosFr'],
  ['sensortower_current_keywords_android_fr', 'dataAndroidFr'],
  ['sensortower_current_keywords_ios_it', 'dataIosIt'],
  ['sensortower_current_keywords_android_it', 'dataAndroidIt'],
);
