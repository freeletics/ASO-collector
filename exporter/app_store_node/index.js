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
const SEARCH_ADS_ONLY = argv.search_ads_only;
const from = argv.from;
const to = argv.to;

getEverythingForPeriod(from, to);

async function getEverythingForPeriod(from, to) {
  const connection = getConnection(USERNAME, PASSWORD);
  console.log(`From: ${from}, to: ${to}`);
  const startDate = moment.utc(from, "YYYY-MM-DD");
  const weekStartDate = startDate.clone();
  const monthStartDate = startDate.clone();
  const endDate = moment.utc(to, "YYYY-MM-DD");
  const data = readRawData();
  console.log("Getting data for month");
  while (monthStartDate <= endDate) {
    const startOfMonth = monthStartDate.clone().startOf("month");
    console.log(startOfMonth);
    const endOfMonth = startOfMonth.clone().endOf("month");
    await getAppStoreData(data, startOfMonth, endOfMonth, "month", connection);
    monthStartDate.add(1, "month");
  }
  console.log("Getting data for week");
  while (weekStartDate <= endDate) {
    const weekMonday = weekStartDate.clone().day("Monday");
    console.log(weekMonday);
    const weekSunday = weekMonday
      .clone()
      .add(1, "week")
      .subtract(1, "day");
    await getAppStoreData(data, weekMonday, weekSunday, "week", connection);
    weekStartDate.add(1, "week");
  }
  console.log("Getting data for day");
  while (startDate <= endDate) {
    console.log(startDate);
    await getAppStoreData(data, startDate, startDate, "day", connection);
    startDate.add(1, "day");
  }
}

function readRawData() {
  try {
    const contents = fs.readFileSync(OUTPUT);
    return JSON.parse(contents);
  } catch (e) {
    console.log(e);
    return {};
  }
}
async function getAppStoreData(data, from, to, aggregation, connection) {
  if (!SEARCH_ADS_ONLY) {
    await getAnalyticsData(data, from, to, aggregation, APP_ID, connection);
  }
  await getSearchAdsData(data, from, to, aggregation, SEARCH_ADS_CREDENTIALS);
  fs.writeFileSync(OUTPUT, JSON.stringify(data, null, 2), "utf-8");
}
