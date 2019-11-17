import React from 'react';
import moment from 'moment';
import { Wrapper } from './withFilters';
import fetchData from '../../services/fetchData';

const getRange = ({ from, to }, data) =>
  data.update_data ? data.update_data.filter(
    item => from <= moment(item[0]).toDate() && to >= moment(item[0]).toDate(),
  ) : [];

const withFiltersTimeline = (WrappedComponent, ...dataSources) => {
  return class extends Wrapper {
    processData(data) {
      return data ? JSON.parse(data) : {}
    }

    getCountry() {
      return (
        this.props.params.selectedCountries.length &&
        this.props.params.selectedCountries[0].value
      );
    }

    update() {
      dataSources.forEach(([filenameBase, dataName]) => {
        fetchData(this.getFilename(filenameBase), data =>
          this.setState({
            ['loaded' + dataName]: true,
            [dataName]: this.processData(data),
          }),
        );
      });
    }

    getFilename(base) {
      return `${base}_${this.getCountry()}_days.json`;
    }

    allLoaded() {
      return dataSources.map(([_, dataName]) => this.state['loaded' + dataName]);
    }

    data = name => getRange(this.dates(), this.state[name]);

    render() {
      return this.allLoaded().every(x => Boolean(x)) ? (
        <WrappedComponent {...this.props} data={this.data} country={this.getCountry()}/>
      ) : null;
    }
  };
};

export default withFiltersTimeline;
