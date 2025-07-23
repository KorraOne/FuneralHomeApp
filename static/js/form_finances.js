function formatCurrency(val) {
  const num = parseFloat(val.replace(/[^0-9.-]+/g, ''));
  return isNaN(num) ? "$-" : `$${num.toFixed(2)}`;
}

function updateTotals() {
  let expensesSum = 0;
  let invoiceSum = 0;

  const expensesQty = document.querySelectorAll('.expenses-qty');
  const expensesCost = document.querySelectorAll('.expenses-cost');
  const invoiceQty = document.querySelectorAll('.invoice-qty');
  const invoiceCost = document.querySelectorAll('.invoice-cost');

  for (let i = 0; i < expensesQty.length; i++) {
    const qty = parseFloat(expensesQty[i].value) || 0;
    const cost = parseFloat(expensesCost[i].value.replace(/[^0-9.-]+/g, '')) || 0;
    expensesSum += qty * cost;
  }

  for (let i = 0; i < invoiceQty.length; i++) {
    const qty = parseFloat(invoiceQty[i].value) || 0;
    const cost = parseFloat(invoiceCost[i].value.replace(/[^0-9.-]+/g, '')) || 0;
    invoiceSum += qty * cost;
  }

  document.getElementById('expenses_total').value = `$${expensesSum.toFixed(2)}`;
  document.getElementById('invoice_total').value = `$${invoiceSum.toFixed(2)}`;
}

document.querySelectorAll('.expenses-qty, .expenses-cost, .invoice-qty, .invoice-cost').forEach(input => {
  input.addEventListener('input', updateTotals);
  input.addEventListener('blur', () => {
    if (input.classList.contains('expenses-cost') || input.classList.contains('invoice-cost')) {
      input.value = formatCurrency(input.value);
    }
    updateTotals();
  });
});

window.addEventListener('DOMContentLoaded', updateTotals);