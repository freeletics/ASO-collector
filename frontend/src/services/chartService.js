import { defaultColors } from '../config/colors';

function getColor(colors, index) {
  return colors[index % colors.length];
}

export function getChartData(labels, data, options = defaultColors) {
  if (validateInput(labels, data)) {
    return {};
  } else {
    options = parseOptions(options);
    const datasets = getDatasets(options, data);
    return { labels, datasets };
  }
}

function getDatasets(options, data) {
  return Object.entries(data).map(([label, data], index) => {
    let datasetOptions = Array.isArray(data) ? { data } : { ...data };
    datasetOptions.data = datasetOptions.data.map(point => {
      const pointFixed = parseFloat(point).toFixed(2);
      return options.percent || datasetOptions.percent
        ? (parseFloat(point).toFixed(4) * 100).toFixed(2)
        : pointFixed;
    });
    return {
      label,
      backgroundColor: getColor(options.colors, index),
      borderColor: getColor(options.colors, index),
      borderWidth: 1,
      fill: false,
      ...options,
      ...datasetOptions,
    };
  });
}

function parseOptions(options) {
  return Array.isArray(options)
    ? { colors: options }
    : { ...options, colors: options.colors || defaultColors };
}

function validateInput(labels, data) {
  return !labels || !data || Object.keys(data).length === 0;
}

export function getDatasetColors(datasetLength, inputColors = defaultColors) {
  const colors = Array(datasetLength).fill(inputColors);
  return {
    backgroundColor: [...[].concat.apply([], colors)],
    borderColor: [...[].concat.apply([], colors)],
  };
}

export const defaultOptions = {
  tooltips: {
    position: 'nearest',
  },
  responsive: true,
  legend: {
    display: true,
  },
  scales: {
    xAxes: [
      {
        stacked: true,
        display: true,
      },
    ],
    yAxes: [
      {
        stacked: true,
        display: true,
      },
    ],
  },
};

export const ratingScaleOption = {
  legend: {
    display: false,
  },
  scales: {
    yAxes: [
      {
        ticks: {
          max: 5,
          min: 0,
        },
      },
    ],
  },
};

export const rankingScaleOption = {
  legend: {
    display: false,
  },
  scales: {
    yAxes: [
      {
        ticks: {
          reverse: true,
        },
      },
    ],
  },
};

export const starsConfig = {
  ...defaultOptions,
  scales: {
    yAxes: [
      {
        id: 'A',
        type: 'linear',
        position: 'left',
        stacked: true,
        display: true,
        ticks: {
          min: 0,
        },
      },
      {
        id: 'B',
        type: 'linear',
        position: 'right',
        ticks: {
          max: 5,
          min: 0,
        },
      },
    ],
    xAxes: [
      {
        stacked: true,
        display: true,
      },
    ],
  },
};
