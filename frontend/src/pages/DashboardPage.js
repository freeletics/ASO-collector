import Page from '../components/Page';
import React from 'react';
import OverviewFilters from '../components/Filters/OverviewFilters';
import Installs from '../components/Boxes/Installs';
import Reviews from '../components/Boxes/Reviews';
import Rating from '../components/Boxes/Ratings';
import RatingComparison from '../components/Boxes/RatingComparison';
import FeaturingList from '../components/Boxes/FeaturingList'

class DashboardPage extends React.Component {
  render() {
    return (
      <Page className="DashboardPage" title="Regional">
        <OverviewFilters>
          <Installs></Installs>
          <FeaturingList></FeaturingList>
          <RatingComparison></RatingComparison>
          <Rating></Rating>
          <Reviews></Reviews>
        </OverviewFilters>
      </Page>
    );
  }
}
export default DashboardPage;
