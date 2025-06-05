import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../components/ui/button';

describe('Button Component', () => {
  it('renders correctly', () => {
    render(<Button>Test Button</Button>);
    expect(screen.getByRole('button')).toBeInTheDocument();
    expect(screen.getByRole('button')).toHaveTextContent('Test Button');
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies variant classes correctly', () => {
    render(<Button variant="destructive">Destructive Button</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-destructive');
  });

  it('applies size classes correctly', () => {
    render(<Button size="sm">Small Button</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('h-8');
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled Button</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});

