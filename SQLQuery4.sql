

CREATE TABLE Loan (
    customer_id INT,
    amount FLOAT,
    term INT,
    status VARCHAR(255),
	loan_id INT IDENTITY(1,1)
);

CREATE TABLE Repay(
    loan_id INT,
    amount FLOAT,
    due_date DATE,
    status VARCHAR(255),
);

drop table Loans

select @@SERVERNAME

select * from Loan
select * from Repay
Delete from Loans
Delete from Loan