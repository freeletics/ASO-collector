export const notDate = key => key !== 'date';

export const dateLabels = data => data.map(row => row.date);

export const avgList = values =>
  values.reduce((total, [_, value]) => sum(total, value), 0) / values.length;

export const avg = values =>
  values.reduce((total, value) => sum(total, value), 0) /
  values.filter(value => value).length;

export const sumList = values =>
  values.reduce((total, [_, value]) => sum(total, value), 0);

export const sum = (total, value) => total + Number(value);

export const getCountryFromKey = key => key.split('_')[0];

export const isCountrySelected = (props, country) =>
  !props.params.selectedCountries.length ||
  props.params.selectedCountries
    .map(option => option.value)
    .includes(getCountryFromKey(country));

export const getCountryCode = key => key.split(/_(.+)/)[0];

export const getPercent = (value, total) =>
  parseFloat(((value * 1.0) / total) * 100).toFixed(1);

export const formatPercent = value =>
  !isNaN(value) ? `${parseFloat(value).toFixed(2)}%` : 'N/A';

export const getFormatedPercent = (...args) => formatPercent(avg(getAvgs(...args)));

export const reduce = (props, data, filedName) =>
  getSums(props, data, filedName).reduce(sum, 0);

export const capitalize = s => {
  if (typeof s !== 'string') return '';
  return s.charAt(0).toUpperCase() + s.slice(1);
};

export const getReviewsDatasets = (props, data) => ({
  Average: {
    type: 'line',
    yAxisID: 'B',
    data: getValues(props, data, 'average', avgList),
  },
  '1 star': getValues(props, data, 'star_1', sumList),
  '2 stars': getValues(props, data, 'star_2', sumList),
  '3 stars': getValues(props, data, 'star_3', sumList),
  '4 stars': getValues(props, data, 'star_4', sumList),
  '5 stars': getValues(props, data, 'star_5', sumList),
});

export const getAvg = (props, data) =>
  avg(getValues(props, data, 'average', avgList).filter(value => !isNaN(value)));

export function getCountriesAvg(props, data) {
  const datasets = {};
  data.forEach(row =>
    Object.entries(row).forEach(([key, value]) => {
      const country = getCountryCode(key);
      if (key.includes('average') && isCountrySelected(props, country)) {
        datasets[country] = datasets[country] ? datasets[country] : [];
        datasets[country].push(value);
      }
    }),
  );
  return datasets;
}

export function getValues(props, data, valueName, func) {
  return data.map(row =>
    func(
      Object.entries(row)
        .filter(
          ([key, value]) =>
            isCountrySelected(props, getCountryCode(key)) &&
            key.includes(valueName) &&
            value,
        )
        .filter(arr => arr.length),
    ),
  );
}

const condition = (props, key, type) =>
  notDate(key) &&
  key
    .split('_')
    .slice(1)
    .join('_') === type &&
  isCountrySelected(props, key);

export function getSums(props, data, type) {
  return data.map(row =>
    Object.entries(row).reduce((sum, [key, value]) => {
      return condition(props, key, type) ? sum + Number(value) : sum;
    }, 0),
  );
}

export function getAvgs(props, data, type) {
  return data.map(row =>
    avgList(Object.entries(row).filter(([key, _]) => condition(props, key, type))),
  );
}

export const setDefault = (obj, key, defaultValue, value) => {
  obj[key] = obj[key] ? obj[key] : defaultValue;
  obj[key].push(value);
};

export function getKeywords(data) {
  const datasets = {};
  data.forEach(row =>
    Object.entries(row).forEach(([key, value]) => {
      if (notDate(key)) {
        setDefault(datasets, key, [], value);
      }
    }),
  );
  return datasets;
}

export function getCountries(props, data, type) {
  const datasets = {};
  data.forEach(row =>
    Object.entries(row).forEach(([key, value]) => {
      if (condition(props, key, type)) {
        const country = getCountryFromKey(key);
        setDefault(datasets, country, [], value);
      }
    }),
  );
  return datasets;
}
