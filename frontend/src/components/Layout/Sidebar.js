import React from 'react';
import {
  MdDashboard,
  MdLocalAirport,
  MdAcUnit,
  MdExtension,
  MdKeyboardArrowDown,
} from 'react-icons/md';
import { NavLink } from 'react-router-dom';
import {
  Collapse,
  Nav,
  Navbar,
  NavItem,
  NavLink as BSNavLink,
} from 'reactstrap';
import bn from '../../utils/bemnames';

const navItems = [];

const navAso = [
  { to: '/', name: 'regional', exact: true, Icon: MdDashboard },
  { to: '/detail', name: 'detail', exact: true, Icon: MdLocalAirport },
];

const bem = bn.create('sidebar');

class Sidebar extends React.Component {
  state = {
    isOpenAso: true,
  };

  handleClick = name => () => {
    this.setState(prevState => {
      const isOpen = prevState[`isOpen${name}`];

      return {
        [`isOpen${name}`]: !isOpen,
      };
    });
  };

  render() {
    return (
      <aside className={bem.b()}>
        <div className={bem.e('content')}>
          <Navbar>
            <span className="navbar-brand d-flex text-white">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="52"
                height="30.5"
                viewBox="0 0 52.01 30.56"
              >
                <path
                  fill="#fff"
                  d="M37.73 14.78c-.25-.07-.45-.14-.46-.15-.02-.03-2.2-8.47-2.19-8.49 0-.01.65-.65 1.44-1.43l1.56-1.52.12-.11.01 5.92c0 4.72 0 5.91-.01 5.91-.02 0-.23-.06-.47-.13zm4.59 1.28l-3.41-.95-.01-6.35-.01-6.36 1.22-1.2C40.79.55 41.34 0 41.35 0c.01 0 1.92.53 4.24 1.17l4.23 1.18 1.09 4.25c.6 2.34 1.09 4.25 1.09 4.26-.01.02-6.26 6.15-6.28 6.15 0 0-1.53-.43-3.4-.95zM26.45 11.1l-.01-6.15 7.2-.01v2.88l-1.9.01-1.9.01v1.72h3.6l.01 1.39.01 1.39h-3.61v1.98h3.8v1.47l.01 1.47-7.2.01-.01-6.17zm-8.32 0l-.01-6.15 7.2-.01v2.88H21.5v1.72h3.61v2.78H21.5v1.98h3.82v2.94l-7.2.01.01-6.15zm-5.86-.82c.3-.08.52-.2.7-.38.26-.28.38-.66.34-1.12-.02-.19-.05-.32-.12-.47-.17-.36-.46-.56-.94-.65-.12-.02-.22-.03-.5-.02-.19 0-.39.01-.44.02l-.1.01v2.64l.06.01c.04 0 .08.01.11.01h.39c.31-.01.36-.01.5-.05zm-4.46.81L7.8 4.92l.05-.01c.06-.01.55-.03 1.21-.06.72-.03 3.59-.03 3.87 0 1.58.15 2.62.6 3.26 1.4.51.66.76 1.59.71 2.65-.06 1.21-.69 2.3-1.66 2.89-.14.09-.4.21-.5.25-.03.01-.06.02-.06.03 0 .01.07.12.16.26.28.42.49.77.95 1.56L17 15.94c.42.71.76 1.29.76 1.3 0 .01-.92.01-2.05.02h-2.06l-1.15-2.25-1.16-2.25h-.13v4.5h-3.4v-6.17zm-7.8.03L0 4.97l7.02-.01v2.91H3.4v1.99h3.42v2.78H3.4v4.62H0l.01-6.14zm25.38 19.26c-.01-.01-.01-2.77-.02-6.15l-.01-6.14h3.39l.01 12.3h-1.69c-.91 0-1.67 0-1.68-.01zM7.88 24.26l-.01-6.15 7.2-.01v2.87h-3.8v1.74h3.61v2.78h-3.61v1.98h3.8v2.94l-7.2.01.01-6.16zm-7.86.01l-.01-6.15H3.4l.01 9.27h3.38v3.03l-6.77.01v-6.16zm18.57 1.47v-4.69h-2.66v-2.91l8.71-.01v2.91h-2.66l.01 9.38H18.6l-.01-4.68zm16.04 4.75c-1.35-.09-2.47-.48-3.31-1.16a4.76 4.76 0 0 1-.6-.59c-.7-.83-1.11-1.92-1.24-3.3-.03-.32-.03-1.3.01-1.64.1-1.06.32-1.88.71-2.67.3-.6.61-1.05 1.06-1.5.43-.43.84-.73 1.39-1.01.71-.36 1.45-.56 2.38-.65.5-.05 1.26-.04 1.87.03.4.04 1.21.19 1.24.23.01 0-.07.7-.18 1.53-.16 1.24-.2 1.52-.21 1.52-.01 0-.12-.03-.25-.06-.85-.2-1.74-.26-2.29-.16-.89.17-1.52.76-1.82 1.67-.07.23-.13.47-.17.76-.04.27-.04 1.02 0 1.34.1.87.34 1.46.77 1.89.47.47 1.13.69 2.03.66.54-.02 1.11-.11 1.55-.26.08-.03.16-.06.18-.06.03 0 .04.07.23 1.5l.2 1.5s-.65.1-1.44.21c-1.41.2-1.44.21-1.68.2-.13.03-.32.02-.43.02zm5.48-.06c-.67-.07-1.22-.13-1.23-.13-.01-.01.17-3.04.17-3.05 0 0 .07.01.16.04.8.24 1.8.39 2.51.37.17 0 .34-.02.4-.03.49-.1.81-.35.88-.7.01-.05.01-.14.01-.22-.02-.38-.25-.65-.77-.89-.2-.09-.33-.15-.83-.33-1.16-.42-1.63-.69-2.1-1.15-.19-.19-.31-.34-.44-.56-.39-.66-.55-1.68-.39-2.61.29-1.74 1.72-2.89 3.93-3.17.4-.05.64-.06 1.12-.06.69 0 1.37.05 2.08.16l.16.02-.01.12c0 .06-.05.71-.09 1.44l-.09 1.33s-.13-.02-.28-.06c-.64-.16-1.15-.23-1.71-.24-.5-.02-.81.03-1.08.16-.15.07-.31.21-.37.33-.12.22-.11.52.02.73.06.09.22.25.35.33.16.11.56.29 1.02.48.61.24.83.34 1.14.49.69.35 1.13.71 1.46 1.21.26.37.4.77.48 1.3.03.22.04.82.01 1.06-.17 1.36-.96 2.46-2.23 3.12-.73.37-1.53.58-2.49.65-.37 0-.52-.01-1.79-.14z"
                ></path>
              </svg>
            </span>
          </Navbar>
          <Nav vertical>
            <NavItem
              className={bem.e('nav-item')}
              onClick={this.handleClick('Aso')}
            >
              <BSNavLink className={bem.e('nav-item-collapse')}>
                <div className="d-flex">
                  <MdExtension className={bem.e('nav-item-icon')} />
                  <span className=" align-self-start">ASO</span>
                </div>
                <MdKeyboardArrowDown
                  className={bem.e('nav-item-icon')}
                  style={{
                    padding: 0,
                    transform: this.state.isOpenAso
                      ? 'rotate(0deg)'
                      : 'rotate(-90deg)',
                    transitionDuration: '0.3s',
                    transitionProperty: 'transform',
                  }}
                />
              </BSNavLink>
            </NavItem>
            <Collapse isOpen={this.state.isOpenAso}>
              {navAso.map(({ to, name, exact, Icon }, index) => (
                <NavItem key={index} className={bem.e('nav-item')}>
                  <BSNavLink
                    id={`navItem-${name}-${index}`}
                    className="text-uppercase"
                    tag={NavLink}
                    to={to}
                    activeClassName="active"
                    exact={exact}
                  >
                    <Icon className={bem.e('nav-item-icon')} />
                    <span className="">{name}</span>
                  </BSNavLink>
                </NavItem>
              ))}
            </Collapse>
            {navItems.map(({ to, name, exact, Icon }, index) => (
              <NavItem key={index} className={bem.e('nav-item')}>
                <BSNavLink
                  id={`navItem-${name}-${index}`}
                  className="text-uppercase"
                  tag={NavLink}
                  to={to}
                  activeClassName="active"
                  exact={exact}
                >
                  <Icon className={bem.e('nav-item-icon')} />
                  <span className="">{name}</span>
                </BSNavLink>
              </NavItem>
            ))}
          </Nav>
        </div>
      </aside>
    );
  }
}

export default Sidebar;
