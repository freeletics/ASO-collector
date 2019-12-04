import React from 'react';

import { Navbar, Nav, NavItem } from 'reactstrap';

import SourceLink from '../Widget/SourceLink';

const Footer = () => {
  return (
    <Navbar>
      <Nav navbar>
        <NavItem>
          <SourceLink>Freeletics</SourceLink>
        </NavItem>
      </Nav>
    </Navbar>
  );
};

export default Footer;
