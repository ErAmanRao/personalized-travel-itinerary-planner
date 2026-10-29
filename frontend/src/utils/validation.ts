export interface BudgetValidationResult {
  isValid: boolean;
  value?: number;
  error?: string;
}

export const MAX_BUDGET = 100_000_000; // 100 Million maximum technical limit

/**
 * Normalizes and validates budget input across frontend form submission.
 * Safely handles formatted currency strings (e.g. "₹20,000", "35,000", "$15,000.50"),
 * whitespace, commas, and plain numbers without rounding or replacing valid budgets.
 */
export function parseAndValidateBudget(input: string | number | null | undefined): BudgetValidationResult {
  if (input === null || input === undefined) {
    return { isValid: false, error: 'Please enter a total trip budget.' };
  }

  let cleaned: string;
  if (typeof input === 'number') {
    if (isNaN(input)) {
      return { isValid: false, error: 'Budget must be a valid positive number.' };
    }
    if (!isFinite(input)) {
      return { isValid: false, error: 'Budget cannot be infinite.' };
    }
    cleaned = input.toString();
  } else {
    cleaned = String(input).trim();
  }

  if (!cleaned) {
    return { isValid: false, error: 'Please enter a total trip budget.' };
  }

  // Strip common currency symbols and labels safely with full regex escaping
  const symbols = ['₹', '$', '€', '£', '¥', 'A$', 'C$', 'S$', 'INR', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'SGD', 'Rs.', 'Rs', '?'];
  for (const sym of symbols) {
    const escaped = sym.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    cleaned = cleaned.replace(new RegExp(escaped, 'gi'), '');
  }

  // Strip thousands commas and surrounding whitespace
  cleaned = cleaned.replace(/,/g, '').trim();

  // Validate format: must be purely digits with at most one optional decimal point
  if (!/^\d+(\.\d+)?$/.test(cleaned)) {
    return { isValid: false, error: 'Please enter a valid positive numeric amount (e.g., 20000 or 20,000).' };
  }

  const num = parseFloat(cleaned);

  if (isNaN(num)) {
    return { isValid: false, error: 'Budget must be a valid positive number.' };
  }

  if (!isFinite(num)) {
    return { isValid: false, error: 'Budget cannot be infinite.' };
  }

  if (num <= 0) {
    return { isValid: false, error: 'Budget must be greater than zero.' };
  }

  if (num > MAX_BUDGET) {
    return { isValid: false, error: `Budget cannot exceed ${MAX_BUDGET.toLocaleString()} in chosen currency.` };
  }

  return {
    isValid: true,
    value: Math.round(num * 100) / 100,
  };
}
