import { render, screen } from '@testing-library/react';
import React from 'react';
import App from '../App';
import { describe, it, expect } from 'vitest';

describe('App', () => {
  it('renders upload button', () => {
    render(<App />);
    expect(screen.getByText(/upload/i)).toBeDefined();
  });
});
