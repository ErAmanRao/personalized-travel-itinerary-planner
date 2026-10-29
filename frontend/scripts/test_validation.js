// Unit test script for frontend budget validation logic
import assert from 'node:assert';

const MAX_BUDGET = 100_000_000;

function parseAndValidateBudget(input) {
  if (input === null || input === undefined) {
    return { isValid: false, error: 'Please enter a total trip budget.' };
  }

  let cleaned;
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

  const symbols = ['₹', '$', '€', '£', '¥', 'A$', 'C$', 'S$', 'INR', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'SGD', 'Rs.', 'Rs', 'rs.', 'rs', '?'];
  for (const sym of symbols) {
    const escaped = sym.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    cleaned = cleaned.replace(new RegExp(escaped, 'gi'), '');
  }

  cleaned = cleaned.replace(/,/g, '').trim();

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

// 1. Valid numbers
const validCases = [
  ['20000', 20000],
  ['35000', 35000],
  ['15000', 15000],
  ['5000', 5000],
  ['100000', 100000],
  ['20,000', 20000],
  ['₹20,000', 20000],
  ['₹ 35,000.50', 35000.5],
  ['$50,000', 50000],
  ['  15000  ', 15000],
  [20000, 20000],
  [35000.75, 35000.75],
];

for (const [input, expected] of validCases) {
  const res = parseAndValidateBudget(input);
  assert.strictEqual(res.isValid, true, `Expected valid for input: ${input}`);
  assert.strictEqual(res.value, expected, `Expected value ${expected} for input: ${input}, got: ${res.value}`);
}

// 2. Invalid inputs
const invalidCases = [
  '',
  '   ',
  null,
  undefined,
  '0',
  0,
  '-5000',
  -5000,
  'invalid_text',
  'abc',
  NaN,
  Infinity,
  -Infinity,
  '100000001',
];

for (const input of invalidCases) {
  const res = parseAndValidateBudget(input);
  assert.strictEqual(res.isValid, false, `Expected invalid for input: ${input}`);
  assert(res.error, `Expected error message for input: ${input}`);
}

console.log(`PASS: All ${validCases.length} valid cases and ${invalidCases.length} invalid cases passed frontend validation tests.`);
