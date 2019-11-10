import Page from '../components/Page';
import React from 'react';
import OverviewFilters from '../components/Filters/OverviewFilters';
import Reviews from '../components/Boxes/Reviews';
import Rating from '../components/Boxes/Ratings';
import RatingComparison from '../components/Boxes/RatingComparison';
import ConversionRateTable from '../components/Boxes/ConversionRateTable';
import RankingComparison from '../components/Boxes/RankingComparison'
import ChangeTimeline from '../components/Boxes/ChangesTimeline'

class DashboardPage extends React.Component {
  render() {
    return (
      <Page className="DashboardPage" title="Regional">
        <OverviewFilters>
          <RankingComparison></RankingComparison>
          <ConversionRateTable></ConversionRateTable>
          <RatingComparison></RatingComparison>
          <Rating></Rating>
          <Reviews></Reviews>
          <ChangeTimeline></ChangeTimeline>
        </OverviewFilters>
      </Page>
    );
  }
}
export default DashboardPage;
