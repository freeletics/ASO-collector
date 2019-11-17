export default {
  dateFormat: 'YY/MM/DD',
  datePickerFormat: 'dd MMMM yyyy',
  filterDefaultPeriod: 30,
  filterDefaultCountriesAmount: 5,
  platformOptions: [
    { value: 'ios', label: 'IOS' },
    { value: 'android', label: 'Android' },
  ],
  aggregationOptions: [
    { value: 'days', label: 'Day' },
    { value: 'weeks', label: 'Week' },
    { value: 'months', label: 'Month' },
  ],
  countryOptions: [
    { value: 'us', label: 'USA' },
    { value: 'gb', label: 'Great Britain' },
    { value: 'de', label: 'Germany' },
    { value: 'fr', label: 'France' },
    { value: 'it', label: 'Italy' },
  ],
};
