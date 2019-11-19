import React from 'react';
import { Card, CardBody, Col, Row, Table } from 'reactstrap';
import BoxHeader from '../Widget/BoxHeader';
import withFilters from '../Filters/withFilters';
import { notDate, avg, setDefault } from './utils';

const getData = data => {
  const searchResult = {};
  data.forEach(item => {
    Object.entries(item).forEach(([position, key]) => {
      if (notDate(position)) {
        setDefault(searchResult, key, [], parseInt(position));
      }
    });
  });
  Object.entries(([key, positions]) => (searchResult[key] = avg(positions)));
  return Object.keys(searchResult).sort(function(a, b) {
    return searchResult[a] - searchResult[b];
  }).slice(0,10);
};

class SearchAso extends React.Component {
  render() {
    const countriesSelectedCount = this.props.params.selectedCountries.length;
    const dataIos = getData(this.props.dataIos());
    const dataAndroid = getData(this.props.dataAndroid());
    return (
      <div>
        <Row>
          <Col xl={6} lg={6} md={12}>
            <Card>
              <CardBody>
                <KeywordRankingWidget
                  platform="IOS"
                  data={dataIos}
                  countriesSelectedCount={countriesSelectedCount}
                  displayLegend
                ></KeywordRankingWidget>
              </CardBody>
            </Card>
          </Col>
          <Col xl={6} lg={6} md={12}>
            <Card>
              <CardBody>
                <KeywordRankingWidget
                  platform="Android"
                  data={dataAndroid}
                  countriesSelectedCount={countriesSelectedCount}
                  displayLegend
                ></KeywordRankingWidget>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

const KeywordTable = ({ ranking }) => {
  return (
    <Table className="fix-table">
      <thead>
        <tr>
          <th width="15px" />
          <th>App name</th>
        </tr>
      </thead>
      <tbody>
        {ranking.map((entity, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{entity}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

const KeywordRankingWidget = ({ platform, data, countriesSelectedCount }) => {
  return (
    <div>
      <BoxHeader>Top 10 apps for the keyword "Freeletics" ({platform})</BoxHeader>
      {countriesSelectedCount === 1 ? (
        <KeywordTable ranking={data}></KeywordTable>
      ) : (
        'Visible only when one country selected'
      )}
    </div>
  );
};

export default withFilters(
  SearchAso,
  ['app_follow_aso_search_ios', 'dataIos'],
  ['app_follow_aso_search_android', 'dataAndroid'],
);
