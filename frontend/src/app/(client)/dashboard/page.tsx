import React from 'react';

const page = () => {
  const url =
    'https://app.powerbi.com/reportEmbed?reportId=8ae8e760-1471-495f-a032-dc2e9bfd8ec7&autoAuth=true&ctid=2dff09ac-2b3b-4182-9953-2b548e0d0b39';
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
      }}
    >
      <iframe title="Tableau Dashboard" width="80%" height="100%" src={url} />
    </div>
  );
};

export default page;
