import React from 'react';

interface KinematicsVisualProps {
  l1?: number;
  l2?: number;
  theta1?: number;
  theta2?: number;
  scale?: number;
}

const KinematicsVisual: React.FC<KinematicsVisualProps> = ({
  l1 = 50,
  l2 = 50,
  theta1 = 30, // degrees
  theta2 = 60, // degrees
  scale = 1,
}) => {
  const rad1 = (theta1 * Math.PI) / 180;
  const rad2 = (theta2 * Math.PI) / 180;

  const x1 = l1 * Math.cos(rad1) * scale;
  const y1 = l1 * Math.sin(rad1) * scale;

  const x2 = x1 + l2 * Math.cos(rad1 + rad2) * scale;
  const y2 = y1 + l2 * Math.sin(rad1 + rad2) * scale;

  return (
    <div style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}>
      <svg width={2 * (l1 + l2) * scale} height={2 * (l1 + l2) * scale} style={{ border: '1px solid #eee' }}>
        <g transform={`translate(${ (l1 + l2) * scale }, ${ (l1 + l2) * scale }) rotate(-90)`}> {/* Center and rotate for Y-up */}
          {/* Base */}
          <circle cx="0" cy="0" r="3" fill="red" />

          {/* Link 1 */}
          <line x1="0" y1="0" x2={x1} y2={y1} stroke="blue" strokeWidth="2" />
          <circle cx={x1} cy={y1} r="3" fill="green" />

          {/* Link 2 */}
          <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="purple" strokeWidth="2" />
          <circle cx={x2} cy={y2} r="3" fill="orange" />
        </g>
      </svg>
    </div>
  );
};

export default KinematicsVisual;
