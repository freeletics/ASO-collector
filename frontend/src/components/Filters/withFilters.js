import React from 'react';
import fetchData from '../../services/fetchData';

const withFilters = (WrappedComponent, dataSources) => {
  return class extends React.Component {
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

    processData(data) {
      const fieldNames = data.shift();
      return data.map(row =>
        row.reduce(
          (o, value, index) => ({ ...o, [fieldNames[index]]: value }),
          {},
        ),
      );
    }

    update() {
      const aggregation = this.props.params.selectedAggregation.value;
      dataSources.forEach(([filenameBase, dataName]) => {
        if (!this.state[dataName]) {
          fetchData(this.getFilename(filenameBase, aggregation), data =>
            this.setState({
              ['loaded' + dataName]: true,
              [dataName]: this.processData(data),
            }),
          );
        }
      });
    }

    getFilename(base, aggregation) {
      return `${base}_${aggregation}.csv`;
    }

    allLoaded() {
      return dataSources.map(
        ([_, dataName]) => this.state['loaded' + dataName],
      );
    }

    render() {
      return this.allLoaded().every(x => Boolean(x)) ? (
        <WrappedComponent
          {...this.props}
          dataAndroid={this.state.dataAndroid}
          dataIos={this.state.dataIos}
        />
      ) : null;
    }
  };
};

export default withFilters;
