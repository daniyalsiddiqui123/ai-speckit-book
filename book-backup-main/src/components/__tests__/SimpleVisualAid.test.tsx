import React from 'react';
import {render} from '@testing-library/react';
import SimpleVisualAid from '../SimpleVisualAid';

test('renders a visual aid container', () => {
  const {container} = render(<SimpleVisualAid />);
  expect(container.firstChild).not.toBeNull();
});
