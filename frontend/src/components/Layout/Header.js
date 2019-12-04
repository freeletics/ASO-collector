import React from 'react';
import { MdClearAll } from 'react-icons/md';
import { Button, Nav, Navbar, NavItem } from 'reactstrap';
import { authenticationService } from '../../services/authService';
import bn from '../../utils/bemnames';

const bem = bn.create('header');

class Header extends React.Component {
  handleSidebarControlButton = event => {
    event.preventDefault();
    event.stopPropagation();

    document.querySelector('.cr-sidebar').classList.toggle('cr-sidebar--open');
  };

  logout() {
    authenticationService.logout();
  }

  render() {
    return (
      <Navbar light expand className={bem.b('bg-white')}>
        <Nav navbar className="mr-2">
          <Button outline onClick={this.handleSidebarControlButton}>
            <MdClearAll size={25} />
          </Button>
        </Nav>
        <Nav navbar className={bem.e('nav-right')}>
          <NavItem className="d-inline-flex">
            <Button outline color="secondary" onClick={this.logout}>
              Logout
            </Button>
          </NavItem>
        </Nav>
      </Navbar>
    );
  }
}

export default Header;
