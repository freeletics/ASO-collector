import React from 'react';
import NumberFormat from 'react-number-format';

const getPercent = (value, total) =>
  parseFloat(((value * 1.0) / total) * 100).toFixed(1);

export default ({ title, field, fieldTotal, data }) => {
  return (
    <div>
      {title}:
      <span className="float-right">
        {getPercent(data[field], data[fieldTotal])}% (
        <NumberFormat
          displayType={'text'}
          thousandSeparator={true}
          value={data[field]}
        ></NumberFormat>
        )
      </span>
    </div>
  );
};
