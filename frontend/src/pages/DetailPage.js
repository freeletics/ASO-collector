import Page from '../components/Page';
import React from 'react';
import OverviewFilters from '../components/Filters/OverviewFilters';
import Downloads from '../components/Boxes/Downloads'

class DashboardPage extends React.Component {
  render() {
    return (
      <Page className="DashboardPage" title="Detail">
        <OverviewFilters>
          <Downloads></Downloads>
        </OverviewFilters>
      </Page>
    );
  }
}
export default DashboardPage;
