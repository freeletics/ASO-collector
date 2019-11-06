import React from 'react';
import {
  Table,
  Card,
  CardBody,
  Row,
  Col,
  ListGroup,
  ListGroupItem,
} from 'reactstrap';
import { Doughnut } from 'react-chartjs-2';
import { defaultColors } from '../../config/colors';
import BoxHeader from '../Widget/BoxHeader';
import PercentageWidget from '../Widget/PercentageWidget';
import withFilters from '../Filters/withFilters';
import { dateLabels, getSums, sum, getCountries } from './utils';

class InstallsDoughnut extends React.Component {
  getChartData(data) {
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

  getData(organic, paid) {
    return {
      organic,
      paid,
      total: organic + paid,
    };
  }

  render() {
    const { dataIos, dataAndroid } = this.props;
    const organicAndroid = getSums(this.props, dataAndroid(), 'organic').reduce(
      sum,
    );
    const organicIos = getSums(this.props, dataIos(), 'organic').reduce(sum);
    const paidAndroid = getSums(this.props, dataAndroid(), 'paid').reduce(sum);
    const paidIos = getSums(this.props, dataIos(), 'paid').reduce(sum);
    const installsIos = this.getData(organicIos, paidIos);
    const installsAndroid = this.getData(organicAndroid, paidAndroid);
    return (
      <div>
        <Row className="justify-content">
          <Col lg="5" md="5" sm="6" xs="12">
            <Card>
              <CardBody>
                <BoxHeader>Installs (IOS)</BoxHeader>
                <Doughnut data={this.getChartData([organicIos, paidIos])} />
                <ListGroup flush>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Organic"
                      data={installsIos}
                      field={'organic'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Paid"
                      data={installsIos}
                      field={'paid'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Total"
                      data={installsIos}
                      field={'total'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                </ListGroup>
              </CardBody>
            </Card>
          </Col>
          <Col lg="5" md="5" sm="6" xs="12">
            <Card>
              <CardBody>
                <BoxHeader>Installs (Android)</BoxHeader>
                <Doughnut
                  data={this.getChartData([organicAndroid, paidAndroid])}
                />
                <ListGroup flush>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Organic"
                      data={installsAndroid}
                      field={'organic'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Paid"
                      data={installsAndroid}
                      field={'paid'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                  <ListGroupItem className="p-1">
                    <PercentageWidget
                      title="Total"
                      data={installsAndroid}
                      field={'total'}
                      fieldTotal={'total'}
                    ></PercentageWidget>
                  </ListGroupItem>
                </ListGroup>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default withFilters(
  InstallsDoughnut,
  ['apps_flyer_installs_ios', 'dataIos'],
  ['apps_flyer_installs_android', 'dataAndroid'],
);
