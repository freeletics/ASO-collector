import React from 'react';
import PropTypes from '../../utils/propTypes';
import { Card, CardText, CardTitle } from 'reactstrap';
import Typography from '../Typography';

const getPerformance = (value, valueCompare) => {
  if (value && valueCompare) {
    return (valueCompare - value) * 100.0 / valueCompare;
  } else {
    return null;
  }
};

const NumberWidget = ({
  title,
  subtitle,
  number,
  numberCompare,
  color,
  ...restProps
}) => {
  const performance = getPerformance(number, numberCompare);
  const performanceColor = performance >= 0 ? 'success' : 'danger';
  return (
    <Card body {...restProps}>
      <div className="d-flex justify-content-between">
        <CardText tag="div">
          <Typography className="mb-0">
            <strong>{title}</strong>
          </Typography>
          <Typography className="mb-0 text-muted small">{subtitle}</Typography>
        </CardText>
        <CardTitle className={`ml-3 text-${performanceColor}`}>
          <h1>{number !== 0 ? parseFloat(number).toFixed(1) : 'N/A'}</h1>
          {(performance || performance === 0) && (
            <span className={`text-${performanceColor}`}>
              {performance >= 0 && '+'}
              {parseFloat(performance).toFixed(1)}%
            </span>
          )}
        </CardTitle>
      </div>
    </Card>
  );
};

NumberWidget.propTypes = {
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string,
  number: PropTypes.oneOfType([
    PropTypes.string.isRequired,
    PropTypes.number.isRequired,
  ]),
  color: PropTypes.oneOf([
    'primary',
    'secondary',
    'success',
    'info',
    'warning',
    'danger',
    'light',
    'dark',
  ]),
};

NumberWidget.defaultProps = {
  title: '',
  subtitle: '',
  number: 0,
  color: 'primary',
};

export default NumberWidget;
