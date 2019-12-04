import React from 'react';
import { getChartData } from '../../services/chartService';

export const MAX_NUMBER_ENTITY_LABELS = 5;

const CountryChart = ({ component, data, options, datasetOption }) => {
  const Chart = component;
  datasetOption = datasetOption || {};
  return (
    <Chart
      data={getChartData(data.labels, data.datasets, datasetOption)}
      options={{
        ...options,
        legend: {
          display:
            options.display || Object.entries(data.datasets).length <= MAX_NUMBER_ENTITY_LABELS,
        },
      }}
    />
  );
};

export default CountryChart;
