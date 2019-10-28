import Page from '../components/Page';
import React from 'react';
import OverviewFilters from '../components/Filters/OverviewFilters';

class DashboardPage extends React.Component {
  render() {
    return (
      <Page className="DashboardPage" title="Regional">
        <OverviewFilters>
        </OverviewFilters>
      </Page>
    );
  }
}
export default DashboardPage;
