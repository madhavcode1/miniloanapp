

CREATE TABLE loan (
    amount DECIMAL(18, 2),
    term INT,
    created_at DATETIME,
    status VARCHAR(255),
    customer_id INT
);


create table repayment(
loan_id int,
amount int,
due_date datetime,
status varchar(255)
)

select * from loan
select * from repayment

select @@SERVERNAME
select * from loan
ALTER TABLE loan
ADD customer_id INT;
ALTER TABLE loan
DROP COLUMN customer_id;


select * from repayment
select * from loan
SELECT SCOPE_IDENTITY()
select * from loan
DELETE FROM loan
WHERE customer_id = 1;


drop table loan,repayment


