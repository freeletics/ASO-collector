const moment = require("moment");
const countries = require("./countries");
const itc = require("itunesconnectanalytics");

const Itunes = itc.Itunes;
const AnalyticsQuery = itc.AnalyticsQuery;

const REQUEST_DELAY = 10000;
const MEASURE_IDS = [
  "impressions",
  "impressionsUnique",
  "pageViewUnique",
  "pageViews",
  "units"
];

const GROUP_PARAMS = [{}, { group: { dimension: itc.dimension.sourceType } }];

let connection;

function getConnection(username, password) {
  if (!connection) {
    connection = new Itunes(username, password, {
      errorCallback: e => {
        console.log("Error logging in: " + e);
      },
      successCallback: d => {
        console.log("Logged in");
      }
    });
  }
  return connection;
}

function getData(connection, query, country, date, aggregation) {
  return new Promise(function(resolve, reject) {
    setTimeout(() => {
      connection.request(query, async function(error, data) {
        if (data.results) {
          try {
            resolve(getPartialData(data.results, country, date, aggregation));
          } catch (e) {
            console.error(e);
            reject(e);
          }
        } else {
          reject("No result");
        }
      });
    }, REQUEST_DELAY);
  });
}

function getPartialData(results, country, momentDate, aggregation) {
  let date = momentDate.toDate();
  const partialData = { country, date, aggregation };
  results.forEach(result => {
    date = getDateFromResult(result);
    partialData.date = date;
    if (!result.group) {
      partialData[result.totals.key + "All"] = getDataFromResult(result);
    } else if (result.group.key == "Other") {
      partialData[result.totals.key + "Browsers"] = getDataFromResult(result);
    } else if (result.group.key == "Search") {
      partialData[result.totals.key + "Searchers"] = getDataFromResult(result);
    }
  });
  return partialData;
}

function getDateFromResult(result) {
  return moment.utc(result.data[0].date).toDate();
}

function getDataFromResult(result) {
  return result.data[0][result.totals.key];
}

async function getAnalyticsData(
  data,
  startMoment,
  endMoment,
  aggregation,
  appId,
  connection
) {
  const queryParamList = getQueryParamList(countries);
  let queryList = queryParamList
    .filter(params => params.countryAppStoreCode)
    .map(params => {
      return createQuery(params, startMoment, endMoment, aggregation, appId);
    });
  while (queryList.length > 0) {
    const queryRecord = queryList.shift();
    const { country, query } = queryRecord;
    try {
      console.log("Saving data for country", country);
      const key = [startMoment.format("YYYY-MM-DD"), country, aggregation]
      data[key] = data[key] || {}
      Object.assign(data[key], await getData(
        connection,
        query,
        country,
        startMoment,
        aggregation
      ));
    } catch (e) {
      console.error("Saving data failed", country, e);
      queryList.push(queryRecord);
    }
  }
}

function getQueryParamList(countries) {
  const queryParamList = [];
  Object.entries(countries).forEach(([countryCode, country]) => {
    MEASURE_IDS.forEach(measureId => {
      GROUP_PARAMS.forEach(group => {
        queryParamList.push({
          countryCode,
          measureId,
          group,
          countryAppStoreCode: country.appStoreCode
        });
      });
    });
  });
  return queryParamList;
}

function createQuery(params, start, end, aggregation, appId) {
  return {
    date: start,
    country: params.countryCode,
    query: AnalyticsQuery.metrics(appId, {
      measures: itc.measures[params.measureId],
      frequency: itc.frequency[`${aggregation}s`],
      ...params.group,
      dimensionFilters: [
        {
          dimensionKey: itc.dimensionFilterKey.territory,
          optionKeys: [params.countryAppStoreCode]
        }
      ]
    }).date(start, end)
  };
}

module.exports = {
  getConnection,
  getAnalyticsData
};
