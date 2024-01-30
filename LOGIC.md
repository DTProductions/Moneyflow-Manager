# Application Logic

The calculations and formulas used in the application are described below, alongside the reasoning behind them.

> *_Note:_* A category needs at least one transaction tied to it for it to show in the charts.

## Single Currency View Calculations

### Total

In single currency view, the total is equal to the sum of all transactions registered as income (in the selected currency) minus the sum of all transactions registered as expenses (in the selected currency) plus the sum of all destination amounts (where the selected currency appears as destination currency) minus the sum of all source amounts (where the currency appears as source currency). So it represents the amount of money the user currently holds in the selected currency.

### Income Chart

Each chart label refers to a category registered as income, and each label's value is the sum of all amounts where the label is defined.

### Expenses Chart

Each chart label refers to a category registered as expenses, and the label values are calculated in the same way as described above.

### Chart Totals

Each chart total is the sum of all values each holds.

## Multicurrency View Calculations

### Total

In multicurrency view, the total is equal to the sum of all money the user has (his single currency totals) converted into the selected currency using the latest available exchange rates (except, of course, the selected currency total itself, since it does not need conversion).

### Income Chart

Each chart label refers to a category registered as income, and each label's value is the sum of all amounts tied to it (through a transaction), where each amount is converted into the selected currency based on the exchange rates of the day the transaction took place.

This conversion is essential because when income is received in a foreign currency (non-selected currency), its value in the local currency (selected currency) is fixed at the time of the transaction. Regardless of subsequent fluctuations in exchange rates, the initial worth of the income remains constant, reflecting its value at the moment of receipt.

In the income chart, this approach prevents a scenario where earning a specific amount in a foreign currency could lead to the foreign currency value surging against the local currency. Without considering the exchange rates at the time of the transaction, the associated label on the chart might inaccurately reflect a much larger impact than the actual value (even if the rates increased, it doesn't imply that the user earned more). This method ensures that the chart accurately represents the user's earnings in the local currency based on the exchange rates prevailing at the time of each transaction.

The same logic can be applied in the opposite situation (where exchange rates go down).

### Expenses Chart

Each chart label refers to a category registered as expenses, and the label values are calculated similarly as the income, for similar reasons.

Below is an example that demonstrates why the value of an expense does not change over time:

Consider this scenario: You live in the USA and purchased something for 400EUR when the exchange rate was such that 400EUR equaled 389USD. The key point here is that at the time of the transaction, you paid the equivalent of 389USD for the product, regardless of subsequent changes in the EUR/USD exchange rate.

Now, fast-forward, and suppose the 400EUR is now worth 400USD due to fluctuations in the exchange rate. It would be misleading to say you paid 400USD because, even though the EUR has increased in value, you initially bought the product for the equivalent of 389USD. The value you assigned to the purchase remains tied to the exchange rate at the time of the transaction.

### Chart Totals

Just like in the single currency view, each chart total is the sum of all values each holds.

### Exchange Rate Impact 

The exchange rate impact is a measure as to how the user's actions towards foreign currencies (such as choosing whether to convert money from one currency into another or not) impact his finances. It represents the amount of money that was lost or earned through exchange rates variation.

The formula is as follows: total - (total income - total expenses).

The idea behind the formula is that the user has a certain amount of money (total), and a certain amount of money he should have hadn't the exchange rates affected his money (total income - total expenses), since the income/expenses are converted based on the rates of the day of transaction, the exchange rates variation provide no impact in their totals. Therefore, the difference between the amount of money the user has and the amount of money he should have is the result of exchange rates going up and down.

The exchange rate impact may be different when looking at different currencies in the multicurrency view.