import React from 'react';
import { Row, Col, Card, CardBody } from 'reactstrap';
import { Line } from 'react-chartjs-2';
import NumberWidget from '../Widget/NumberWidget';
import BoxHeader from '../Widget/BoxHeader';
import CountryChart from '../Widget/CountryChart';
import withFilters from '../Filters/withFilters';
import { getChartData, rankingScaleOption } from '../../services/chartService';
import { avg, getAvgs, getCountries, dateLabels } from './utils';

class RankingComparison extends React.Component {
  render() {
    const {
      dataIos,
      dataIosCompare,
      dataAndroid,
      dataAndroidCompare,
      colSizes,
    } = this.props;
    return (
      <div>
        <Row className="justify-content">
          <Col lg="4" md="4" sm="6" xs="12">
            <RankingComparisonWidget
              title={'Ranking IOS'}
              subtitle={'All'}
              number={avg(getAvgs(this.props, dataIos(), '0_topfreeapplications'))}
              numberCompare={avg(
                getAvgs(this.props, dataIosCompare(), '0_topfreeapplications'),
              )}
            />
          </Col>

          <Col lg="4" md="4" sm="6" xs="12">
            <RankingComparisonWidget
              title={'Ranking Android'}
              subtitle={'All'}
              number={avg(
                getAvgs(this.props, dataAndroid(), 'application_topselling_free'),
              )}
              numberCompare={avg(
                getAvgs(this.props, dataAndroidCompare(), 'application_topselling_free'),
              )}
            />
          </Col>
        </Row>
        <Row className="justify-content">
          <Col lg="4" md="4" sm="6" xs="12">
            <RankingComparisonWidget
              title={'Ranking IOS'}
              subtitle={'Health & Fitness'}
              number={avg(getAvgs(this.props, dataIos(), '6013_topfreeapplications'))}
              numberCompare={avg(
                getAvgs(this.props, dataIosCompare(), '6013_topfreeapplications'),
              )}
            />
          </Col>
          <Col lg="4" md="4" sm="6" xs="12">
            <RankingComparisonWidget
              title={'Ranking Android'}
              subtitle={'Health & Fitness'}
              number={avg(
                getAvgs(this.props, dataAndroid(), 'health_and_fitness_topselling_free'),
              )}
              numberCompare={avg(
                getAvgs(
                  this.props,
                  dataAndroidCompare(),
                  'health_and_fitness_topselling_free',
                ),
              )}
            />
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <LifestyleChartBox
              title={'Ranking inside Health & Fitness Category (IOS)'}
              labels={dateLabels(dataIos())}
              data={getAvgs(this.props, dataIos(), '6013_topfreeapplications')}
            ></LifestyleChartBox>
          </Col>
          <Col {...colSizes} md={12}>
            <LifestyleChartBox
              title={'Ranking inside Health & Fitness Category (Android)'}
              labels={dateLabels(dataAndroid())}
              data={getAvgs(
                this.props,
                dataAndroid(),
                'health_and_fitness_topselling_free',
              )}
            ></LifestyleChartBox>
          </Col>
        </Row>
        <Row>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Ranking inside Health & Fitness Category (IOS)</BoxHeader>
                <CountryChart
                  component={Line}
                  data={{
                    labels: dateLabels(dataIos()),
                    datasets: getCountries(
                      this.props,
                      dataIos(),
                      '6013_topfreeapplications',
                    ),
                  }}
                  options={rankingScaleOption}
                />
              </CardBody>
            </Card>
          </Col>
          <Col {...colSizes} md={12}>
            <Card>
              <CardBody>
                <BoxHeader>Ranking inside Health & Fitness Category (Android)</BoxHeader>
                <CountryChart
                  component={Line}
                  data={{
                    labels: dateLabels(dataIos()),
                    datasets: getCountries(
                      this.props,
                      dataAndroid(),
                      'health_and_fitness_topselling_free',
                    ),
                  }}
                  options={rankingScaleOption}
                />
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

const RankingComparisonWidget = ({ title, subtitle, number, numberCompare }) => {
  return (
    <NumberWidget
      className="no-border"
      title={title}
      subtitle={subtitle ? subtitle : ''}
      number={number ? number : 0}
      numberCompare={numberCompare ? numberCompare : 0}
      color="secondary"
    />
  );
};

const LifestyleChartBox = ({ data, labels, title }) => {
  return (
    <Card>
      <CardBody>
        <BoxHeader>{title}</BoxHeader>
        <Line
          data={getChartData(labels, {
            Position: data,
          })}
          options={{ ...rankingScaleOption }}
        />
      </CardBody>
    </Card>
  );
};

export default withFilters(
  RankingComparison,
  ['sensortower_rankings_ios', 'dataIos'],
  ['sensortower_rankings_android', 'dataAndroid'],
);
