import Page from '../components/Page';
import React from 'react';
import OverviewFilters from '../components/Filters/OverviewFilters';
import Downloads from '../components/Boxes/Downloads'
import Impressions from '../components/Boxes/Impressions'
import PageViews from '../components/Boxes/PageViews'
import Keywords from '../components/Boxes/Keywords'
import Installs from '../components/Boxes/Installs';
import Reviews from '../components/Boxes/Reviews';
import Rating from '../components/Boxes/Ratings';
import RatingComparison from '../components/Boxes/RatingComparison';
import InstallsDoughnut from '../components/Boxes/InstallsDoughnut';
import NewDownloads from '../components/Boxes/NewDownloads';
import ConversionRateTable from '../components/Boxes/ConversionRateTable';
import RankingComparison from '../components/Boxes/RankingComparison'

class DashboardPage extends React.Component {
  render() {
    return (
      <Page className="DashboardPage" title="Detail">
        <OverviewFilters>
          <RankingComparison></RankingComparison>
          <ConversionRateTable></ConversionRateTable>
          <InstallsDoughnut></InstallsDoughnut>
          <Installs></Installs>
          <NewDownloads></NewDownloads>
          <Downloads></Downloads>
          <PageViews></PageViews>
          <Impressions></Impressions>
          <RatingComparison></RatingComparison>
          <Rating></Rating>
          <Reviews></Reviews>
          <Keywords></Keywords>
        </OverviewFilters>
      </Page>
    );
  }
}
export default DashboardPage;
