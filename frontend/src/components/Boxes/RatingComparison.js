import React from 'react';
import { Row, Col } from 'reactstrap';
import NumberWidget from '../Widget/NumberWidget';
import withFilters from '../Filters/withFilters';
import { getAvg } from './utils';

class RatingComparison extends React.Component {
  render() {
    const {
      dataIos,
      dataIosCompare,
      dataAndroid,
      dataAndroidCompare,
    } = this.props;
    return (
      <div>
        <Row className="justify-content">
          <Col lg="4" md="4" sm="6" xs="12">
            <RatingComparisonWidget
              title="Ratings IOS"
              number={getAvg(this.props, dataIos('dataIosRating'))}
              numberCompare={getAvg(
                this.props,
                dataIosCompare('dataIosRating'),
              )}
            />
          </Col>
          <Col lg="4" md="4" sm="6" xs="12">
            <RatingComparisonWidget
              title="Ratings Android"
              subtitle="(available only when no country selected)"
              number={getAvg(this.props, dataAndroid('dataAndroidRating'))}
              numberCompare={getAvg(
                this.props,
                dataAndroidCompare('dataAndroidRating'),
              )}
            />
          </Col>
        </Row>
        <Row className="justify-content">
          <Col lg="4" md="4" sm="6" xs="12">
            <RatingComparisonWidget
              title="Review ratings IOS"
              number={getAvg(this.props, dataIos('dataIosReview'))}
              numberCompare={getAvg(
                this.props,
                dataIosCompare('dataIosReview'),
              )}
            />
          </Col>
          <Col lg="4" md="4" sm="6" xs="12">
            <RatingComparisonWidget
              title="Review ratings Android"
              number={getAvg(this.props, dataAndroid('dataAndroidReview'))}
              numberCompare={getAvg(
                this.props,
                dataAndroidCompare('dataAndroidReview'),
              )}
            />
          </Col>
        </Row>
      </div>
    );
  }
}

const RatingComparisonWidget = ({ title, subtitle, number, numberCompare }) => {
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

export default withFilters(
  RatingComparison,
  ['sensortower_ratings_ios', 'dataIosRating'],
  ['sensortower_ratings_android', 'dataAndroidRating'],
  ['sensortower_reviews_ios', 'dataIosReview'],
  ['sensortower_reviews_android', 'dataAndroidReview'],
);
