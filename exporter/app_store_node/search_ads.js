const axios = require("axios");
const https = require("https");
const fs = require("fs");

const REQUEST_DELAY = 500;
const SEARCH_ADS_API_BASE = "https://api.searchads.apple.com/api/v2";
const CAMPAIGN_GROUP_ENDPOINT = "/acls";
const REPORT_ENDPOINT = "/reports/campaigns";

async function getSearchAdsData(
  data,
  startDate,
  endDate,
  aggregation,
  certificateDirectory
) {
  const authAxios = createHttpsAgent(certificateDirectory);
  const campaignGroups = await getCampaignGroups(authAxios);
  const searchAdsData = {};
  while (campaignGroups.length > 0) {
    const group = campaignGroups.shift();
    try {
      console.log("Saving data for group", group.orgName);
      (await getData(
        authAxios,
        group.orgId,
        startDate,
        endDate,
        aggregation
      )).forEach(campaignData => {
        const key = [
          startDate.format("YYYY-MM-DD"),
          campaignData.country,
          aggregation
        ];
        searchAdsData[key] = searchAdsData[key] || initSearchAds();
        searchAdsData[key] = addSearchAds(searchAdsData[key], campaignData);
      });
    } catch (e) {
      console.error("Saving data failed", group.orgName, e);
    }
  }
  mergeData(data, searchAdsData);
}

function mergeData(data, searchAdsData) {
  Object.keys(data).forEach(key => {
    Object.assign(data[key], searchAdsData[key]);
  });
}

function initSearchAds() {
  return {
    tapsSearchAds: 0,
    impressionsSearchAds: 0,
    downloadsSearchAds: 0
  };
}

function addSearchAds(a, b) {
  return {
    tapsSearchAds: a.tapsSearchAds + b.tapsSearchAds,
    impressionsSearchAds: a.impressionsSearchAds + b.impressionsSearchAds,
    downloadsSearchAds: a.downloadsSearchAds + b.downloadsSearchAds
  };
}

function getData(authAxios, ordId, startDate, endDate, aggregation) {
  return new Promise(function(resolve, reject) {
    setTimeout(async () => {
      try {
        resolve(
          await getDataForCampaignGroup(
            authAxios,
            ordId,
            startDate,
            endDate,
            aggregation
          )
        );
      } catch (e) {
        console.error(e);
        reject();
      }
    }, REQUEST_DELAY);
  });
}

async function getCampaignGroups(httpsAgent) {
  const response = await httpsAgent.get(
    `${SEARCH_ADS_API_BASE}${CAMPAIGN_GROUP_ENDPOINT}`
  );
  return response.data.data.map(org => ({
    orgName: org.orgName,
    orgId: org.orgId
  }));
}

async function getDataForCampaignGroup(
  httpsAgent,
  groupId,
  startDate,
  endDate,
  aggregation,
  certificateDirectory
) {
  const response = await httpsAgent.post(
    `${SEARCH_ADS_API_BASE}${REPORT_ENDPOINT}`,
    getRequestPayload(startDate, endDate),
    getHeaders(groupId, certificateDirectory)
  );
  return response.data.data.reportingDataResponse.row.map(campaign => ({
    aggregation,
    country: campaign.metadata.countriesOrRegions[0].toLowerCase(),
    date: startDate.toDate(),
    tapsSearchAds: campaign.total.taps,
    impressionsSearchAds: campaign.total.impressions,
    downloadsSearchAds: campaign.total.newDownloads
  }));
}

function getRequestPayload(startDate, endDate) {
  const format = "YYYY-MM-DD";
  return {
    endTime: endDate.format(format),
    startTime: startDate.format(format),
    returnGrandTotals: true,
    returnRecordsWithNoMetrics: true,
    returnRowTotals: true,
    selector: {
      orderBy: [{ field: "localSpend", sortOrder: "DESCENDING" }],
      pagination: { offset: 0, limit: 500 }
    }
  };
}

function createHttpsAgent(certificateDirectory) {
  const httpsAgent = new https.Agent({
    rejectUnauthorized: false,
    cert: fs.readFileSync(`${certificateDirectory}/search-ads.pem`),
    key: fs.readFileSync(`${certificateDirectory}/search-ads.key`)
  });
  return axios.create({
    httpsAgent
  });
}

function getHeaders(groupId) {
  return {
    headers: {
      Authorization: `orgId=${groupId}`,
      "Content-Type": "application/json"
    }
  };
}

module.exports = { getSearchAdsData };
