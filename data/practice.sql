
CREATE TABLE Clients (
    ClientID INT,
    ClientName VARCHAR(100)
);

CREATE TABLE Invoices (
    InvoiceID INT,
    ClientID INT,
    Amount DECIMAL(10, 2),
    EventDate DATE
);

INSERT INTO Clients (ClientID, ClientName) VALUES
(1, 'Alpha'),
(2, 'Beta'),
(3, 'Gamma');

INSERT INTO Invoices (InvoiceID, ClientID, Amount, EventDate) VALUES
(101, 1, 100.00, '2024-01-01'),
(102, 1, 200.00, '2024-01-10'),
(103, 1, 150.00, '2024-02-01'),
(104, 2, 400.00, '2024-01-05'),
(105, 2, 100.00, '2024-02-15'),
(106, 3, 250.00, '2024-01-07');








Last N Purchases per Customer
From a Purchases table, find the last 3 purchases for each customer along with their total spend across all time.

Top Selling Products per Category
From a Products and Sales table, find the top 2 products (by revenue) in each category and also include the total category revenue.

Highest Paid Employees per Department
From an Employees table, retrieve the top 2 highest-paid employees in each department along with the department’s average salary.

Recent Orders and Lifetime Value
From an Orders table, fetch the last 2 orders of each customer and also show the lifetime total number of orders and spend for that customer.

Monthly Top Spenders
From a Transactions table, find the customer who spent the most in each month and also display their all-time spending.

Churned Customers
From a Subscriptions table, find customers who canceled in the last 30 days, along with their total subscription duration in months.

Average vs. Latest Order Value
From Orders, for each customer, show their latest order amount alongside their historical average order value.

Repeat Purchase Interval
From Orders, find for each customer the difference in days between their last 2 purchases.

First & Last Transaction per Customer
From Transactions, return the first and last transaction date of each customer, along with their total number of transactions.

Quarterly Top Revenue Clients
From Invoices, find the top 2 clients by revenue for each quarter and show their overall lifetime revenue.
select * from Invoices



















CREATE TABLE person_info (
    id INT PRIMARY KEY ,
    name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    city VARCHAR(50) NOT NULL
);

INSERT INTO person_info (id,  name, date_of_birth, city)
VALUES
(111,'Sanchita Bagde', '1996-05-14', 'Nagpur'),
(222,'Rahul Sharma', '1991-08-22', 'Mumbai'),
(333,'Priya Singh', '2007-12-03', 'Delhi')


SELECT 
    name, 
    MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)))  AS MIN_YEAR , 
    MAX(EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth))) as MAX_YEAR  , 
    count(name) as no_of_count_name
FROM person_info
GROUP BY name 
order by no_of_count_name asc




















