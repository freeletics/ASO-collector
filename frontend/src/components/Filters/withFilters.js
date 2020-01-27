import React from 'react';
import * as CSV from 'csv-string';
import moment from 'moment';
import fetchData from '../../services/fetchData';

export const getRange = ({ from, to }, data) => {
  from = moment(from).utc().format('YYYY-MM-DD');
  to = moment(to).utc().format('YYYY-MM-DD');
  return data.filter(
    row => from <= row.date && to >= row.date
  );
};

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
      if (rawString !== '') {
        const data = CSV.parse(rawString);
        const fieldNames = data.shift();
        return data.map(row =>
          row.reduce(
            (o, value, index) => ({ ...o, [fieldNames[index]]: value }),
            {},
          ),
        );
      } else {
        return [];
      }
    }

    getAggregation(base, aggregation) {
      if (
        base.includes('featured') ||
        base.includes('timeline') ||
        base.includes('aso_search')
      ) {
        aggregation = 'days';
      }
      return aggregation;
    }

    getFilename(base, aggregation, countriesSelected) {
      if (base.includes('aso_search') || base.includes('keywords')) {
        if (countriesSelected.length === 1) {
          return `${base}_${countriesSelected[0].value}_${this.getAggregation(
            base,
            aggregation,
          )}.csv`;
        }
      }
      return `${base}_${this.getAggregation(base, aggregation)}.csv`;
    }

    datesCompare() {
      const { fromCompareDate, toCompareDate } = this.props.params;
      return { from: fromCompareDate, to: toCompareDate };
    }

    update() {
      const aggregation = this.props.params.selectedAggregation.value;
      const countriesSelected = this.props.params.selectedCountries;
      dataSources.forEach(([filenameBase, dataName]) => {
        if (
          (!filenameBase.includes('aso_search') &&
            !filenameBase.includes('keywords')) ||
          (countriesSelected.length === 1 &&
            (filenameBase.includes('aso_search') ||
              filenameBase.includes('keywords')))
        ) {
          fetchData(
            this.getFilename(filenameBase, aggregation, countriesSelected),
            data =>
              this.setState({
                ['loaded' + dataName]: true,
                [dataName]: this.processData(data),
              }),
          );
        } else {
          this.setState({
            ['loaded' + dataName]: true,
            [dataName]: [],
          });
        }
      });
    }

    allLoaded() {
      return dataSources.map(
        ([_, dataName]) => this.state['loaded' + dataName],
      );
    }

    data = name => getRange(this.dates(), this.state[name]);

    dataIos = (name = 'dataIos') => getRange(this.dates(), this.state[name]);

    dataAndroid = (name = 'dataAndroid') =>
      getRange(this.dates(), this.state[name]);

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
