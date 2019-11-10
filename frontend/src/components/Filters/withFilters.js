import React from 'react';
import * as CSV from 'csv-string';
import moment from 'moment';
import fetchData from '../../services/fetchData';

export const getRange = ({ from, to }, data) =>
  data.filter(
    row => from <= moment(row.date).toDate() && to >= moment(row.date).toDate(),
  );

export class Wrapper extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loaded: false,
    };
  }

  componentDidMount() {
    this.props.onRef(this);
    this.update();
  }

  componentWillUnmount() {
    this.props.onRef(undefined);
  }

  dates() {
    const { fromDate, toDate } = this.props.params;
    return { from: fromDate, to: toDate };
  }

  data = name => getRange(this.dates(), this.state[name]);
}

const withFilters = (WrappedComponent, ...dataSources) => {
  return class extends Wrapper {
    processData(rawString) {
      const data = CSV.parse(rawString);
      const fieldNames = data.shift();
      return data.map(row =>
        row.reduce((o, value, index) => ({ ...o, [fieldNames[index]]: value }), {}),
      );
    }

    getAggregation(base, aggregation) {
      if (base.includes('featured') || base.includes('timeline')) {
        aggregation = 'days';
      }
      return aggregation;
    }

    getFilename(base, aggregation) {
      return `${base}_${this.getAggregation(base, aggregation)}.csv`;
    }

    datesCompare() {
      const { fromCompareDate, toCompareDate } = this.props.params;
      return { from: fromCompareDate, to: toCompareDate };
    }

    update() {
      const aggregation = this.props.params.selectedAggregation.value;
      dataSources.forEach(([filenameBase, dataName]) => {
        fetchData(this.getFilename(filenameBase, aggregation), data =>
          this.setState({
            ['loaded' + dataName]: true,
            [dataName]: this.processData(data),
          }),
        );
      });
    }

    allLoaded() {
      return dataSources.map(([_, dataName]) => this.state['loaded' + dataName]);
    }

    data = name => getRange(this.dates(), this.state[name]);

    dataIos = (name = 'dataIos') => getRange(this.dates(), this.state[name]);

    dataAndroid = (name = 'dataAndroid') => getRange(this.dates(), this.state[name]);

    dataIosCompare = (name = 'dataIos') =>
      getRange(this.datesCompare(), this.state[name]);

    dataAndroidCompare = (name = 'dataAndroid') =>
      getRange(this.datesCompare(), this.state[name]);

    render() {
      return this.allLoaded().every(x => Boolean(x)) ? (
        <WrappedComponent
          {...this.props}
          data={this.data}
          dataAndroid={this.dataAndroid}
          dataIos={this.dataIos}
          dataAndroidCompare={this.dataAndroidCompare}
          dataIosCompare={this.dataIosCompare}
        />
      ) : null;
    }
  };
};

export default withFilters;
