const moment = require("moment");
const fs = require("fs");
const argv = require("yargs").argv;
const { getSearchAdsData } = require("./search_ads");
const { getAnalyticsData, getConnection } = require("./analytics");

const USERNAME = argv.username;
const PASSWORD = argv.password;
const APP_ID = argv.id;
const SEARCH_ADS_CREDENTIALS = argv.certificates;
const OUTPUT = argv.output;
const from = argv.from;
const to = argv.to;

getEverythingForPeriod(from, to);

// TODO: dodac logowanie
// TODO: dodac ladowanie pliku z raw data i nie powtarzanie requestow
async function getEverythingForPeriod(from, to) {
  const connection = getConnection(USERNAME, PASSWORD);
  const startDate = moment.utc(from, "YYYY-MM-DD");
  const weekStartDate = startDate.clone();
  const monthStartDate = startDate.clone();
  const endDate = moment.utc(to, "YYYY-MM-DD");
  const data = {}
  while (monthStartDate <= endDate) {
    const startOfMonth = monthStartDate.clone().startOf("month");
    const endOfMonth = startOfMonth.clone().endOf("month");
    await getAppStoreData(data, startOfMonth, endOfMonth, "month", connection);
    monthStartDate.add(1, "month");
  }
  while (weekStartDate <= endDate) {
    const weekMonday = weekStartDate.clone().day("Monday");
    const weekSunday = weekMonday.clone().add(1, 'week').subtract(1, 'day');
    await getAppStoreData(data, weekMonday, weekSunday, "week", connection);
    weekStartDate.add(1, "week");
  } 
  while (startDate <= endDate) {
    await getAppStoreData(data, startDate, startDate, "day", connection);
    startDate.add(1, "day");
  }
}

async function getAppStoreData(data, from, to, aggregation, connection) {
  await getAnalyticsData(data, from, to, aggregation, APP_ID, connection);
  await getSearchAdsData(data, from, to, aggregation, SEARCH_ADS_CREDENTIALS);
  fs.writeFileSync(OUTPUT, JSON.stringify(data, null, 2), "utf-8");
}

