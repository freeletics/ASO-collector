import moment from 'moment';
import config from '../config';

export default function queryParams(params) {
  const countriesFilter = getListParam('countries', params.selectedCountries);
  const platformFilter = getListParam('platforms', params.selectedPlatforms);
  const aggregationFilter = getParam('aggregation', params.selectedAggregation);
  const to = getDateParam('to', params.toDate);
  const from = getDateParam('from', params.fromDate);
  const fromCompare = getDateParam('fromCompare', params.fromCompareDate);
  const toCompare = getDateParam('toCompare', params.toCompareDate);
  return `?${countriesFilter}${platformFilter}${to}${from}${fromCompare}${toCompare}${aggregationFilter}`;
}

function getParam(name, param) {
  return param ? `&${name}=${param.value}` : '';
}

function getListParam(name, param) {
  let list =
    param && param.length && typeof param[0] !== 'string'
      ? param.map(option => option.value)
      : param;
  return param && param.length ? `&${name}=${list.join(',')}` : '';
}

function getDateParam(name, param) {
  return param ? `&${name}=${moment(param).format(config.dateFormat)}` : '';
}
