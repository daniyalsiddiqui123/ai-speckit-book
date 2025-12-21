import React from 'react';
import {render} from '@testing-library/react';
import KinematicsVisual from '../KinematicsVisual';

test('renders the kinematics visual component', () => {
  const {container} = render(<KinematicsVisual />);
  expect(container.firstChild).not.toBeNull();
});
