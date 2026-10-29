export const CURRENCY_SYMBOLS: Record<string, string> = {
  INR: '₹',
  USD: '$',
  EUR: '€',
  GBP: '£',
  JPY: '¥',
  AED: 'د.إ',
  AUD: 'A$',
  CAD: 'C$',
  SGD: 'S$',
};

export function formatCurrency(amount: number, currency: string = 'INR'): string {
  const symbol = CURRENCY_SYMBOLS[currency] || currency;
  const rounded = Math.round(amount);
  
  // Format with commas according to locale
  const formatted = currency === 'INR'
    ? rounded.toLocaleString('en-IN')
    : rounded.toLocaleString('en-US');

  return `${symbol}${formatted}`;
}
