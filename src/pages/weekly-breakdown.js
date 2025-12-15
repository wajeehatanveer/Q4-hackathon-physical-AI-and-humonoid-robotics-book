import React from 'react';
import Layout from '@theme/Layout';

function WeeklyBreakdown() {
  return (
    <Layout
      title="Weekly Breakdown"
      description="This is a protected page showing weekly breakdown.">
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '50vh',
            fontSize: '20px',
          }}>
          <p>This is the Weekly Breakdown page. Only authenticated users can see this!</p>
        </div>
    </Layout>
  );
}

export default WeeklyBreakdown;