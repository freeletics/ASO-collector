import React from 'react';
import Select from 'react-select';
import DatePicker from 'react-datepicker';
import { createBrowserHistory } from 'history';
import queryString from 'query-string';
import queryParams from '../../utils/queryParams';
import moment from 'moment';
import { Row, Col, Label, Button } from 'reactstrap';
import config from '../../config';
import 'react-datepicker/dist/react-datepicker.css';

const CHART_SIZE_HALF = 6;
const CHART_SIZE_FULL = 12;

class OverviewFilters extends React.Component {
  constructor(props) {
    super(props);
    const history = createBrowserHistory();
    this.state = {
      history,
      chartSize: CHART_SIZE_HALF,
      children: [],
      selectedCountries: config.countryOptions.slice(
        0,
        config.filterDefaultCountriesAmount,
      ),
      selectedAggregation: config.aggregationOptions[0],
      toDate: moment().toDate(),
      fromDate: moment()
        .subtract(config.filterDefaultPeriod, 'days')
        .toDate(),
      toCompareDate: moment()
        .subtract(config.filterDefaultPeriod + 1, 'days')
        .toDate(),
      fromCompareDate: moment()
        .subtract(2 * config.filterDefaultPeriod + 1, 'days')
        .toDate(),
    };
    const params = queryString.parse(this.state.history.location.search);
    if (Object.entries(params).length) {
      this.state.selectedCountries = [];
    }
    Object.entries(params).forEach(([name, value]) => {
      if (name === 'aggregation') {
        this.state.selectedAggregation = config.aggregationOptions.find(
          aggregation => aggregation.value === value,
        );
      } else if (name === 'countries') {
        this.state.selectedCountries = config.countryOptions.filter(country =>
          value.split(',').includes(country.value),
        );
      } else if (['from', 'to', 'fromCompare', 'toCompare'].includes(name)) {
        this.state[name + 'Date'] = moment(value, 'YY/MM/DD').toDate();
      }
    });
  }

  handleAggregationChange = selectedAggregation => {
    this.setState(
      {
        selectedAggregation: selectedAggregation ? selectedAggregation : [],
      },
      this.updateChildren,
    );
  };

  handleChartSizeChange = () => {
    this.setState({
      chartSize:
        this.state.chartSize === CHART_SIZE_HALF
          ? CHART_SIZE_FULL
          : CHART_SIZE_HALF,
    });
  };

  handleCountryChange = selectedCountries => {
    this.setState({
      selectedCountries: selectedCountries ? selectedCountries : [],
    }, this.updateChildren);
  };

  handleFromDateChange = date => {
    this.setState({
      fromDate: date < this.state.toDate ? date : this.state.toDate,
    }, this.updateChildren);
  };

  handleToDateChange = date => {
    this.setState({ toDate: date }, this.updateChildren);
  };

  handleFromCompareDateChange = date => {
    this.setState({
      fromCompareDate: date < this.state.toDate ? date : this.state.toDate,
    }, this.updateChildren);
  };

  handleToCompareDateChange = date => {
    this.setState({ toCompareDate: date }, this.updateChildren);
  };

  updateQueryParams = () =>
    this.state.history.push({
      pathname: this.state.history.location.pathname,
      search: queryParams(this.state),
    });

  updateChildren = () => {
    this.updateQueryParams()
    this.state.children.forEach(child => child.update());
  };

  setupChildren() {
    return React.Children.map(this.props.children, child => {
      return React.cloneElement(child, {
        params: this.state,
        colSizes: { xl: this.state.chartSize, lg: this.state.chartSize },
        onRef: ref => this.state.children.push(ref),
      });
    });
  }

  render() {
    const children = this.setupChildren();
    return (
      <div>
        <Row className="align-end">
          <Col lg={4} md={0}>
            <Button
              onClick={this.handleChartSizeChange}
              size="m"
              className="primary border-0"
              block
            >
              Change chart layout
              {this.state.chartSize === CHART_SIZE_HALF ? ' (full)' : ' (half)'}
            </Button>
          </Col>
          <Col lg={4} md={12} sm={12} xs={12} className="mb-3">
            <Button
              onClick={() => {
                navigator.clipboard.writeText(window.location.href).then(
                  function() {
                    console.log('Async: Copying to clipboard was successful!');
                  },
                  function(err) {
                    console.error('Async: Could not copy text: ', err);
                  },
                );
              }}
              size="m"
              className="primary border-0"
              block
            >
              Copy report link
            </Button>
          </Col>
          <Col lg={4} md={12} sm={12} xs={12} className="mb-3">
            <Label>Aggregation</Label>
            <Select
              closeMenuOnSelect={false}
              onChange={this.handleAggregationChange}
              options={config.aggregationOptions}
              value={this.state.selectedAggregation}
            />
          </Col>
          <Col lg={12} md={12} sm={12} xs={12} className="mb-3">
            <Label>Countries</Label>
            <Select
              closeMenuOnSelect={false}
              isMulti
              onChange={this.handleCountryChange}
              options={config.countryOptions}
              value={this.state.selectedCountries}
              placeholder="Select countries (default all)"
            />
          </Col>
          <Col lg={3} md={6} sm={6} xs={12} className="mb-3">
            <Label>From</Label>
            <DatePicker
              dateFormat={config.datePickerFormat}
              selected={this.state.fromDate}
              onChange={this.handleFromDateChange}
            />
          </Col>
          <Col lg={3} md={6} sm={6} xs={12} className="mb-3">
            <Label>To</Label>
            <DatePicker
              dateFormat={config.datePickerFormat}
              selected={this.state.toDate}
              onChange={this.handleToDateChange}
            />
          </Col>
          <Col lg={3} md={6} sm={6} xs={12} className="mb-3">
            <Label>From (comparison)</Label>
            <DatePicker
              dateFormat={config.datePickerFormat}
              selected={this.state.fromCompareDate}
              onChange={this.handleFromCompareDateChange}
            />
          </Col>
          <Col lg={3} md={6} sm={6} xs={12} className="mb-3">
            <Label>To (comparison)</Label>
            <DatePicker
              dateFormat={config.datePickerFormat}
              selected={this.state.toCompareDate}
              onChange={this.handleToCompareDateChange}
            />
          </Col>
        </Row>
        {children}
      </div>
    );
  }
}

export default OverviewFilters;
