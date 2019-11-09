import Page from '../components/Page';
import React from 'react';
import OverviewFilters from '../components/Filters/OverviewFilters';
import Downloads from '../components/Boxes/Downloads'
import Impressions from '../components/Boxes/Impressions'
import PageViews from '../components/Boxes/PageViews'
import Keywords from '../components/Boxes/Keywords'

class DashboardPage extends React.Component {
  render() {
    return (
      <Page className="DashboardPage" title="Detail">
        <OverviewFilters>
          <Keywords></Keywords>
          <PageViews></PageViews>
          <Impressions></Impressions>
          <Downloads></Downloads>
        </OverviewFilters>
      </Page>
    );
  }
}
export default DashboardPage;
