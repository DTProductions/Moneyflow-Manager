# Moneyflow Manager

## Description
Moneyflow Manager is a web-based application to help you track and manage where your money comes from and where it goes to, in multiple currencies.

As it turns out, converting currencies is somewhat challenging and requires both intuition and an understanding of economics. Therefore, an explanation of the calculations involved in this application can be found [here](LOGIC.md).

The technologies employed in this project are: Python, Flask, HTML, CSS, Javascript and SQL (Implemented through SQLite/SQLAlchemy).

## Supported Currencies

For now, the supported currencies are: BRL, USD, EUR and GBP.

## Functionalities

All functionalities of the application are described below.

### Login/Registration
This project features a login and registration process where the user may insert his email and password for having access to the functionalities of the application.

All other functionalities are only available to logged users.

### Overview

The main page of the application. Here the user can analyse his financial data through multiple fields.

There are 2 types of overview: Single currency and multicurrency. In both the user has to select a currency in which the data will be analysed in.

>*_Note_*: The "Total" options in the dropdown selector refer to the multicurrency views.

#### Single currency view

In the single currency view the user can see the total amount he currently has in the selected currency, his expenses and income, where they come from / go to and their totals (all limited to the selected currency).

#### Multicurrency view

In the multicurrency view the user can see all the money he has converted into the selected currency using the latest available exchange rates (in the total field), his expenses and income converted into the selected currency based on the exchange rates on the day each transaction took place, in order to represent the **_actual value of the transaction_** (you may find a more detailed explanation [here](LOGIC.md)), and also their totals.

### CRUD pages

The following pages provide the user with CRUD functionalities to manage his data in the application.

A description of what data they work with and what they are used for can be seen below.

#### Categories

Each category has a name and a type (income or expense). They determine which chart a transaction belongs to.

#### Transactions

Each transaction has a date, amount, currency and category. Each category is used to determine how the transaction is going to be calculated/shown in the overview tab, the date is used for currency conversion and the currency determines which currency the transaction used.

#### Exchanges

Exchanges are a way to transfer money from one currency into another. Each exchange contains a source currency, destination currency, source amount, destination amount and a date.

>*_Note_*: The exchange date is not used for calculations, and therefore is not a required field. Still, all other fields described in the transactions, categories and exchanges pages are required for the application to work, and therefore required.
